# Deployment Checklist

1. Push all commits to GitHub.
2. Deploy backend first and verify:
   - `/api/auth/health/`
   - `/api/monitoring/health/`
3. Set frontend env:
   - `VITE_API_BASE_URL=https://<backend-domain>/api`
4. Deploy frontend and verify login and dashboards.
5. Share final submission:
   - repository URL
   - demo credentials
   - optional live links
