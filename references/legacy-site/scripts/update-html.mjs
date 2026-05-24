// Script to update all day HTML files to use the new dynamic navigation system
// This removes hardcoded navbars and adds the sidebar container

import { readFileSync, writeFileSync } from 'fs';
import { join, resolve } from 'path';

const webDir = resolve('web');
const dayFiles = [];

// Find all day HTML files
for (let i = 1; i <= 12; i++) {
    dayFiles.push(join(webDir, `day${i}.html`));
}

dayFiles.forEach(filePath => {
    try {
        let content = readFileSync(filePath, 'utf-8');
        const originalContent = content;

        // Remove old navbar patterns (day10+ style)
        content = content.replace(
            /<nav class="navbar">[\s\S]*?<\/nav>\s*/,
            ''
        );

        // Remove old sidebar if it exists (day1-9 style)  
        content = content.replace(
            /<div class="app-container">\s*<aside class="sidebar">[\s\S]*?<\/aside>/,
            '<div class="app-container">'
        );

        // Add sidebar container if not present
        if (!content.includes('id="sidebar"')) {
            content = content.replace(
                '<div class="app-container">',
                '<div class="app-container">\n        <aside class="sidebar" id="sidebar"></aside>'
            );
        }

        // Remove old navigation buttons at bottom
        content = content.replace(
            /<div class="navigation">[\s\S]*?<\/div>/,
            ''
        );

        content = content.replace(
            /<div class="nav-buttons">[\s\S]*?<\/div>/,
            ''
        );

        // Add navigation buttons container before footer
        if (!content.includes('id="navigation-buttons"')) {
            content = content.replace(
                '</body>',
                '<div id="navigation-buttons"></div>\n    </body>'
            );
        }

        // Replace old script tags with new module script
        content = content.replace(
            /<script src="js\/main\.js"><\/script>/,
            ''
        );

        content = content.replace(
            /<script type="module" src="\/js\/main\.js"><\/script>/,
            ''
        );

        // Add new module script before closing body tag
        if (!content.includes('src="/js/main.js"')) {
            content = content.replace(
                '</body>',
                '<script type="module" src="/js/main.js"></script>\n    </body>'
            );
        }

        // Only write if content changed
        if (content !== originalContent) {
            writeFileSync(filePath, content, 'utf-8');
            console.log(`✓ Updated ${filePath}`);
        } else {
            console.log(`- No changes needed for ${filePath}`);
        }
    } catch (error) {
        console.error(`✗ Error updating ${filePath}:`, error.message);
    }
});

console.log('\n✅ All day files updated!');
