import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(
    DATABASE_URL, echo=True if os.getenv("APP_ENV") == "DEV" else False
)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
