import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from supabase import create_client, Client

app = FastAPI()

# 读取环境变量
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
ACCESS_KEY = os.getenv('ACCESS_KEY')
TABLE_NAME = os.getenv('TABLE_NAME')

# 初始化 supabase client
supabase = None
startup_error = None

# 安全初始化逻辑
try:
    if not SUPABASE_URL:
        raise ValueError("Missing environment variable: SUPABASE_URL")
    if not SUPABASE_KEY:
        raise ValueError("Missing environment variable: SUPABASE_KEY")
    if not TABLE_NAME:
        raise ValueError("Missing environment variable: TABLE_NAME")

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

except Exception as e:
    startup_error = str(e)
    print(f"Startup Error: {startup_error}")

# 路由
@app.get("/")
async def keepalive(request: Request):
    # 如果初始化出错，优雅返回
    if startup_error:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Startup failed: {startup_error}"}
        )

    # 校验 key
    key = request.query_params.get('key')
    if key != ACCESS_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

    # 发送简单查询
    try:
        response = supabase.table(TABLE_NAME).select('id').limit(1).execute()
        return {"status": "success", "message": "Keepalive ping successful."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
