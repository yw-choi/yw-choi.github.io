# Young Woo Choi Research Group Website

This is the official website for the Computational Quantum Materials Physics Lab at Sogang University, led by Prof. Young Woo Choi.

## About

The website showcases:
- Research interests and activities
- Group members and alumni
- Publications and talks
- Photo gallery
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
│   └── photos/       # Photo gallery
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

### Adding Photos

1. Upload images to `content/photos/images/`
2. Edit `content/photos/_index.md`
3. Add new entries to the `gallery` array with `src` and `caption`

### Updating People

Edit `content/people/index.html` to add or update group members and alumni.

### Adding News

Edit `content/_index.md` and add new items to the "News" section.

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
