import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { webcrypto } from 'node:crypto';

if (!globalThis.crypto) {
  globalThis.crypto = webcrypto;
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
})
