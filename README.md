# Young Woo Choi Research Group Website

This is the official website for the Computational Quantum Materials Physics Lab at Sogang University, led by Prof. Young Woo Choi.

## About

The website showcases:
- Research interests and activities
- Group members and alumni
- Publications and talks
- News and group photos
- Contact information

## Technology Stack

- **Static Site Generator**: [Hugo](https://gohugo.io/) v0.128.0
- **Theme**: Custom theme (`ywchoi`)
- **CSS Framework**: Bootstrap 5.3.3
- **Font**: Arial
- **Hosting**: GitHub Pages
- **Deployment**: GitHub Actions

## Development

### Prerequisites

- Hugo Extended v0.128.0 or later
- Git

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yw-choi/yw-choi.github.io.git
   cd yw-choi.github.io
   ```

2. Run the Hugo development server:
   ```bash
   hugo server -D
   ```

3. Open your browser to `http://localhost:1313`

### Building for Production

```bash
hugo --minify
```

The built site will be in the `public/` directory.

## Project Structure

```
.
├── content/           # Content files (Markdown)
│   ├── _index.md     # Homepage content
│   ├── people/       # People page
│   ├── research/     # Research page
│   ├── publications/ # Publications page
│   ├── talks/        # Talks page
│   ├── news/         # News archive
│   └── photos/       # Original photo assets and legacy redirect
├── data/news.yaml    # Shared News / Recent News feed
├── static/           # Static files (images, PDFs, etc.)
├── themes/           # Hugo theme
│   └── ywchoi/      # Custom theme
└── hugo.toml         # Hugo configuration
```

## Features

### SEO Optimization
- Meta tags (description, keywords)
- Open Graph and Twitter Card support
- Schema.org structured data
- Sitemap generation
- robots.txt
- RSS feeds

### Accessibility
- Semantic HTML5
- ARIA labels and roles
- Skip-to-content link
- Keyboard navigation support
- Screen reader friendly

### Performance
- Lazy loading for images
- Resource preloading and prefetching
- DNS prefetch for external resources
- Minified CSS and JavaScript in production

### Responsive Design
- Mobile-first approach
- Bootstrap responsive grid
- Collapsible navigation menu
- Touch-friendly interface

### Print Support
- Optimized print stylesheet
- Proper page breaks
- Simplified layout for printing

## Deployment

The site is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the `main` branch.

### Deployment Workflow

1. Push changes to `main` branch
2. GitHub Actions workflow runs:
   - Installs Hugo
   - Builds the site with `hugo --minify`
   - Deploys to GitHub Pages

## Content Management

### Adding Publications

Edit `content/publications/_index.md` and add new publications in the numbered list format.
The homepage's **Recent Papers** section automatically uses the first five entries,
in the same order. Keep the `publication-title` and `publication-citation` spans;
give each title a stable `id` so its homepage link opens the matching entry.

### Adding News and Photos

Both `/news/` and the homepage's five **Recent News** entries use `data/news.yaml`.
Add new images under `static/images/news/`, then add a post:

```yaml
- id: 2026-11-example
  date: "2026-11-08"
  title: Optional short title
  comment: A short description of the news.
  kind: photo
  images:
    - /images/news/example.webp
    - /images/news/example-2.webp
```

`id`, `date`, `comment`, and at least one local image are required. The build
rejects duplicate IDs and missing images. `title`, `image_alt`, `category`,
`status`, and `link` are optional. Omit `title` to use the comment as the card
and homepage label; long labels are visually truncated without shortening the
modal text. Use plain text for titles and comments.

Posts are sorted newest first. Dates can be `YYYY-MM-DD` or, for older records
without a known day, `YYYY-MM`. Equal dates retain their order in the YAML file.
A known day sorts ahead of a month-only date in the same month. The migration
preserves the original news dates rather than inventing days.

Use `kind: photo` for photographs, `document` for a published paper's first-page
capture, `poster` for official event posters/program covers, and `icon` for
announcements. `banner` gives transparent white event artwork a dark background.
Accepted papers use `/images/news/accepted.svg` (fireworks).
Keep a published paper's full PDF outside this repository; only its first-page
preview is needed. Existing photos remain at `/photos/images/` so old image URLs
continue to work. `/photos/` redirects to `/news/`.

Each card opens the shared modal, with a fixed image viewport, optional title,
comment and date. Multiple images support buttons, arrow keys and touch swipes.
Link directly to a post with `/news/#<id>`.

Image provenance and the one outstanding PDF preview are documented in
[`static/images/news/README.md`](static/images/news/README.md).

### Updating People

Edit `content/people/index.html` to add or update group members and alumni.

## Contributing

For internal contributors:
1. Create a feature branch
2. Make your changes
3. Test locally with `hugo server`
4. Submit a pull request

## Contact

**Young Woo Choi**  
Assistant Professor  
Department of Physics  
Sogang University  
Email: ywchoi02@sogang.ac.kr

## License

Copyright © 2024-2025 Quantum Materials Physics Lab, Sogang University. All Rights Reserved.
