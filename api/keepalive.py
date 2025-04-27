import os
from supabase import create_client, Client
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# 读取环境变量
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
ACCESS_KEY = os.getenv('ACCESS_KEY')  # 防止别人乱访问的Key
TABLE_NAME = os.getenv('TABLE_NAME')  # 你的轻量表名

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
async def keepalive(request: Request):
    # 校验key
    key = request.query_params.get('key')
    if key != ACCESS_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

    # 发送一个简单查询
    try:
        response = supabase.table(TABLE_NAME).select('id').limit(1).execute()
        return {"status": "success", "message": "Keepalive ping successful."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
