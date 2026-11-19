import { defineConfig } from 'vite';
export default defineConfig({ server: { proxy: { '/__integration_api': { target: 'http://127.0.0.1:8000', rewrite: path => path.replace('/__integration_api', '') } } } });
