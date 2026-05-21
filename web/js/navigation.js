// DSA Study Plan - Navigation Configuration
// Centralized nav data for consistent navigation across all pages

export const studyDays = [
    { day: 1, title: 'Arrays & Hashing', week: 1, weekTitle: 'Week 1 - Foundations' },
    { day: 2, title: 'Advanced Arrays', week: 1, weekTitle: 'Week 1 - Foundations' },
    { day: 3, title: 'Strings', week: 1, weekTitle: 'Week 1 - Foundations' },
    { day: 4, title: 'Stack & Queue', week: 1, weekTitle: 'Week 1 - Foundations' },
    { day: 5, title: 'Linked List', week: 1, weekTitle: 'Week 1 - Foundations' },
    { day: 6, title: 'Trees', week: 1, weekTitle: 'Week 1 - Foundations' },
    { day: 7, title: 'Review', week: 1, weekTitle: 'Week 1 - Foundations' },
    { day: 8, title: 'Graphs', week: 2, weekTitle: 'Week 2 - Advanced Structures' },
    { day: 9, title: 'Advanced Graphs', week: 2, weekTitle: 'Week 2 - Advanced Structures' },
    { day: 10, title: 'Review & Practice', week: 2, weekTitle: 'Week 2 - Advanced Structures' },
    { day: 11, title: 'DP Part 1', week: 3, weekTitle: 'Week 3 - Dynamic Programming' },
    { day: 12, title: 'Advanced DP', week: 3, weekTitle: 'Week 3 - Dynamic Programming' },
    { day: 13, title: 'More Advanced DP', week: 3, weekTitle: 'Week 3 - Dynamic Programming' },
    { day: 14, title: 'Review & Practice', week: 3, weekTitle: 'Week 3 - Dynamic Programming' },
    { day: 15, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 16, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 17, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 18, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 19, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 20, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 21, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 22, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 23, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 24, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 25, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 26, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 27, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 28, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 29, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' },
    { day: 30, title: 'TBD', week: 4, weekTitle: 'Week 4 - Advanced Topics' }
];

// Get current day from URL
export function getCurrentDay() {
    const match = window.location.pathname.match(/day(\d+)\.html/);
    return match ? parseInt(match[1]) : 0;
}

// Check if a day file exists (only days 1-12 created so far)
export function dayExists(dayNumber) {
    return dayNumber >= 1 && dayNumber <= 12;
}
