from sqlalchemy.ext.asyncio import AsyncSession


class KyrgyzAdventureRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
