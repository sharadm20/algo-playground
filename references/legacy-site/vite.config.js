import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
    root: 'web',
    server: {
        port: 8080,
        open: true,
        hot: true,
        host: true
    },
    build: {
        outDir: resolve(__dirname, 'dist'),
        emptyOutDir: true,
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'web/index.html'),
                day1: resolve(__dirname, 'web/day1.html'),
                day2: resolve(__dirname, 'web/day2.html'),
                day3: resolve(__dirname, 'web/day3.html'),
                day4: resolve(__dirname, 'web/day4.html'),
                day5: resolve(__dirname, 'web/day5.html'),
                day6: resolve(__dirname, 'web/day6.html'),
                day7: resolve(__dirname, 'web/day7.html'),
                day8: resolve(__dirname, 'web/day8.html'),
                day9: resolve(__dirname, 'web/day9.html'),
                day10: resolve(__dirname, 'web/day10.html'),
                day11: resolve(__dirname, 'web/day11.html'),
                day12: resolve(__dirname, 'web/day12.html')
            }
        }
    },
    publicDir: resolve(__dirname, 'web/public'),
    css: {
        devSourcemap: true
    }
});
