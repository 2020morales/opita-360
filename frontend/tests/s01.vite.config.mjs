// Isolated browser-test proxy; production API URL and CORS remain unchanged.
export default {
  server: { proxy: { '/__s01_api': {
    target: 'http://127.0.0.1:8000',
    rewrite: path => path.replace(/^\/__s01_api/, '')
  } } }
};
