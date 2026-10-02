# attempts

Writings about AI, philosophy, life, sports, kids.

Reminders to myself.

Built with [Hugo](https://gohugo.io) and the PaperMod theme, deployed to GitHub Pages at https://thomasht86.github.io/attempts/.

## Writing

```sh
hugo new content posts/my-post.md   # creates a draft
hugo server -D                      # live preview at http://localhost:1313 (-D includes drafts)
```

Set `draft = false` when a post is ready, then push to `main`. GitHub Actions builds and deploys it.

- Code fences are highlighted at build time (Chroma).
- ` ```mermaid ` fences render as diagrams (mermaid.js is loaded only on pages that use it).

## Cross-posting to X

Add `crosspost = ['x']` to a post's front matter. When the post is published, the deploy workflow also publishes it as an X Article: images and mermaid diagrams are uploaded, code and tables are kept, and the article ends with a link back to the post. Each post goes out once; `data/crossposts/x.json` records what was posted, and the workflow commits it back (run `git pull` afterwards).

- Preview the conversion: `uv run scripts/crosspost_x.py --dry-run --file content/posts/<post>.md`
- Edits made after a post is on X don't sync; the X API can't update an article. Edit it on X by hand.
- X accepts PNG, JPEG, GIF and WebP images. Other formats (SVG) are replaced by a text placeholder.
- Needs X Premium, plus an X developer app with OAuth 1.0a user tokens (read and write) stored as repo secrets: `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_TOKEN_SECRET`. Without the secrets, the job skips cross-posting with a warning.

## Built to keep working for years

- **Hugo version is pinned** in `.github/workflows/pages.yml` (`HUGO_VERSION`). Use the same version locally. To upgrade, bump it, run `hugo server`, and fix any warnings.
- **The theme is a copy** in `themes/PaperMod/` (not a submodule), taken from upstream commit `d3768854` (2026-08-02). Edit it freely.
- **mermaid.js is a local copy** (`static/js/mermaid.min.js`, v11.17.2), so no CDN is needed.

## Notes

- `content/old/` holds the posts migrated from the MkDocs site. They keep their old URLs through `url` in the front matter, and they are listed only at `/old/`, not on the home page, archive or RSS (`mainSections` in `hugo.toml`). New posts go in `content/posts/` and get `/posts/<slug>/`.
- `archive/` holds the original Norwegian posts. They are not published.
- `static/twister/` is a standalone HTML app, served as-is.
