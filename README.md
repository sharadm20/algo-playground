# 30-Day DSA Study Plan

A comprehensive 30-day Data Structures and Algorithms study plan with Python and Rust implementations, detailed documentation, and a modern web UI for browsing materials.

## 🚀 Quick Start

### Web UI (Recommended)
**Windows:**
```bash
# Double-click this file or run:
start_web_server.bat
```

**Mac/Linux:**
```bash
chmod +x start_web_server.sh
./start_web_server.sh
```

**Alternative methods:**
```bash
# Using npm
npm start

# Using Python (with file watching)
python start_server_enhanced.py

# Direct Python server
cd web && python -m http.server 8080
```

Then open **http://localhost:8080** in your browser.

## 📚 Project Structure

```
ds_and_algo/
├── QWEN.md                    # Main context file (progress tracking)
├── Day1_Arrays_Hashing.docx   # Day 1 documentation
├── Day2_Advanced_Arrays.docx  # Day 2 documentation
├── Day3_String_Manipulation.docx
├── Day4_Stack_Queue.docx
├── Day5_Linked_List.docx
├── Day6_Trees.docx
├── python_projects/           # Python implementations
│   ├── day1_arrays_hashing.py
│   ├── day2_advanced_arrays.py
│   ├── day3_strings.py
│   ├── day4_stack_queue.py
│   ├── day5_linked_list.py
│   └── day6_trees.py
├── rust_projects/             # Rust implementations
│   ├── day2_advanced_arrays.rs
│   ├── day3_strings.rs
│   ├── day4_stack_queue.rs
│   ├── day5_linked_list.rs
│   ├── day6_trees.rs
│   ├── day2_arrays/           # Cargo projects
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   ├── day3_strings/
│   ├── day4_stack_queue/
│   ├── day5_linked_list/
│   └── day6_trees/
└── web/                       # Web UI
    ├── index.html             # Home page
    ├── day1.html - day7.html  # Daily materials
    ├── css/style.css
    └── js/main.js
```

## 📅 Progress

| Day | Topic | Status | Implementations |
|-----|-------|--------|----------------|
| 1 | Arrays & Hashing | ✅ Completed | Python |
| 2 | Advanced Arrays | ✅ Completed | Python + Rust |
| 3 | String Manipulation | ✅ Completed | Python + Rust |
| 4 | Stack & Queue | ✅ Completed | Python + Rust |
| 5 | Linked List | ✅ Completed | Python + Rust |
| 6 | Trees & Binary Trees | ✅ Completed | Python + Rust |
| 7 | Review & Practice | 📝 Upcoming | - |

## 🛠️ Running Code

### Python
```bash
cd python_projects
python day6_trees.py  # Replace with any day
```

### Rust
```bash
cd rust_projects/day6_trees
cargo test   # Run tests
cargo run    # Run binary
```

## 🌐 Web Server Options

| Method | Command | Features |
|--------|---------|----------|
| **Batch Script** | `start_web_server.bat` | One-click start (Windows) |
| **Shell Script** | `./start_web_server.sh` | One-click start (Unix) |
| **npm** | `npm start` | Cross-platform |
| **Enhanced** | `python start_server_enhanced.py` | File change detection |
| **Direct** | `cd web && python -m http.server 8080` | Simple Python server |

### Enhanced Server Features
- 📁 File change detection
- 🔔 Auto-reload notifications
- 🎨 Colorized log output
- ⚡ No caching headers for development

## 📖 Using the Study Plan

1. **Open the Web UI** at http://localhost:8080
2. **Navigate to the current day** using the sidebar
3. **Read the documentation** in the Word files (.docx)
4. **Study the code implementations** in Python and Rust
5. **Run the tests** to verify everything works
6. **Practice the homework problems** listed in each day's materials

## 🎯 Learning Approach

Each day covers:
- **Core Concepts** - Detailed explanations with examples
- **Patterns** - Reusable problem-solving techniques
- **Implementations** - Production-ready code in Python and Rust
- **Practice Problems** - LeetCode problems categorized by difficulty
- **Complexity Analysis** - Time and space complexity for all algorithms

## 🔮 Future Improvements

### Web UI Enhancement (Planned)
- Migrate to React + Vite for hot reload
- React Router for better navigation
- Syntax highlighting for code blocks
- Dark mode toggle
- Progress tracking with localStorage
- Deploy to GitHub Pages or Netlify

See `QWEN.md` for full details.

## 📝 Notes

- **Python Environment**: Use base Python (not conda)
- **Rust Version**: 2021 edition
- **Web Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)
- **IDE**: VS Code recommended for both Python and Rust

## 🤝 Contributing

This is a personal study plan. Feel free to fork and customize for your own learning journey!

## 📄 License

MIT License - Free to use for educational purposes.

---

**Happy Coding! 🚀**
