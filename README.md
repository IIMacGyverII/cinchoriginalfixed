# cinchoriginalfixed

Production-ready static website for **CINCH Systems** (Adobe Muse-based HTML/CSS).

## Current Status

This repository has been updated and validated for:

- Sitewide SEO metadata coverage (title, description, canonical, OG, Twitter, robots, viewport)
- Sitewide structured data coverage (JSON-LD WebPage / Organization where applicable)
- Internal link integrity and external link refreshes
- External and datasheet links opening in new tabs
- Consistent social metadata alignment:
  - `og:title` == page `<title>`
  - `twitter:title` == page `<title>`
  - `og:description` == meta description
  - `twitter:description` == meta description
- Copyright footer year normalization to **2026** across pages
- Removal of deprecated content and references:
  - `alarm-communication.html` and related navigation/sitemap/manifest references
  - CE-TCP module references and removed assets

## Project Structure

- `*.html` — page templates/content (Adobe Muse export style)
- `css/` — per-page and master CSS
- `images/` — site image assets
- `assets/` — downloadable PDFs/datasheets
- `sitemap.xml` — indexed page list
- `robots.txt` — crawler directives
- `muse_manifest.xml` — Muse manifest mapping

## Key Standards

### Footer + Legal

- Footer copyright text should use:
  - `Copyright © 2026 CINCH™ systems Inc. All Rights Reserved...`
- Footer links should include:
  - Privacy Policy
  - Terms of Use

### Links

- External URLs: must use `target="_blank"`.
- Datasheet/document links (`assets/*.pdf`): must use `target="_blank"`.
- Internal navigation links: stay in same tab unless explicitly required otherwise.

### Metadata

Each page should include, at minimum:

- `<title>`
- `<meta name="description" ...>`
- `<link rel="canonical" ...>`
- Open Graph (`og:title`, `og:description`, `og:url`, `og:image`)
- Twitter (`twitter:title`, `twitter:description`, `twitter:image`, `twitter:card`)
- `meta name="robots" content="index, follow"`
- JSON-LD block

## Homepage Notes

- `index.html` contains a restored top background layer (`u25112-5`) behind the top menu/tagline.
- Avoid removing this element unless coordinated CSS updates are made.

## Maintenance Workflow

1. Make targeted edits (avoid broad formatting changes).
2. Re-audit affected areas:
   - links
   - metadata consistency
   - footer/legal consistency
3. Validate no unintended file changes.
4. Commit with focused message and push to `main`.

## Deployment

This repository is maintained directly on `main` and pushed to:

- `https://github.com/IIMacGyverII/cinchoriginalfixed`

If hosting cache is aggressive, perform a hard refresh after deployment to validate visual/UI changes.
