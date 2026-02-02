import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  // Add this to help Vite resolve the package
  optimizeDeps: {
    include: ['react-markdown']
  }
})