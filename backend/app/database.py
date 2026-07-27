from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Convert drivers to async equivalents
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith("sqlite://"):
    DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
else:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


from datetime import datetime, timezone

engine = create_async_engine(DATABASE_URL, echo=settings.ENV == "development")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
