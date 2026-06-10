import uuid
from sqlalchemy import Column, String, DateTime, Integer, Boolean, Numeric, ForeignKey, func
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER, TINYINT
from sqlalchemy.orm import relationship
from app.database import Base

# 1. MODEL NGƯỜI DÙNG (Bảng Users)
class User(Base):
    __tablename__ = "Users"

    UserId = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    FullName = Column(String(100), nullable=False)
    Email = Column(String(150), unique=True, nullable=False, index=True)
    PasswordHash = Column(String(255), nullable=False)
    CreatedAt = Column(DateTime, server_default=func.getdate())


# 2. MODEL DANH MỤC THU CHI (Bảng Categories)
class Category(Base):
    __tablename__ = "Categories"

    CategoryId = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(100), nullable=False)
    CategoryType = Column(Boolean, nullable=False)  # 1: Income (Thu), 0: Expense (Chi)
    IconUrl = Column(String(255), nullable=True)


# 3. MODEL HŨ TÀI CHÍNH (Bảng Jars)
class Jar(Base):
    __tablename__ = "Jars"

    JarId = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    JarName = Column(String(100), nullable=False)
    Description = Column(String(255), nullable=True)
    Budget = Column(Numeric(18, 2), default=0)
    JarType = Column(TINYINT, default=1)  # 1: Personal, 2: Group
    CreatedByUserId = Column(UNIQUEIDENTIFIER, ForeignKey("Users.UserId"), nullable=False)
    CreatedAt = Column(DateTime, server_default=func.getdate())


# 4. MODEL THÀNH VIÊN HŨ NHÓM (Bảng JarMembers - Quan hệ Nhiều-Nhiều)
class JarMember(Base):
    __tablename__ = "JarMembers"

    JarId = Column(UNIQUEIDENTIFIER, ForeignKey("Jars.JarId"), primary_key=True)
    UserId = Column(UNIQUEIDENTIFIER, ForeignKey("Users.UserId"), primary_key=True)
    Role = Column(String(20), default="Member")
    JoinedAt = Column(DateTime, server_default=func.getdate())


# 5. MODEL GIAO DỊCH (Bảng Transactions)
class Transaction(Base):
    __tablename__ = "Transactions"

    TransactionId = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    JarId = Column(UNIQUEIDENTIFIER, ForeignKey("Jars.JarId"), nullable=False)
    UserId = Column(UNIQUEIDENTIFIER, ForeignKey("Users.UserId"), nullable=False)
    CategoryId = Column(Integer, ForeignKey("Categories.CategoryId"), nullable=False)
    Amount = Column(Numeric(18, 2), nullable=False)
    Description = Column(String(500), nullable=True)
    ReceiptImageUrl = Column(String(500), nullable=True)  # Đường dẫn ảnh cục bộ từ camera
    TransactionType = Column(Boolean, nullable=False)
    TransactionDate = Column(DateTime, server_default=func.getdate())