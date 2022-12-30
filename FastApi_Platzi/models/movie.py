from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):                  #Con esto decimos que Movie sera una identidad de la base de datos

    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)