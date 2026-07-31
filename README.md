# SS Jewellery E-Commerce Application

A full-stack luxury jewellery e-commerce application featuring a Flask (Python) backend and React (Vite) frontend.

## Production Environment & Deployment Configuration

When deploying the application to cloud hosting platforms (**Render**, **Oracle Cloud**, **Railway**, **AWS**, **Vercel**, etc.), ensure the following environment variables are properly set in your hosting platform dashboard:

### Backend Environment Variables (`backend/`)

| Variable Name | Required | Description | Example |
| :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | Yes | Target runtime environment (`PROD` or `DEV`). | `PROD` |
| `JWT_SECRET` | **Required** | Strong, unique secret key used to sign and verify JWT authentication tokens. | `your_production_jwt_secret_key_here` |
| `SECRET_KEY` | **Required** | Secret key for Flask session security. | `your_production_flask_secret_key_here` |
| `FRONTEND_URL` | **Required** | Deployed frontend domain URL for CORS allowlist. | `https://ssjewellery.onrender.com` |
| `DATABASE_URL` | Yes | PostgreSQL / Neon DB connection URI. | `postgresql://user:pass@ep-xyz.neon.tech/neondb` |
| `LOGGING_LEVEL` | No | Logging verbosity (`INFO`, `DEBUG`, `WARN`). | `INFO` |

### Frontend Environment Variables (`frontend/`)

| Variable Name | Required | Description | Example |
| :--- | :--- | :--- | :--- |
| `VITE_API_BASE_URL` | **Required** | Base URL pointing to deployed backend API. | `https://ssjewellery-api.onrender.com/api` |

---

## Authentication & CORS Security Notes

- **CORS Allowlist**: The backend automatically reads `FRONTEND_URL` and `ALLOWED_ORIGINS` to permit cross-origin requests with `credentials: true`.
- **JWT Authentication**: All admin and user endpoints use `Bearer` tokens transmitted via standard `Authorization` headers.
- **Axios Configuration**: The React frontend uses global interceptors that automatically attach credentials and authorization headers to all API requests.
