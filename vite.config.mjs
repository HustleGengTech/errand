import { defineConfig } from "vite";
import { resolve } from 'path';
import tailwindcss from "@tailwindcss/vite"

export default defineConfig({
  root: resolve("./static/src"),
  base: "/static/",
  build: {
    manifest: true,
    outDir: resolve("./static/dist"),
    assetsDir: "assets",
    rollupOptions: {
      input: {
        main: resolve("./static/src/main.js"),
      },
    },
    emptyOutDir: true,
  },
  plugins: [
    tailwindcss()
  ]
})
