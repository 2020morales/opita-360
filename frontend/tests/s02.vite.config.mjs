// Test-only proxy; production API/CORS remain unchanged.
export default { server: { proxy: { '/__s02_api': {
  target: 'http://127.0.0.1:8000', rewrite: path => path.replace(/^\/__s02_api/, '')
} } } };
