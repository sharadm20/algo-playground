// DSA Study Plan - Sidebar Navigation Renderer
// Dynamically generates consistent sidebar navigation

import { studyDays, getCurrentDay, dayExists } from './navigation.js';

// Progress Manager
class ProgressManager {
    constructor() {
        this.storageKey = 'dsaProgress';
        this.data = this.load();
    }

    load() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            if (stored) {
                return JSON.parse(stored);
            }
        } catch (e) {
            console.warn('Failed to load progress:', e);
        }
        return { completedDays: [], currentDay: 0, lastVisited: null };
    }

    save() {
        try {
            this.data.lastVisited = new Date().toISOString();
            localStorage.setItem(this.storageKey, JSON.stringify(this.data));
        } catch (e) {
            console.warn('Failed to save progress:', e);
        }
    }

    markComplete(dayNumber) {
        if (!this.data.completedDays.includes(dayNumber)) {
            this.data.completedDays.push(dayNumber);
            this.data.completedDays.sort((a, b) => a - b); // Keep sorted
            this.data.currentDay = dayNumber;
            this.save();
        }
    }

    markIncomplete(dayNumber) {
        this.data.completedDays = this.data.completedDays.filter(d => d !== dayNumber);
        this.save();
    }

    isComplete(dayNumber) {
        return this.data.completedDays.includes(dayNumber);
    }

    getCompletedDays() {
        return [...this.data.completedDays];
    }
}

// Sidebar Renderer
class SidebarRenderer {
    constructor(progressManager) {
        this.progress = progressManager;
        this.currentDay = getCurrentDay();
    }

    render() {
        const sidebar = document.getElementById('sidebar');
        if (!sidebar) return;

        // Build sidebar HTML
        let html = `
            <div class="sidebar-header">
                <h1>📚 DSA Study Plan</h1>
                <p>30 Days to Mastery</p>
                <button class="progress-toggle" id="progress-toggle" title="Toggle auto-complete">
                    Auto-complete: <span id="auto-complete-status">${this.progress.isComplete(this.currentDay) ? 'ON' : 'OFF'}</span>
                </button>
            </div>
        `;

        // Home link
        html += `
            <nav class="nav-section">
                <div class="nav-section-title">Overview</div>
                <ul class="nav-list">
                    <li class="nav-item">
                        <a href="index.html" class="nav-link ${this.currentDay === 0 ? 'active' : ''}">
                            <span class="day-badge">🏠</span>
                            <span class="day-title">Home</span>
                        </a>
                    </li>
                </ul>
            </nav>
        `;

        // Group by weeks
        const weeks = {};
        studyDays.forEach(dayInfo => {
            if (!weeks[dayInfo.week]) {
                weeks[dayInfo.week] = {
                    title: dayInfo.weekTitle,
                    days: []
                };
            }
            weeks[dayInfo.week].days.push(dayInfo);
        });

        // Render each week
        Object.keys(weeks).sort((a, b) => a - b).forEach(weekNum => {
            const week = weeks[weekNum];
            
            // Check if any days in this week exist
            const hasExistingDays = week.days.some(d => dayExists(d.day));
            if (!hasExistingDays) return;

            html += `
                <nav class="nav-section">
                    <div class="nav-section-title">${week.title}</div>
                    <ul class="nav-list">
            `;

            week.days.forEach(dayInfo => {
                const exists = dayExists(dayInfo.day);
                const isComplete = this.progress.isComplete(dayInfo.day);
                const isCurrent = dayInfo.day === this.currentDay;
                const isPast = dayInfo.day < this.currentDay;
                const isFuture = dayInfo.day > this.currentDay;

                let linkClass = 'nav-link';
                if (isCurrent) linkClass += ' active';
                if (isComplete) linkClass += ' completed';

                let statusIcon = '';
                if (isComplete) {
                    statusIcon = '<span class="status-icon">✓</span>';
                } else if (isCurrent) {
                    statusIcon = '<span class="status-icon">●</span>';
                } else if (isPast && exists) {
                    statusIcon = '<span class="status-icon incomplete">○</span>';
                } else if (isFuture && exists) {
                    statusIcon = '<span class="status-icon upcoming">→</span>';
                }

                const href = exists ? `day${dayInfo.day}.html` : '#';
                const clickHandler = exists ? '' : `onclick="alert('Day ${dayInfo.day} content not yet created!'); return false;"`;

                html += `
                    <li class="nav-item">
                        <a href="${href}" class="${linkClass}" data-day="${dayInfo.day}" ${clickHandler}>
                            <span class="day-badge">${dayInfo.day}</span>
                            <span class="day-title">${dayInfo.title}</span>
                            ${statusIcon}
                        </a>
                    </li>
                `;
            });

            html += `
                    </ul>
                </nav>
            `;
        });

        sidebar.innerHTML = html;

        // Setup event listeners
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Auto-complete toggle
        const toggleBtn = document.getElementById('progress-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                if (this.currentDay > 0) {
                    if (this.progress.isComplete(this.currentDay)) {
                        this.progress.markIncomplete(this.currentDay);
                    } else {
                        this.progress.markComplete(this.currentDay);
                    }
                    this.render(); // Re-render to update UI
                }
            });
        }

        // Mark previous days as complete when navigating back
        this.setupAutoComplete();
    }

    setupAutoComplete() {
        // When visiting a day, automatically mark all previous days as complete
        if (this.currentDay > 1) {
            const shouldAutoComplete = localStorage.getItem('dsaAutoComplete') !== 'false';
            if (shouldAutoComplete) {
                for (let i = 1; i < this.currentDay; i++) {
                    this.progress.markComplete(i);
                }
            }
        }

        // Mark current day as complete after spending 30 seconds on page
        if (this.currentDay > 0 && !this.progress.isComplete(this.currentDay)) {
            let timeSpent = 0;
            const checkInterval = setInterval(() => {
                timeSpent++;
                if (timeSpent >= 30) {
                    this.progress.markComplete(this.currentDay);
                    this.render(); // Update UI to show checkmark
                    clearInterval(checkInterval);
                }
            }, 1000);

            // Also mark complete on page unload (user visited the page)
            window.addEventListener('beforeunload', () => {
                this.progress.markComplete(this.currentDay);
            });
        }
    }
}

// Navigation Buttons (Previous/Next/Home)
class NavigationButtons {
    constructor(progressManager) {
        this.progress = progressManager;
        this.currentDay = getCurrentDay();
    }

    render(containerId = 'navigation-buttons') {
        const container = document.getElementById(containerId);
        if (!container || this.currentDay === 0) return;

        const prevDay = this.currentDay - 1;
        const nextDay = this.currentDay + 1;
        const hasNext = dayExists(nextDay);

        let html = '<div class="nav-buttons">';

        // Previous button
        if (prevDay >= 1) {
            html += `
                <a href="day${prevDay}.html" class="nav-btn prev-btn">
                    <span class="btn-icon">←</span>
                    <span class="btn-text">
                        <span class="btn-label">Previous</span>
                        <span class="btn-day">Day ${prevDay}</span>
                    </span>
                </a>
            `;
        }

        // Home button
        html += `
            <a href="index.html" class="nav-btn home-btn">
                <span class="btn-icon">🏠</span>
                <span class="btn-text">
                    <span class="btn-label">Home</span>
                </span>
            </a>
        `;

        // Next button (only if exists and not completed)
        if (hasNext) {
            const isNextCompleted = this.progress.isComplete(nextDay);
            const btnClass = isNextCompleted ? 'nav-btn next-btn completed' : 'nav-btn next-btn';
            const label = isNextCompleted ? 'Next' : 'Upcoming';
            html += `
                <a href="day${nextDay}.html" class="${btnClass}">
                    <span class="btn-text">
                        <span class="btn-label">${label}</span>
                        <span class="btn-day">Day ${nextDay}</span>
                    </span>
                    <span class="btn-icon">→</span>
                </a>
            `;
        }

        // Mark complete button
        const isCurrentComplete = this.progress.isComplete(this.currentDay);
        if (!isCurrentComplete) {
            html += `
                <button class="nav-btn complete-btn" id="mark-complete-btn">
                    <span class="btn-icon">✓</span>
                    <span class="btn-text">
                        <span class="btn-label">Mark Complete</span>
                    </span>
                </button>
            `;
        } else {
            html += `
                <button class="nav-btn complete-btn completed" id="mark-complete-btn" title="Already completed">
                    <span class="btn-icon">✓</span>
                    <span class="btn-text">
                        <span class="btn-label">Completed</span>
                    </span>
                </button>
            `;
        }

        html += '</div>';
        container.innerHTML = html;

        // Setup event listeners
        this.setupEventListeners();
    }

    setupEventListeners() {
        const completeBtn = document.getElementById('mark-complete-btn');
        if (completeBtn && !completeBtn.classList.contains('completed')) {
            completeBtn.addEventListener('click', () => {
                this.progress.markComplete(this.currentDay);
                this.render(); // Re-render buttons
                // Also update sidebar
                window.sidebar?.render();
            });
        }
    }
}

// Export classes
export { ProgressManager, SidebarRenderer, NavigationButtons };
