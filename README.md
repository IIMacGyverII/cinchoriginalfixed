Shim removal and top-gap fixes
================================

Summary
- Performed conservative, reversible edits to remove unwanted top-of-page gaps caused by Adobe Muse browser-width shim nodes (elements like `#uNNNN` and `#uNNNN-bw`).
- Created a preview JSON (`shim_removal_preview.json`) listing 107 shim candidates and their CSS references.

What was changed
- Trial: removed `#u4474` from `intrusion-detection-systems.html` on branch `shim/remove-u4474-ids` (backup saved as `intrusion-detection-systems.html.bak`).
- Per-page fixes: added inline shim-hide overrides to six top pages (index/about/training/news/partners/contact) on branch `shim/hide-top-shims`. Backups for each edited HTML were saved as `*.html.bak`.
- `.gitignore` updated to ignore `shim_removal_preview.json`.

Next steps
- Parse `shim_removal_preview.json` and run a guarded per-page batch:
  1. Create a branch for each batch.
  2. Back up the page as `page.html.bak`.
  3. Apply a reversible inline shim-hide or coordinated CSS update.
  4. Bump CSS cache-bust query (`?v=`) for that page.
  5. Visually verify, then commit.

If you want me to proceed, I will parse the preview and apply the next guarded batch (10 pages), create backups, and open the diffs for review.
# cinchoriginalfixed

Static website for CINCH Systems, built with Adobe Muse CC 2018. This repo contains the production-ready, optimized version of the site.

---

## Project Changes

### HTML Optimization (All 108 Pages)

- Removed UTF-8 BOM characters from all HTML files that were causing rendering issues
- Optimized all pages for SEO and performance
- Ensured consistent structure and encoding across the entire site

### 20th Anniversary Badge

- Added `CinchMaxout20year2.webp` anniversary badge to the footer of all 108 pages
- Badge is positioned to the right of the phone number in the footer bar using `position:absolute; left:300px; top:15px`
- On `index.html` the badge uses `top:29px` to match the index footer's phone number position
- Badge is 80×80px and uses `id="cinch-anniversary"`

### Page Jump / Layout Shift Fixes

**Scrollbar reflow fix (`css/site_global.css`)**
- Added `overflow-y:scroll` to the `html` rule so the scrollbar is always visible
- Prevents the ~8px horizontal content shift that occurred when navigating between pages of different heights (short pages have no scrollbar, tall pages do)

**VBS nav bar alignment (36 CSS files)**
- All VBS pages use a different nav column structure (`#u4746` + `#u4746_position_content`) compared to secondary/IDS/door pages
- Original `#u4746 margin-top` was `-10px`, causing the nav bar to appear ~14px too high on VBS pages
- Corrected `#u4746 margin-top` across all 36 VBS CSS files so the nav bar lands precisely at **21px from the page top**, matching all other page types:
  - 31 files: `margin-top:-3px` (paired with `#u4746_position_content { padding-top:15px }`)
  - 4 files: `margin-top:-3px` (paired with `padding:15px` shorthand directly on `#u4746`)
  - 1 file (`vbs_e-r-kit.css`): uses IDS nav structure, already correct — no change needed

**Index page nav bar alignment (`css/index.css`)**
- `index.html` uses a different nav column (`#u270`) compared to all other pages
- `#u270 margin-top` was `13px`, placing the nav bar 1px lower than all other pages (22px vs 21px)
- Changed to `12px` so `index.html` nav bar matches all other pages at exactly **21px**

**Verified nav bar position across all 5 page types:**

| Page type | Files | Nav bar top from page |
|-----------|-------|-----------------------|
| Index | 1 | 21px |
| Secondary | 10 | 21px |
| IDS | 53 | 21px |
| VBS | 36 | 21px |
| Door / Gate | 7 | 21px |

### Background & Styling Consistency

**`css/index.css`**
- `#page` background: removed grey-to-white gradient (`linear-gradient #DCDCDC→#FFFFFF`) → `background-image:none; background-color:#FFFFFF` to match all other pages
- `#page` `min-height`: `694px` → `693px` to match all other pages
- `#u107` and `#u107-bw` flag background height: `583px` → `581px` to match all other pages

**VBS flag background (35 CSS files)**
- `#u4660,#u4660-bw{min-height:581px}` split into two rules:
  - `#u4660{height:581px}` — fixed height replacing `min-height`, matching all other page types
  - `#u4660-bw{margin-top:7px;height:581px}` — added the 7px top offset present on all other page types
- Note: In VBS pages `#u4660-bw` is the **DOM parent** of the nav column (`#u4746`), unlike all other page types where the flag bg is a sibling of the nav. Adding `margin-top:7px` to `#u4660-bw` therefore also shifted the nav bar down by 7px, requiring a compensating adjustment (see below)

**VBS nav bar re-correction after flag bg fix (35 CSS files)**
- Because `#u4660-bw` is the nav's parent, the `margin-top:7px` flag bg fix pushed the nav 7px lower
- Corrected by changing `#u4746 margin-top: 4px → -3px` across all 35 files
- Final VBS nav formula: `7(u4660-bw) + (-3)(u4746) + 15(u4746_position_content) + 2(menuu11870) = 21px`

**All 5 page types confirmed identical on every shared structural property:**

| Property | All page types |
|----------|----------------|
| `#page` background | `#FFFFFF` solid white, `background-image:none` |
| `#page` min-height | `693px` |
| Flag bg `-bw` height | `581px` |
| Flag bg `-bw` margin-top | `7px` |
| Nav bar top from page | `21px` |
| Menu bar dimensions | `640×53px`, `margin-top:2px`, `left:6px` |

---

## Site Structure

- **108 HTML pages** across 5 layout types (index, secondary, IDS, VBS, door/gate)
- **Per-page CSS files** in `css/` — one `.css` per HTML page, plus 5 master layout CSS files
- **`css/site_global.css`** — global styles shared by all pages
- **`images/`** — all site images including WebP assets
