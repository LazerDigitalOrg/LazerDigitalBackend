from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncSession

async_engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost:5433/lazerdigital"
)
async_session = async_sessionmaker(async_engine,class_=AsyncSession)
