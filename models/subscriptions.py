from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from database import Base

class PushSubscription(Base):
    __tablename__ = "push_subscription"

    id = Column(Integer, primary_key=True, index=True)

    endpoint = Column(String, unique=True, nullable=False)
    public_browser_key = Column(String, nullable=False)
    auth = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False)
