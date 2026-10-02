# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "markdown-it-py==3.0.0",
#   "requests==2.32.3",
#   "requests-oauthlib==2.0.0",
# ]
# ///
"""Cross-post opted-in blog posts to X as Articles.

A post opts in with `crosspost = ['x']` in its front matter. Only published
pages under content/posts/ are considered, and each is posted at most once:
successful posts are recorded in data/crossposts/x.json.

    uv run scripts/crosspost_x.py --dry-run                 # show what would be posted
    uv run scripts/crosspost_x.py --dry-run --file <post>   # preview one post (even a draft)
    uv run scripts/crosspost_x.py                           # post for real (needs X_* env vars)

X API docs: https://docs.x.com/x-api/articles/introduction
"""

import argparse
import base64
import csv
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import tomllib
from datetime import datetime, timezone

import requests
from markdown_it import MarkdownIt

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = ROOT / "data" / "crossposts" / "x.json"
API = "https://api.x.com/2"
MERMAID_CLI = "@mermaid-js/mermaid-cli@11.12.0"
HEADERS = {1: "header-one", 2: "header-two"}  # h3 and deeper → header-three
IMAGE_TYPES = {"png", "jpg", "jpeg", "gif", "webp"}  # what X accepts as tweet_image
CHROME = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
          "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]


def utf16_len(s):
    """DraftJS offsets are JavaScript string indices (UTF-16 code units)."""
    return len(s.encode("utf-16-le")) // 2


def read_post(path):
    text = path.read_text()
    if not text.startswith("+++"):
        sys.exit(f"{path}: expected TOML front matter (+++)")
    _, fm, body = text.split("+++", 2)
    return tomllib.loads(fm), body


# --- Markdown → DraftJS content state ---------------------------------------


class Converter:
    def __init__(self, post_path, upload_image):
        self.post_dir = post_path.parent
        self.upload_image = upload_image  # (bytes, filename) -> media_id, or None in dry-run
        self.blocks, self.entities = [], []

    def entity(self, type_, data, mutability):
        self.entities.append(
            {"key": str(len(self.entities)), "value": {"type": type_, "mutability": mutability, "data": data}}
        )
        return len(self.entities) - 1

    def atomic(self, type_, data, mutability):
        key = self.entity(type_, data, mutability)
        self.blocks.append({"type": "atomic", "text": " ", "entity_ranges": [{"key": key, "offset": 0, "length": 1}]})

    def text_block(self, type_, text, styles, links):
        if not text.strip():
            return
        block = {"type": type_, "text": text}
        if styles:
            block["inline_style_ranges"] = styles
        if links:
            block["entity_ranges"] = links
        self.blocks.append(block)

    def image(self, src, alt=""):
        data, name = self.load_image(src)
        if data is None:
            self.text_block("unstyled", f"[Image: {alt or src}]", [], [])
            return
        media_id = self.upload_image(data, name) if self.upload_image else f"<dry-run:{name}>"
        payload = {"media_items": [{"media_category": "tweet_image", "media_id": media_id}]}
        if alt:
            payload["caption"] = alt
        self.atomic("image", payload, "immutable")

    def load_image(self, src):
        if src.rsplit(".", 1)[-1].lower().split("?")[0] not in IMAGE_TYPES:
            print(f"  warning: X only takes PNG/JPEG/GIF/WebP, skipping {src}", file=sys.stderr)
            return None, None
        if src.startswith(("http://", "https://")):
            r = requests.get(src, timeout=30)
            if r.ok and r.headers.get("content-type", "").startswith("image/"):
                return r.content, src.rsplit("/", 1)[-1]
            print(f"  warning: could not fetch image {src}", file=sys.stderr)
            return None, None
        local = ROOT / "static" / src.lstrip("/") if src.startswith("/") else self.post_dir / src
        if local.is_file():
            return local.read_bytes(), local.name
        print(f"  warning: image not found: {src}", file=sys.stderr)
        return None, None

    def mermaid(self, source):
        with tempfile.TemporaryDirectory() as tmp:
            src, out, cfg = (pathlib.Path(tmp) / n for n in ("d.mmd", "d.png", "puppeteer.json"))
            src.write_text(source)
            chrome = os.environ.get("CHROME_PATH") or next(filter(None, map(shutil.which, CHROME)), None)
            cfg.write_text(json.dumps({"args": ["--no-sandbox"], **({"executablePath": chrome} if chrome else {})}))
            cmd = ["npx", "-y", MERMAID_CLI, "-i", src, "-o", out, "-s", "2", "-b", "white", "-p", cfg]
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=180)
                data = out.read_bytes()
            except (subprocess.SubprocessError, OSError) as e:
                print(f"  warning: mermaid render failed ({e}); linking to the post instead", file=sys.stderr)
                return False
        media_id = self.upload_image(data, "diagram.png") if self.upload_image else "<dry-run:diagram.png>"
        self.atomic("image", {"media_items": [{"media_category": "tweet_image", "media_id": media_id}]}, "immutable")
        return True

    def inline(self, children):
        """Flatten inline tokens into text + style ranges + link ranges. Images are returned separately."""
        text, styles, links, images = "", [], [], []
        open_styles, open_link = {}, None
        style_of = {"strong": "bold", "em": "italic", "s": "strikethrough"}
        for t in children:
            kind = t.type.removesuffix("_open").removesuffix("_close")
            if t.type in ("text", "code_inline"):  # X has no inline-code style; keep the text
                text += t.content
            elif t.type == "softbreak":
                text += " "
            elif t.type == "hardbreak":
                text += "\n"
            elif kind in style_of and t.type.endswith("_open"):
                open_styles[kind] = utf16_len(text)
            elif kind in style_of and t.type.endswith("_close"):
                start = open_styles.pop(kind)
                styles.append({"style": style_of[kind], "offset": start, "length": utf16_len(text) - start})
            elif t.type == "link_open":
                open_link = (utf16_len(text), t.attrs["href"])
            elif t.type == "link_close" and open_link:
                start, href = open_link
                key = self.entity("link", {"url": href}, "mutable")
                links.append({"key": key, "offset": start, "length": utf16_len(text) - start})
                open_link = None
            elif t.type == "image":
                images.append((t.attrs["src"], t.content))
        return text, styles, links, images

    def convert(self, markdown, post_url):
        md = MarkdownIt("commonmark").enable(["table", "strikethrough"])
        lines = markdown.splitlines()
        tokens = md.parse(markdown)
        block_type, list_depth = "unstyled", []
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t.type == "heading_open":
                block_type = HEADERS.get(int(t.tag[1]), "header-three")
            elif t.type == "heading_close":
                block_type = "unstyled"
            elif t.type in ("bullet_list_open", "ordered_list_open"):
                list_depth.append("unordered-list-item" if t.type == "bullet_list_open" else "ordered-list-item")
            elif t.type in ("bullet_list_close", "ordered_list_close"):
                list_depth.pop()
            elif t.type == "blockquote_open":
                block_type = "blockquote"
            elif t.type == "blockquote_close":
                block_type = "unstyled"
            elif t.type == "inline":
                text, styles, links, images = self.inline(t.children)
                type_ = list_depth[-1] if list_depth and block_type == "unstyled" else block_type
                self.text_block(type_, text, styles, links)
                for src, alt in images:
                    self.image(src, alt)
            elif t.type == "fence" and t.info.strip() == "mermaid":
                if not self.mermaid(t.content):
                    key = self.entity("link", {"url": post_url}, "mutable")
                    label = "[Diagram: see the original post]"
                    self.blocks.append({"type": "unstyled", "text": label,
                                        "entity_ranges": [{"key": key, "offset": 0, "length": utf16_len(label)}]})
            elif t.type in ("fence", "code_block"):
                lang = t.info.strip().split(" ")[0]
                self.atomic("markdown", {"markdown": f"```{lang}\n{t.content.rstrip()}\n```"}, "mutable")
            elif t.type == "table_open":  # X takes tables as a markdown entity: pass the source through
                start, end = t.map
                self.atomic("markdown", {"markdown": "\n".join(lines[start:end]).strip()}, "mutable")
                while tokens[i].type != "table_close":
                    i += 1
            elif t.type == "hr":
                self.atomic("divider", {}, "immutable")
            i += 1

        # Footer pointing back to the canonical post.
        self.atomic("divider", {}, "immutable")
        prefix, label = "Originally published at ", post_url
        key = self.entity("link", {"url": post_url}, "mutable")
        self.blocks.append({"type": "unstyled", "text": prefix + label,
                            "entity_ranges": [{"key": key, "offset": utf16_len(prefix), "length": utf16_len(label)}]})
        return {"blocks": self.blocks, "entities": self.entities}


# --- X API ---------------------------------------------------------------------


def x_session():
    from requests_oauthlib import OAuth1

    names = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"]
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        return None, missing
    s = requests.Session()
    s.auth = OAuth1(*(os.environ[n] for n in names))
    return s, []


def call(session, path, payload=None):
    r = session.post(f"{API}{path}", json=payload, timeout=60)
    body = r.json() if r.content else {}
    if not r.ok or body.get("errors"):
        sys.exit(f"X API {path} failed ({r.status_code}): {json.dumps(body)}")
    return body["data"]


def make_uploader(session):
    def upload(data, name):
        print(f"  uploading {name}")
        payload = {"media": base64.b64encode(data).decode(), "media_category": "tweet_image"}
        return call(session, "/media/upload", payload)["id"]

    return upload


# --- Main ----------------------------------------------------------------------


def published_posts():
    """(path, permalink) for every published, non-future page in the posts section, via Hugo itself."""
    out = subprocess.run(["hugo", "list", "published"], cwd=ROOT, check=True, capture_output=True, text=True).stdout
    now = datetime.now(timezone.utc)
    for row in csv.DictReader(io.StringIO(out)):
        if row["kind"] == "page" and row["section"] == "posts":
            if datetime.fromisoformat(row["publishDate"].replace("Z", "+00:00")) <= now:
                yield row["path"], row["permalink"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print the payloads; call nothing")
    ap.add_argument("--file", help="only this post (with --dry-run, drafts and opt-out are ignored)")
    args = ap.parse_args()

    state = json.loads(STATE.read_text()) if STATE.exists() else {}

    if args.file:
        path = pathlib.Path(args.file).resolve().relative_to(ROOT).as_posix()
        permalinks = dict(published_posts())
        candidates = [(path, permalinks.get(path, f"<permalink of {path}>"))]
    else:
        candidates = list(published_posts())

    todo = []
    for path, url in candidates:
        fm, body = read_post(ROOT / path)
        if path in state:
            print(f"skip {path}: already on X ({state[path]['url']})")
        elif "x" in fm.get("crosspost", []) or (args.file and args.dry_run):
            todo.append((path, url, fm, body))

    if not todo:
        print("Nothing to cross-post.")
        return

    session = None
    if not args.dry_run:
        session, missing = x_session()
        if not session:
            print(f"::warning::X credentials not set ({', '.join(missing)}); skipping cross-posting.")
            return

    for path, url, fm, body in todo:
        print(f"{'[dry-run] ' if args.dry_run else ''}{path} → X Article")
        uploader = make_uploader(session) if session else None
        content_state = Converter(ROOT / path, uploader).convert(body, url)
        payload = {"title": fm["title"], "content_state": content_state}
        cover = (fm.get("cover") or {}).get("image")
        if cover:
            data, name = Converter(ROOT / path, None).load_image(cover)
            if data:
                media_id = uploader(data, name) if uploader else f"<dry-run:{name}>"
                payload["cover_media"] = {"media_category": "tweet_image", "media_id": media_id}

        if args.dry_run:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            continue

        draft = call(session, "/articles/draft", payload)
        published = call(session, f"/articles/{draft['id']}/publish")
        state[path] = {
            "article_id": draft["id"],
            "post_id": published["post_id"],
            "url": f"https://x.com/i/status/{published['post_id']}",
            "published": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        # Record each success immediately so a later failure never causes a repost.
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        print(f"  published: {state[path]['url']}")


if __name__ == "__main__":
    main()
