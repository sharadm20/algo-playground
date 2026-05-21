# DSA Study Plan Web App

A modern static site powered by **Vite** for browsing DSA study materials.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
web/
├── index.html           # Home page
├── day1.html - day12.html  # Daily lesson pages
├── css/
│   └── style.css        # Global styles
├── js/
│   └── main.js          # Client-side JavaScript (progress tracking, syntax highlighting)
└── public/              # Static assets (images, fonts, etc.)
```

## 🛠️ Features

- ⚡ **Hot Reload**: Instant updates during development
- 📊 **Progress Tracking**: localStorage-based completion tracking
- 🎨 **Syntax Highlighting**: Code block highlighting
- ⌨️ **Keyboard Shortcuts**: 
  - `Ctrl+Shift+C`: Copy code block
  - `Escape`: Toggle sidebar
- 📱 **Responsive Design**: Works on desktop and mobile

## 🔧 Development

```bash
# Start dev server (port 8080)
npm run dev

# Build optimized production files
npm run build

# Preview production build
npm run preview
```

## 🌐 Access

Open http://localhost:8080 in your browser.

## 📦 Tech Stack

- **Vite**: Next-gen frontend build tool
- **Vanilla JS**: No framework overhead
- **CSS3**: Modern styling with CSS variables
- **localStorage**: Client-side progress persistence

## 📝 Adding New Days

1. Create `dayN.html` in `web/` directory
2. Add entry to `vite.config.js` input object
3. Update navigation in existing HTML files
4. Run `npm run dev` to see it live

## 🎯 Future Improvements

- [ ] React migration for component reusability
- [ ] Markdown-based content generation
- [ ] Dark mode toggle
- [ ] Search functionality
- [ ] Print-friendly PDFs
