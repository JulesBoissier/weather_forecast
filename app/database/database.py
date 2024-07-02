from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, Date

from sqlalchemy.orm import Session

from contextlib import contextmanager


# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./weather.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    date = Column(String, index=True)
    min_temp = Column(Float)
    max_temp = Column(Float)
    avg_temp = Column(Float)
    humidity = Column(Float)

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


# Create all tables
Base.metadata.create_all(bind=engine)


def get_weather(db: Session, city: str, date: str):
    return db.query(Weather).filter(Weather.city == city, Weather.date == date).first()


def create_weather(db: Session, weather: Weather):
    db.add(weather)
    db.commit()
    db.refresh(weather)
    return weather


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
