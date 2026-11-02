# US import duty in a Next.js app

A form and a [route handler](app/api/duty/route.ts). The handler calls the API with the
`tarifftrust` package, so the key stays on the server and the browser only ever calls your route.

```bash
npm install
TARIFFTRUST_API_KEY=tarifftrust_... npm run dev
```

Then open http://localhost:3000. The package has no dependency and works in any server-side runtime
with `fetch`. Never import it into a client component: that would ship your key to the browser.
