// Test-only proxy; production CORS unchanged.
export default {server:{proxy:{'/__s04_api':{target:'http://127.0.0.1:8000',rewrite:path=>path.replace(/^\/__s04_api/,'')}}}};
