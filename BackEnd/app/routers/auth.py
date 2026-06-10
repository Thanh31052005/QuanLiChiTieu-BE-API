from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from app.database import get_db
from app.models.models import User

# --- ĐỊNH NGHĨA PHẦN DỮ LIỆU ĐẦU VÀO / ĐẦU RA ---
# Dữ liệu từ Flutter gửi lên khi Đăng ký
class UserRegister(BaseModel):
    FullName: str
    Email: EmailStr
    Password: str

# Dữ liệu API trả về cho Flutter (Ẩn mật khẩu để bảo mật)
class UserResponse(BaseModel):
    UserId: UUID
    FullName: str
    Email: EmailStr
    CreatedAt: datetime

    class Config:
        from_attributes = True


# --- KHỞI TẠO ROUTER (Biến mà file main.py đang tìm kiếm đây rồi!) ---
router = APIRouter(prefix="/auth", tags=["Authentication"])


# --- API ĐĂNG KÝ TÀI KHOẢN TEST KẾT NỐI DB ---
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    # 1. Kiểm tra xem Email này đã có ai đăng ký trong SQL Server chưa
    db_user = db.query(User).filter(User.Email == user_in.Email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email này đã được sử dụng!")
    
    # 2. Tạo User mới (Tạm thời để mật khẩu thô để kiểm tra xem SQL Server có INSERT được không)
    new_user = User(
        FullName=user_in.FullName,
        Email=user_in.Email,
        PasswordHash=user_in.Password 
    )
    
    # 3. Lưu vào SQL Server
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user