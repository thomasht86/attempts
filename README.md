# attempts

Writings about AI, philosophy, life, sports, kids.

Reminders to myself.

Built with [Hugo](https://gohugo.io) and the PaperMod theme, deployed to GitHub Pages at https://thomasht86.github.io/ad-se-ipsum/.

## Writing

```sh
hugo new content posts/my-post.md   # creates a draft
hugo server -D                      # live preview at http://localhost:1313 (-D includes drafts)
```

Set `draft = false` when a post is ready, then push to `main`. GitHub Actions builds and deploys it.

- Code fences are highlighted at build time (Chroma).
- ` ```mermaid ` fences render as diagrams (mermaid.js is loaded only on pages that use it).

## Built to keep working for years

- **Hugo version is pinned** in `.github/workflows/pages.yml` (`HUGO_VERSION`). Use the same version locally. To upgrade, bump it, run `hugo server`, and fix any warnings.
- **The theme is a copy** in `themes/PaperMod/` (not a submodule), taken from upstream commit `d3768854` (2026-08-02). Edit it freely.
- **mermaid.js is a local copy** (`static/js/mermaid.min.js`, v11.17.2), so no CDN is needed.

## Notes

- `content/old/` holds the posts migrated from the MkDocs site. They keep their old URLs through `url` in the front matter, and they are listed only at `/old/`, not on the home page, archive or RSS (`mainSections` in `hugo.toml`). New posts go in `content/posts/` and get `/posts/<slug>/`.
- `archive/` holds the original Norwegian posts. They are not published.
- `static/twister/` is a standalone HTML app, served as-is.
