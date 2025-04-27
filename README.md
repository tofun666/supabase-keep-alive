# Supabase Keep Alive

A lightweight Python serverless project to keep your Supabase database alive.  
It periodically sends a small query to prevent the database from going idle.  
This project is optimized for deployment on Vercel and is intended to be triggered by an external cron service.

## Features

- 🔒 Secure endpoint with access key validation
- 🛠 Configurable target table via environment variables
- 🚀 Fully serverless, ideal for Vercel hosting
- 📦 Simple environment setup
- 🆓 Open-source, non-commercial use only

## Project Structure

```
supabase-keepalive/
├── api/
│   └── keepalive.py
├── .env.example
├── requirements.txt
├── vercel.json
└── LICENSE
```

## Getting Started

### 1. Set Up Environment Variables

Create a `.env` file based on the provided `.env.example`:

```env
SUPABASE_URL=https://your-supabase-project.supabase.co
SUPABASE_KEY=your-supabase-api-key
ACCESS_KEY=your-access-key
TABLE_NAME=your-table-name
```

**Important:**  
Never commit your real `.env` file.  
On Vercel, configure these environment variables in **Project Settings > Environment Variables**.

---

### 2. Deploy to Vercel

- Push the project to a GitHub repository.
- Import the repository into [Vercel](https://vercel.com/).
- Set up environment variables on the Vercel dashboard.
- Deploy your project.

---

### 3. Set Up External Cron Job

Use any external cron service (such as EasyCron, UptimeRobot, GitHub Actions)  
to periodically trigger your endpoint once per day:

```
GET https://your-vercel-project.vercel.app/api/keepalive?key=your-access-key
```

The `key` parameter must match the `ACCESS_KEY` you configured.

---

## API Endpoint

**GET `/api/keepalive`**

| Parameter | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `key` | Query Parameter | Yes | Must match `ACCESS_KEY` to authorize the request. |

### Response

- Success:  
  ```json
  { "status": "success", "message": "Keepalive ping successful." }
  ```
- Failure:  
  ```json
  { "status": "error", "message": "error details" }
  ```

---

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.

- ✅ You may share and adapt the code.
- ❌ Commercial use is **not permitted**.

Read the full license here: [CC BY-NC 4.0 License](https://creativecommons.org/licenses/by-nc/4.0/)

---

## Notes

- This project uses [Supabase Python Client](https://github.com/supabase-community/supabase-py) and [FastAPI](https://fastapi.tiangolo.com/).
- Keep the queried table lightweight to ensure minimal resource usage.
- Supabase databases usually remain active, but periodic pings add an extra layer of stability for serverless applications.