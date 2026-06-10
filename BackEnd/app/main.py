import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db, engine, Base
from app.routers import auth

# Tự động tạo thư mục chứa ảnh camera nếu chưa có
os.makedirs("static/uploads/receipts", exist_ok=True)

app = FastAPI(title="Shared Jars API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)

# KIỂM TRA KẾT NỐI DATABASE KHI KHỞI ĐỘNG
@app.on_event("startup")
def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("🚀 [SUCCESS] Kết nối đến SQL Server thành công!")
    except Exception as e:
        print(f"❌ [ERROR] Kết nối Database thất bại. Chi tiết lỗi: {e}")

@app.get("/")
def read_root():
    return {"status": "Online", "database": "Connected"}