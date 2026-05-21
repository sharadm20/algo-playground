import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import mdx from '@mdx-js/rollup';
import { resolve } from 'path';

export default defineConfig({
  root: 'web',
  plugins: [
    react(),
    mdx(),
  ],
  server: {
    port: 5173,
    open: true,
    hot: true,
    host: true,
  },
  build: {
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: true,
  },
});
