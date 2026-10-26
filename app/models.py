from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from app.database import Base
from datetime import datetime, timezone

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "course"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    author = Column(String(255), index=True, nullable=False)
    duration = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    discount = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Обратная связь (один курс содержит много видео), только для ORM (нет в БД)
    videos: Mapped[List["Video"]] = relationship(back_populates="course")

    def __repr__(self):
        return f"<Course(id={self.id}, name='{self.name}')>"
    
class Video(Base):
    __tablename__ = 'video'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    author = Column(String(100))
    file_path = Column(String(255), nullable=False)  # Путь к файлу видео на диске

    # Реальная колонка, которая связана с course (есть в БД)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    # Прямая связь: одно видео принадлежит одному курсу, только для ORM (нет в БД)
    course: Mapped["Course"] = relationship(back_populates="videos")


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String(30), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(20))
    surname = Column(String(20))
    accessible_videos = Column(Text)
    # created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class Role(Base):
    __tablename__ = 'role'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id = Column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    # Храним только хеш: утечка БД не должна давать рабочие токены
    token_hash = Column(String(64), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

