// DSA Study Plan - Main Application
import { getCurrentDay } from './navigation.js';
import { ProgressManager, SidebarRenderer, NavigationButtons } from './sidebar.js';

class DSAStudyPlan {
    constructor() {
        this.currentDay = getCurrentDay();
        this.progress = new ProgressManager();
        this.sidebar = new SidebarRenderer(this.progress);
        this.navButtons = new NavigationButtons(this.progress);
        this.init();
    }

    init() {
        // Render navigation components
        this.sidebar.render();
        this.navButtons.render();

        // Expose sidebar to window for button callbacks
        window.sidebar = this.sidebar;

        // Enable smooth scrolling
        this.enableSmoothScrolling();

        // Highlight code blocks
        this.highlightCodeBlocks();

        // Setup keyboard shortcuts
        this.setupKeyboardShortcuts();
    }

    // Enable smooth scrolling for anchor links
    enableSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Add syntax highlighting to code blocks
    highlightCodeBlocks() {
        const codeBlocks = document.querySelectorAll('.code-block');
        codeBlocks.forEach(block => {
            const code = block.textContent;
            block.innerHTML = this.syntaxHighlight(code);
        });
    }

    // Simple syntax highlighting
    syntaxHighlight(code) {
        // Python keywords
        const keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return',
                          'import', 'from', 'in', 'not', 'and', 'or', 'True', 'False',
                          'None', 'try', 'except', 'with', 'as', 'lambda', 'yield', 'global'];

        // Rust keywords
        const rustKeywords = ['fn', 'let', 'mut', 'if', 'else', 'for', 'while', 'return',
                              'use', 'mod', 'pub', 'struct', 'impl', 'trait', 'enum',
                              'match', 'ref', 'const', 'static', 'async', 'await'];

        let highlighted = code;

        // Highlight comments
        highlighted = highlighted.replace(/(\/\/.*$|#.*$)/gm, '<span class="comment">$1</span>');

        // Highlight strings
        highlighted = highlighted.replace(/(".*?"|'.*?'|`.*?`)/g, '<span class="string">$1</span>');

        // Highlight numbers
        highlighted = highlighted.replace(/\b(\d+)\b/g, '<span class="number">$1</span>');

        // Highlight functions
        highlighted = highlighted.replace(/\b(\w+)(?=\()/g, '<span class="function">$1</span>');

        return highlighted;
    }

    // Setup keyboard shortcuts
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+Shift+C to mark current day as complete
            if (e.ctrlKey && e.shiftKey && e.key === 'C') {
                if (this.currentDay > 0) {
                    this.progress.markComplete(this.currentDay);
                    this.sidebar.render();
                    this.navButtons.render();
                }
            }

            // Left arrow to go to previous day
            if (e.altKey && e.key === 'ArrowLeft') {
                const prevDay = this.currentDay - 1;
                if (prevDay >= 1) {
                    window.location.href = `day${prevDay}.html`;
                }
            }

            // Right arrow to go to next day
            if (e.altKey && e.key === 'ArrowRight') {
                const nextDay = this.currentDay + 1;
                if (nextDay <= 12) {
                    window.location.href = `day${nextDay}.html`;
                }
            }
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.dsaStudyPlan = new DSAStudyPlan();
});

// Export for use in inline scripts
export default DSAStudyPlan;
