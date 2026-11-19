// Test-only proxy; production API URL/CORS unchanged.
export default {server:{proxy:{'/__s03_api':{target:'http://127.0.0.1:8000',rewrite:path=>path.replace(/^\/__s03_api/,'')}}}};
