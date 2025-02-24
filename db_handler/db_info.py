import asyncio
from decouple import config
from sqlalchemy import Column, Integer, String, select, Boolean, Text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

Base = declarative_base()


class Info(Base):
    
    __tablename__ = 'info'

    id = Column('id', Integer, primary_key=True)
    name = Column('Название', String(64))
    amount = Column('Стоимость', Integer)
    description = Column('Описание', Text)
    photo_link = Column('Ссылка на фото', String)
    is_active = Column('Активно?', Boolean, default=True)


class DB:
    
    def __init__(self):
        self.engine = create_async_engine(config('ASYNC_PG_LINK'), echo=True)
        self.session = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_records_count(self) -> int:
        async with self.session() as session:
            count = await session.execute(select(func.count()).select_from(Info))
            return count.scalar()

    async def create(self, data) -> None:

        async with self.session() as session:
            if type(data) is list:
                info_entity_list: list[Info] = [Info(**item) for item in data]
            elif type(data) is dict:
                info_entity_list: list[Info] = [Info(**data)]
            session.add_all(info_entity_list)
            try:
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
           
    async def get_queryset_of_count(self, count_start: int = 0, count_parts: int = 0) -> list[Info]:
        records: list = []
        async with self.session() as session:
            result = await session.execute(select(Info))
            info_list = result.scalars().all()
            
            for record in info_list:
                record = record.__dict__
                record.pop('_sa_instance_state')
                records.append(record)
            
            return records

# async def init_db():
#     db = DB()
#     async with db.engine.begin() as conn:
#         # Создаем все таблицы
#         await conn.run_sync(Base.metadata.create_all)

# # async def drop_user_table():
# #     async with engine.begin() as conn:
# #         # Удаляем только таблицу 'users'
# #         await conn.run_sync(Schedule_url.__table__.create)

# asyncio.run(init_db())
