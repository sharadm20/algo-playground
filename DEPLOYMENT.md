# Deployment Guide

## Local (Docker)

```bash
docker compose build
docker compose up -d
```

- Frontend: http://localhost:8080
- Backend API: http://localhost:8001/api/languages

## Free-Tier Production Deployments

### Recommended: Vercel (frontend) + Render (backend)

**Why this combo:**
- Vercel is the best free static host for Vite SPAs — automatic HTTPS, global CDN, zero config
- Render runs arbitrary web services (Python/Rust/Go) with a free tier — enough for the sandboxed code runner

### Step 1 — Backend on Render

1. Create an account at https://render.com
2. New Web Service → connect your GitHub repo
3. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
   - **Plan**: Free (512 MB RAM, spins down after 15 min idle — first request after idle takes ~30s)
4. Deploy → note your URL like `https://dsa-backend.onrender.com`

### Step 2 — Frontend on Vercel

1. Create an account at https://vercel.com
2. Import repo → keep default settings (Vite auto-detected)
3. Add environment variable:
   - `VITE_API_BASE` = `https://dsa-backend.onrender.com` (your Render URL)
4. Deploy → get URL like `https://dsa-plan.vercel.app`

### Step 3 — Make the API URL configurable

The frontend's `useCodeRunner` hook currently hardcodes `http://127.0.0.1:8001`. For production it needs to read from env:

**`web/src/hooks/useCodeRunner.js`** — change line:
```js
const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8001';
```

After this change, `VITE_API_BASE` environment variable controls the endpoint.

### Step 4 — Vercel SPA routing

Vite SPAs need client-side routing fallback. Create `web/vercel.json`:
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

### Alternative free-tier options

| Platform | Frontend | Backend | Notes |
|----------|----------|---------|-------|
| **Vercel** | ✅ Free (100GB bw) | ❌ No backend runtime | Best for the SPA |
| **Netlify** | ✅ Free (100GB bw) | ❌ Functions only (no subprocess) | Good alternative to Vercel |
| **Cloudflare Pages** | ✅ Free (unlimited bw) | ❌ No backend runtime | Fastest CDN |
| **Render** | ✅ Free | ✅ Free (512MB, spins down) | Best for the backend |
| **Railway** | ✅ Free ($5 credit) | ✅ Free ($5 credit, no spin-down) | Better backend perf than Render |
| **Fly.io** | ❌ | ✅ Free (256MB) | Needs Docker image |
| **PythonAnywhere** | ❌ | ✅ Free (limited Python) | Simpler but no Rust/Go |

### Cost comparison (free tier limits)

| Platform | RAM | Bandwidth | Idle spin-down | Custom domain |
|----------|-----|-----------|----------------|---------------|
| Vercel | N/A (static) | 100 GB/mo | No | Yes |
| Render | 512 MB | 100 GB/mo | After 15 min | Yes (with DNS) |
| Railway | ~500 MB | No limit | No | Yes ($5/mo for custom domain) |

### Production caveats

- **Backend sandboxing**: Render's free tier runs your container but subprocess sandboxing is less strict than Docker's seccomp profiles. For production security, consider running the backend on a paid tier with Docker isolation.
- **Idle spin-down**: Render's free web service spins down after 15 minutes of inactivity. The first request after idle takes ~30 seconds to cold-start. For no spin-down, upgrade to a paid plan ($7/mo).
- **Language runners**: Render supports Python (uvicorn) natively. For Rust/Go/Java runners, ensure the respective compilers/runtimes are installed in the container by adding to the build command.
