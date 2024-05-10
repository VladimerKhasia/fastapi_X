from datetime import datetime
from typing import Optional
from sqlalchemy import TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship #, MappedAsDataclass

class Base(DeclarativeBase):
    """If you want create as dataclass: 
       class Base(MappedAsDataclass, DeclarativeBase) 
       but that changes the logic and will break current implementation"""
    pass

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    published: Mapped[bool] = mapped_column(server_default='TRUE')
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                           server_default=text('now()'))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner: Mapped["User"] = relationship()

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                           server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)  

 
    