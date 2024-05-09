from sqlalchemy import Column, DateTime, Integer, String, Float

# from src.models.base import Base
# from src.core.db import Base
from src.db.base_class import Base
from sqlalchemy.sql.expression import func


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    country = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
