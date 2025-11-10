

SQLAlchemy - самая популярная на данный момент ORM.

## Устройство SQLAlchemy 

Алхимия имеет 2 слоя + DBAPI:
1) **DBAPI** - иными словами движок, драйвер. Например: asyncpg для Postgresql. По сути API, которая отправляет к БД запросы.
2) **CORE** - работает с соединением к БД, открывает и закрывает их, отправляет запросы к DBAPI. Формирует запросы.
3) **ORM** - необязателен, но рекомендуется к использованию. По сути помогает работать с объектами.


## Подключение к Базе Данных, сырые SQL запросы через engine

### Библиотеки
Пример зависимостей для связки SQLAlchemy + PostgreSQL

```
alembic==1.12.0

asyncpg==0.28.0

psycopg==3.1.12

psycopg-binary==3.1.12

sqlalchemy==2.0.20
```

- sqlalchemy - самая алхимия
- asyncpg - DBAPI для асинхронных запросов
- psycopg - DBAPI для синхронных запросов
- psycopg-binary - для корректной работы с PostgreSQL
- alembic - для миграций

### Переменные окружения

```
DB_HOST=localhost

DB_PORT=5432

DB_USER=ishimurasu

DB_PASS=1111

DB_NAME=sa
```


### Конфиг
```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	DB_HOST: str
	DB_PORT: int
	DB_USER: str
	DB_PASS: str
	DB_NAME: str


	@property
	def DATABASE_URL_asyncpg(self):
	# DSN - postgresql+asyncpg://postgres:postgres@localhost:5432/sa
		return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
	
	@property
	def DATABASE_URL_psycopg(self):
	
	# DSN - postgresql+psycopg://postgres:postgres@localhost:5432/sa
		return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
	
	  
	
	model_config = SettingsConfigDict(env_file=".env")

  

settings = Settings()
```

- DATABASE_URL_asyncpg - асинхронная ссылка для алхимии
- DATABASE_URL_psycopg - синхронная ссылка для алхимии
- model_config = SettingsConfigDict(env_file=".env") - конфиг для .env файла

### Создание движка

```python
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from config import settings


# Синхронный движок
sync_engine = create_engine(
	url=settings.DATABASE_URL_psycopg, # Ссылка к БД
	# echo=True, # Логи SQL запросов в консоли
	# pool_size=5, # Количество соединений
	# max_overflow=10, # Максимальное количество дополнительных подключений
)

  
  
# Асинхронный движок
async_engine = create_async_engine(
	url=settings.DATABASE_URL_psycopg, # Ссылка к БД
	# echo=True, # Логи SQL запросов в консоли
	# pool_size=5, # Количество соединений
	# max_overflow=10, # Максимальное количество дополнительных подключений
)

  
# Пример запроса
async def get_test_data():
	async with async_engine.connect() as conn:
	result = await conn.execute(text("SELECT VERSION()")) # Возвращает кортеж.
	# Нужно для того, чтобы в случае большого количества данных они вернулись все. Например: select 1,2,3
	print(result.all()) # Можно использовать first для первого элемента.


asyncio.run(get_test_data())
```


## Создание таблиц (императивный метод) и вставка данных через Core (Query Builder)
### Пример создания таблиц в Core

**Файл models.py**

```python
from sqlalchemy import Table, Column, Integer, String, MetaData


# Метаданные о всех таблицах. Которые созданы на стороне алхимии
metadata_obj = MetaData()

workers_table = Table( # императивный метод
	'workers', # Название таблицы
	metadata_obj, # Метаданные
	Column('id', Integer, primary_key=True), # id, число, первичный ключ
	Column('username', String) # Имя пользователя, строка
)
```

**Файл queries/core.py**
```python
from database import sync_engine
from models import metadata_obj


def create_tables():
	metadata_obj.drop_all(sync_engine) # Удаляет все таблицы из metadata_obj
	metadata_obj.create_all(sync_engine) # Создаёт все таблицы из metadata_obj
```

**Файл main.py**
```python
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from queries.core import create_tables


create_tables()
```


### Базовый пример сырого запроса
**Файл queries/core.py**

```python
from sqlalchemy import text

from database import sync_engine
from models import metadata_obj

def create_tables():
	metadata_obj.drop_all(sync_engine) # Удаляет все таблицы из metadata_obj
	metadata_obj.create_all(sync_engine) # Создаёт все таблицы из metadata_obj
  
def insert_data():
	with sync_engine.connect() as conn:
	# stmt - statment - create, update или delete запрос.
	stmt = text('''
		INSERT INTO workers (username) VALUES
		('AO BOBR'),
		('VOLK');
	''')
	
	conn.execute(stmt) # Выполнение запроса
	conn.commmit() # Отправка данных в БД
	```

**Файл main.py**
```python
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from queries.core import create_tables, insert_data


create_tables()
insert_data()
```

Однако данных запрос можно сделать лучше. Просто переписав его с query builder

```python
def insert_data():
	with sync_engine.connect() as conn:
		stmt = insert(workers_table).values(
			[
				{'username': 'Bobr'},
				{'username': 'Volk'}
			]
		)
		
		conn.execute(stmt)
		conn.commit()
```

Query Builder работает медленнее, однако он более читаемый и понятный. 
Считается более предпочтительным.



## Session и первые шаги в ORM. Создание таблиц в декларативном стиле.
### Сессии
Session - нужна для транзакций. Когда мы входим в сессию мы открываем транзакцию, делаем все необходимые операции. В конце делаем комит или ролбек. Таким образом данные либо попадают, либо не попадают в БД.

Для простоты используется фабрика - sessionmaker. По сути облегчает создание сессий и уменьшает количество кода. Существует также его асинхронный аналог - async_sessionmaker.

```python
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker


session = sessionmaker(sync_engine)
async_session = async_sessionmaker(async_engine)
```

### Таблицы в декларативном стиле (через классы)

Для начала необходимо создать базовый класс. Класс, в котором будут храниться метаданные.

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
	pass
```

Далее этот класс наследуем в моделях. 

```python
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

# Примечание. Очень удобно использовать Mapped. Далее нужно только указывать типы, без импорта классов String, Integer и т.д.

class WorkersORM(Base):
	__tablename__ = 'workers'

	id: Mapped[int] = mapped_column(primary_key=True) # Указываем тип в Mapped 
	# и дополнительные параметры в mapped_column
	username: Mapped[str] # Дополнительные параметры не требуются
	# следовательно не нужен и mapped_column.
```



### Пример вставки данных

```python
def insert_data():
	worker_bobr = WorkersORM(username='Bobr')
	worker_volk = WorkersORM(username='Volk')
	with session() as session:
		# session.add(worker_bobr)
		# session.add(worker_volk)
		session.add_all([worker_bobr, worker_volk]) # Можно передать список
		# напрямую при помощи add_all. Или по очереди как в варианте выше.
		session.commit() # Отправляем данные в БД.


insert_data()
```

Асинхронный вариант

```python
import asyncio


async def insert_data():
	async with async_session_factory() as session:
		# session.add(worker_bobr)
		# session.add(worker_volk)
		worker_bobr = WorkersORM(username='Bobr111')
		worker_volk = WorkersORM(username='Volk111')
		session.add_all([worker_bobr, worker_volk])
		
		await session.commit() # await только здесь. Т.к. данные в БД
		# только тут и создаются

asyncio.run(insert_data())
```


### Пример создания таблиц


```python
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from database import Base, str_200
from sqlalchemy.orm import Mapped, mapped_column
import enum
import datetime
from sqlalchemy import func, text
from typing import Optional, Annotated


# Переиспользуемые типы
intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]
# Автоматическое подставление времени создания. 
# В default - задаются данные на уровне python приложения.
# Вместо этого можно использовать server_default для работы на уровне СУБД.

# Чтобы не путаться в часовых поясах можно приводить к utc (server_default=text("TIMEZONE('utc', now())"))
updated_at = Annotated[datetime.datetime, mapped_column(
	server_default=text("TIMEZONE('utc', now())"),
	onupdate=datetime.datetime.now
)] # Можно реализовать через тригеры в самом sql

  
class WorkersORM(Base):
	__tablename__ = 'workers'
	
	id: Mapped[intpk]
	username: Mapped[str]

  
  

class Workload(enum.Enum):
	parttime = 'parttime'
	fulltime = 'fulltime'

  
  

class ResumeORM(Base):
	__tablename__ = 'resumes'
	
	id: Mapped[intpk]
	title: Mapped[str_200]
	# str_200 объявлен в классе Base
	# = mapped_column(String(256)) # Ограничение
	compensation: Mapped[int | None ]
	#Или Optional[int]. Это можно написать вместо = mapped_column(nullable=True)
	workload: Mapped[Workload]
	worker_id: Mapped[int] = mapped_column(
		ForeignKey('workers.id', ondelete='CASCADE')
	)
	# workers - название таблицы. При удалении работника удаляется у резюме.
	created_at: Mapped[created_at]
	updated_at: Mapped[updated_at]



# Изменённый Base
str_200 = Annotated[str, 200]

class Base(DeclarativeBase):
	type_annotation_map = {
		str_200: String(200)
	}
```





## SELECT и UPDATE запросы через ORM и Core 


### Core

```python

from sqlalchemy import text, insert, select, update
from database import sync_engine
from models import metadata_obj, workers_table


class SyncCore:
	...
	
	@staticmethod
	def select_workers():
		with sync_engine.connect() as conn:
			query = select(workers_table) # SELECT * FROM workers
			result = conn.execute(query)
			workers = result.all() # Все результаты, что вернёт БД
			
	@staticmethod
	def select_workers():
		with session_factory() as session:
			query = select(WorkersOrm)
			result = session.execute(query)
	
	@staticmethod
	def update_worker(worker_id: int = 1, new_username= 'Misha'):
		with sync_engine.connect() as conn:
		#	stmt = text(
		#		'UPDATE workers SET username=:username WHERE id=:id'
		#	)
		
		#	stmt.bindparams(username=new_username, id=worker_id) 
			# Таким образом мы защищаемся от SQL-инъекций при сыром запросе
			stmt = (
				update(workers_table)
				.values(username=new_username)
				.filter_by(id=worker_id)
			)

			conn.execute(stmt)
			
			conn.commit()
```


### ORM
```python
class SyncORM:

  ...
  

	@staticmethod
	def select_workers():
		with session_factory() as session:
			# Для одного работника
			# worker_id = 1
			# worker = session.get(WorkersORM, worker_id)
			
			#Для большего количества
			query = select(WorkersORM)
			result = session.execute(query)
			# workers = result.all() # Кортеж из моделей (1 элемента)
			workers = result.scalars().all() 
			# Выберет первое значение с каждой строки
			
			print(workers)
	
	  
	
	@staticmethod
	def update_worker(worker_id:int=2, new_username:str='Misha'):
		with session_factory() as session:
			worker = session.get(WorkersORM, worker_id)
			worker.username = new_username
			
			# session.add() тут не нужен, только коммит
			session.commit()
	```


**ПРИМЕЧАНИЕ**. При обновлении данных через Core проходит только 1 запрос, в случае с ORM проходят два запроса.

#### flush
**flush -** применяет все изменения в текущей сессии к БД.
Нужен если мы хотим отправить изменения в БД, но ещё не завершить запрос.

```python
@staticmethod
def insert_data():
	with session_factory() as session:
		worker_bobr = WorkersORM(username='Bobr111')
		worker_volk = WorkersORM(username='Volk111')
		
		session.add_all([worker_bobr, worker_volk])
		session.flush() # На этом моменте транзакция ещё не завершена
		session.commit()
```


#### expire и expire_all
**expire** - сбрасывает изменения в конкретном объекте
```python
@staticmethod
def update_worker(worker_id:int=2, new_username:str='Misha'):
	with session_factory() as session:
		worker = session.get(WorkersORM, worker_id)
		worker.username = new_username
		session.expire() # Сбросит все изменения. Операция синхронная
		
		# session.add() тут не нужен, только коммит
		session.commit()
```

**expire_all** - сбрасывает все текущие изменения
```python
@staticmethod
def update_worker(worker_id:int=2, new_username:str='Misha'):
	with session_factory() as session:
		worker = session.get(WorkersORM, worker_id)
		worker.username = new_username
		session.expire_all() # Сбросит все изменения. Операция синхронная
		
		# session.add() тут не нужен, только коммит
		session.commit()
```

#### refresh

**refresh** - возвращает к первоначальным значениям
```python
@staticmethod
def update_worker(worker_id:int=2, new_username:str='Misha'):
	with session_factory() as session:
		worker = session.get(WorkersORM, worker_id)
		worker.username = new_username
		session.refresh(worker) # Сбросит все изменения. Операция синхронная
		
		# session.add() тут не нужен, только коммит
		session.commit()
```


### Примеры более сложных SELECT запросов в ORM

```python
@staticmethod
def select_resumes_avg_compensation(like_language: str = 'Python'):
	'''
	
	SELECT workload, avg(compansation)::int as avg_compansation
	
	FROM resumes
	
	where title like %Python% and compensation > 40000
	
	group by workload
	
	'''
	
	with session_factory() as session:
		query = (
			select(
				ResumeORM.workload,
				cast(func.avg(ResumeORM.compensation), Integer)
				.label('avg_compansation')
			)
			# from писать не обязательно
			.select_from(ResumeORM)
			.filter(and_(
				ResumeORM.title.contains(like_language),
				ResumeORM.compensation > 40000
			))
			.group_by(ResumeORM.workload)
			# Также можно написать и having
			# cast - приводит данные
			#.having(cast(func.avg(ResumeORM.compensation), Integer) > 70000)
		)
		
		# Для красивого вывода запроса в консоли
		# print(query.compile(compile_kwargs={'literal_binds': True}))
		
		result = session.execute(query)
		
		print(result.all())
```


```python
@staticmethod
def join_cte_subquery_window_func(like_language: str = 'Python'):

	'''

	Расчёт зп работника относительно средней зп и загруженности 
	(полная, частичная занятость)
	
	WITH helper2 AS (
	SELECT *, compensation - avg_workload as comp_diff
		FROM (
			SELECT w.id, w.username, r.compansation, r.workload,
			avg(r.compensation) OVER (PARTITION BY workload)::int as avg_workload
			FROM resumes r JOIN workers w ON r.worker_id = w.id
		) helper1
	)
	
	SEECT * FROM helper2
	ORDER BY comp_diff DESC;
	'''

	with session_factory() as session:
		r = aliased(ResumeORM)
		w = aliased(WorkersORM)

		subq = (
		select(
			r,
			w,
			func.avg(
				r.compensation
			).over(partition_by=r.workload).cast(Integer).label('avg_workload')
		)
		# .select_from(r) # Не обязателен
		.join(r,r.worker_id==w.id).subquery('helper1') # inner join
		# .join(full=True) # full join
		# .join(isouter=True) # left join. В алхимии нет right join
		)

		cte = (
			select(
				subq.c.id,
				subq.c.username,
				subq.c.compensation,
				subq.c.workload,
				subq.c.avg_workload,
				(subq.c.compensation - subq.c.avg_workload).label('comp_diff')
			)
			.cte('helper2')
		)

		query = (
			select(cte)
			.order_by(cte.c.comp_diff.desc())
		)

		result = session.execute(query)

		print(result.all())
		```

## Relationship

Relationship - позволяет соединять таблицы между собой.

```python
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from database import Base, str_200
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
import datetime
from sqlalchemy import func, text
from typing import Optional, Annotated


# Переиспользуемые типы
intpk = Annotated[int, mapped_column(primary_key=True)]

created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]

# Автоматическое подставление времени создания. В default - задаются данные на уровне python приложения.

# Вместо этого можно использовать server_default для работы на уровне СУБД.

# Чтобы не путаться в часовых поясах можно приводить к utc (server_default=text("TIMEZONE('utc', now())"))

updated_at = Annotated[datetime.datetime, mapped_column(
	server_default=text("TIMEZONE('utc', now())"),
	onupdate=datetime.datetime.now
)] # Можно реализовать через тригеры в самом sql

  
  

class WorkersORM(Base):
	__tablename__ = 'workers'
	
	id: Mapped[intpk]
	username: Mapped[str]
	# Можно писать и без кавычек, но придётся импортировать.
	# Может привести к проблеме циклических импортов на стороне Python
	resumes: Mapped[list['ResumeOrm']] = relationship(
		back_populates='worker'
	) # Ссылаемся на атрибут resumes в ResumeORM

	resumes_parttime: Mapped[list['ResumeORM']] = relationship(
		back_populates='worker',
		primaryjoin='
		and_(
			WorkersORM.id == ResumeORM.worker_id, 
			ResumeORM.workload == "parttime",
			order_by='ResumesORM.id.desc()', # Сортировка
		)
		'
		# Добавление дополнительных условий для relationship
		# Лучше писать в кавычках, чтобы избежать проблем с импортом в будущем.
	)


class Workload(enum.Enum):
	parttime = 'parttime'
	fulltime = 'fulltime'


class ResumeORM(Base):
	__tablename__ = 'resumes'

	id: Mapped[intpk]	
	title: Mapped[str_200]
	# str_200 объявлен в классе Base
	# = mapped_column(String(256)) # Ограничение
	compensation: Mapped[int | None ]
	#Или Optional[int]. 
	#Это можно написать вместо = mapped_column(nullable=True)
	
	workload: Mapped[Workload]
	
	worker_id: Mapped[int] = mapped_column(
	ForeignKey('workers.id', ondelete='CASCADE'))
	
	# workers - название таблицы. При удалении работника удаляется у резюме.
	created_at: Mapped[created_at]
	updated_at: Mapped[updated_at]
	
	worker: Mapped['WorkersOrm'] = relationship(
		back_populates="resumes"
	) # Ссылаемся на атрибут resumes в WorkersORM


```


### Пример запроса (ленивая подгрузка)
```python

@staticmethod
def select_workers_with_lazy_relationship():
	with session_factory() as session:
		query = (
			select(WorkersORM)
		)
	
	result = session.execute(query)
	res = result.scalars().all()

	worker_1_resumes = res[0].resumes # Запрос
	print(worker_1_resumes)

	worker_2_resumes = res[1].resumes # Запрос
	print(worker_2_resumes)
```

В данном случае количество запросов будет расти с каждым обращением к res мы делаем доп. запрос (проблема n+1).

**!!! НЕЛЬЗЯ ИСПОЛЬЗОВАТЬ С АСИНХРОННЫМ ВАРИАНТОМ !!!**

### Пример запроса с подгрузкой (с joinload)

В данном случае будет один запрос, но сразу со всеми данными. Дополнительного запроса нет.

Чтобы избежать дублирующихся данных -> `res = result.unique().scalars().all()`
(используется unique).

**Подходит для m2o или o2o** 

```python
from sqlalchemy.orm import joinload


@staticmethod
def select_workers_with_joinload_relationship():
	with session_factory() as session:
		query = (
			select(WorkersORM)
			.options(joinedload(WorkersORM.resumes))
		)
	
		result = session.execute(query)
		res = result.unique().scalars().all()

		worker_1_resumes = res[0].resumes
		print(worker_1_resumes)
		
		worker_2_resumes = res[1].resumes
		print(worker_2_resumes)
	```



### Пример запроса с подгрузкой (с selectinload)

```python
from sqlalchemy.orm import selectinload


@staticmethod
def select_workers_with_joinload_relationship():
	with session_factory() as session:
		query = (
			select(WorkersORM)
			.options(selectinload(WorkersORM.resumes))
		)

		result = session.execute(query)
		res = result.unique().scalars().all()
		
		print(res)
```

Происходит два запроса.
1) Выбираем всех работников
2) Выбираем все уникальные резюме.

Больше запросов, но трафика меньше.

**Подходит для o2m или m2m загрузки**

### Оптимизация загрузки с contains_eager

contains_eager - позволяет загружать связанные объекты  вместе с основным объектом, минимизируя количество запросов к БД и улучшая производительность приложения.
**Используя limit можно ограничить количество подгружаемых relationship.**

Пример
```python
@staticmethod
def select_workers_with_relationship_contains_eager_with_limit():

	#https://stackoverflow.com/a/72298903/22259413
	
	with session_factory() as session:
	
		subq = (
			select(ResumesOrm.id.label("parttime_resume_id"))
			.filter(ResumesOrm.worker_id == WorkersOrm.id)
			.order_by(WorkersOrm.id.desc())
			.limit(1)
			.scalar_subquery()
			.correlate(WorkersOrm)
		)

		query = (
			select(WorkersOrm)
			.join(ResumesOrm, ResumesOrm.id.in_(subq))
			.options(contains_eager(WorkersOrm.resumes))
		)

		res = session.execute(query)
		result = res.unique().scalars().all()
		
		print(result)
```

### Индексы и ограничения 

Для создания индекса и ограничения можно использовать `__table_args__` напрямую в модели.
```python
from sqlalchemy import CheckConstraint, Index


class ResumeORM(Base):
	...

	__table_args__ = (
		Index('title_index', "title"),
		CheckConstraint("compensation > 0", name='check_compensation_positive')
	)
```


## Конвертация SQLAlchemy в Pydantic и FastAPI

DTO - Data Transfer Object. Класс, который передаёт данные между различными частями приложения.

В нашем случае pydantic модели

Пример:
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from models import Workload


class WorkersAddDTO(BaseModel):
	username: str


class WorkersDTO(WorkersAddDTO):
	id: int


class ResumesAddDTO(BaseModel):
	title: str
	compensation: Optional[int]
	workload: Workload
	worker_id: int


class ResumesDTO(ResumesAddDTO):
	id: int
	created_at: datetime
	updated_at: datetime


class ResumesRelDTO(ResumesDTO):
	worker: "WorkersDTO"


class WorkersRelDTO(WorkersDTO):
	resumes: list["ResumesDTO"]


class VacanciesAddDTO(BaseModel):
	title: str
	compensation: Optional[int]


class VacanciesDTO(VacanciesAddDTO):=
	id: int


class VacanciesWithoutCompensationDTO(BaseModel):
	id: int
	title: str


class ResumesRelVacanciesRepliedDTO(ResumesDTO):
	worker: "WorkersDTO"
	vacancies_replied: list["VacanciesDTO"]


class ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO(ResumesDTO):
	worker: "WorkersDTO"
	vacancies_replied: list["VacanciesWithoutCompensationDTO"]

```

### Конвертация в Pydantic без relationship 
```python
with session_factory() as session:
	query = (
		select(WorkersOrm)
		.limit(2)
	)
	
	res = session.execute(query)
	result_orm = res.scalars().all()
	print(f"{result_orm=}")
	
	result_dto = [
	WorkersDTO.model_validate(row, from_attributes=True) for row in result_orm
	]
	
	print(f"{result_dto=}")

#result_orm=[<WorkersOrm id=1, username=Jack>, <WorkersOrm id=2, username=Michael>]

#result_dto=[WorkersDTO(username='Jack', id=1), WorkersDTO(username='Michael', id=2)]

```


### Конвертация в Pydantic c relationship 
```python
with session_factory() as session:
	query = (
		select(WorkersOrm)
		.options(selectinload(WorkersOrm.resumes))
		.limit(2)
	)

	res = session.execute(query)
	result_orm = res.scalars().all()
	
	print(f"{result_orm=}")
	
	result_dto = [
		WorkersRelDTO.model_validate(row, from_attributes=True) 
		for row in result_orm
	]
	
	print(f"{result_dto=}")

#result_orm = [<WorkersOrm id=1, username=Jack>, <WorkersOrm id=2, username=Michael>] 

#result_dto = [WorkersRelDTO(username='Jack', id=1, resumes=[ResumesDTO(title='Python Junior Developer', compensation=50000, workload=<Workload.fulltime: 'fulltime'>, worker_id=1, id=1, created_at=datetime.datetime(2023, 10, 29, 10, 41, 12, 770381), updated_at=datetime.datetime(2023, 10, 29, 10, 41, 12, 770381)), ResumesDTO(title='Python Разработчик', compensation=150000, workload=<Workload.fulltime: 'fulltime'>, worker_id=1, id=2, created_at=datetime.datetime(2023, 10, 29, 10, 41, 12, 770381), updated_at=datetime.datetime(2023, 10, 29, 10, 41, 12, 770381))]), WorkersRelDTO(username='Michael', id=2, resumes=[ResumesDTO(title='Python Data Engineer', compensation=250000, workload=<Workload.parttime: 'parttime'>, worker_id=2, id=3, created_at=datetime.datetime(2023, 10, 29, 10, 41, 12, 770381), updated_at=datetime.datetime(2023, 10, 29, 10, 41, 12, 770381)), ResumesDTO(title='Data Scientist', compensation=300000, workload=<Workload.fulltime: 'fulltime'>, worker_id=2, id=4, created_at=datetime.datetime(2023, 10, 29, 10, 41, 12, 770381), updated_at=datetime.datetime(2023, 10, 29, 10, 41, 12, 770381))])]
```


### Конвертация в Pydantic c join

```python

#### pydantic модель
class WorkloadAvgCompensationDTO(BaseModel):
	workload: Workload
	avg_compensation: int
####

with session_factory() as session:

	query = (
		select(
		ResumesOrm.workload,
		func.avg(
		ResumesOrm.compensation
		).cast(Integer).label("avg_compensation"),
	)
	.select_from(ResumesOrm)
	.filter(and_(
		ResumesOrm.title.contains("Python"),
		ResumesOrm.compensation > 40000,
	))
	.group_by(ResumesOrm.workload)
	.having(func.avg(ResumesOrm.compensation) > 70000)
	)
	
	res = session.execute(query)
	result_orm = res.all()
	
	print(f"{result_orm=}")
	
	result_dto = [
		WorkloadAvgCompensationDTO.model_validate(row, from_attributes=True) 
		for row in result_orm
	]
	
	print(f"{result_dto=}")

#result_orm=[(<Workload.parttime: 'parttime'>, 165000), (<Workload.fulltime: 'fulltime'>, 90000)] 

#result_dto=[WorkloadAvgCompensationDTO(workload=<Workload.parttime: 'parttime'>, avg_compensation=165000), WorkloadAvgCompensationDTO(workload=<Workload.fulltime: 'fulltime'>, avg_compensation=90000)]

```

### Интерактивный фронтенд + FastAPI
**Можно нарямую возвращать pydantic модели и обрабатывать их на фронтенде**. Обрабатывать при помощи **jsoneditor**

Пример
```html
<!DOCTYPE HTML>

<html lang="en">
	<head>
		<meta charset="utf-8">

		<link href="https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.10.2/jsoneditor.css" rel="stylesheet" type="text/css">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.10.2/jsoneditor.min.js"></script>
	</head>
	<body>
	
		<div style="display: flex; justify-content: center;">
			<div id="jsoneditor" style="width: 800px; height: 800px;"></div>
		</div>
		
		<script>
			var container = document.getElementById("jsoneditor");
			var editor = new JSONEditor(container);

			async function setJSON () {
				const response = await fetch('http://localhost:8000/resumes');
				const data = await response.json()
				editor.set(data);
			}

			
			function getJSON() {
				var json = editor.get();
				alert(JSON.stringify(json, null, 2));
			}

			document.addEventListener('DOMContentLoaded', function(event) {
				setJSON()
			});
		</script>

	</body>
</html>
```


```python
def create_fastapi_app():
	app = FastAPI(title="FastAPI")
	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
	)

	@app.get("/workers", tags=["Кандидат"])
	async def get_workers():
		workers = SyncORM.convert_workers_to_dto()
		return workers
	
	@app.get("/resumes", tags=["Резюме"])
	async def get_resumes():
		resumes = await AsyncORM.select_resumes_with_all_relationships()
		return resumes
	
	return app
```






## M2M связь в SQLAlchemy

Создаётся связь m2m либо через **table**, либо через класс.

**Пример создания с классом**

```python
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ResumesOrm(Base):
	__tablename__ = "resumes"

	id: Mapped[intpk]
	title: Mapped[str_256]
	compensation: Mapped[Optional[int]]
	workload: Mapped[Workload]
	worker_id: Mapped[int] = mapped_column(
		ForeignKey("workers.id", ondelete="CASCADE")
	)
	created_at: Mapped[created_at]
	updated_at: Mapped[updated_at]

	worker: Mapped["WorkersOrm"] = relationship(
		back_populates="resumes",
	)
	
	vacancies_replied: Mapped[list["VacanciesOrm"]] = relationship(
		back_populates="resumes_replied",
		secondary="vacancies_replies", # Название таблицы 
		# через которую связанны таблицы
	)


class VacanciesOrm(Base):
	__tablename__ = "vacancies"


	id: Mapped[intpk]
	title: Mapped[str_256]
	compensation: Mapped[Optional[int]]
	
	resumes_replied: Mapped[list["ResumesOrm"]] = relationship(
		back_populates="vacancies_replied",
		secondary="vacancies_replies", # Название таблицы 
		# через которую связанны таблицы 
	)


class VacanciesRepliesOrm(Base):
	__tablename__ = "vacancies_replies"
	  
	
	resume_id: Mapped[int] = mapped_column(
		ForeignKey("resumes.id", ondelete="CASCADE"),
		primary_key=True,
	)
	
	vacancy_id: Mapped[int] = mapped_column(
		ForeignKey("vacancies.id", ondelete="CASCADE"),
		primary_key=True,
	)

	cover_letter: Mapped[Optional[str]]
```


**Пример запроса 

```python
@staticmethod
def select_resumes_with_all_relationships():
	with session_factory() as session:
	query = (
		select(ResumesOrm)
		.options(joinedload(ResumesOrm.worker))
		.options(selectinload(ResumesOrm.vacancies_replied)
		.load_only(VacanciesOrm.title))
	)

	res = session.execute(query)
	result_orm = res.unique().scalars().all()
	print(f"{result_orm=}")

	
	result_dto = [ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO.model_validate(row, from_attributes=True) for row in result_orm]
	
	print(f"{result_dto=}")
	
	return result_dto
```

## Alembic + FastAPI

Alembic - библиотека для миграций.

**Пошаговое добавление миграций в проект:**

1. alembic init migrations` - создаст в корне папку migrations. Со всем необходимым. Также создаётся файл alembic.ini
2. Переменные в `alembic.ini`
	1) script_location - путь до папки migrations
	2) prepend_sys_path - область видимости. По дефолту просто точка. Если есть необходимость указать ещё (Например папка migrations в src (для этого использовалась бы команда `alembic init src/migrations` ), то тогда переменная была бы равна prepend_sys_path = .  src)
3. Внутри папки migrations создастся файл `env.py`. В нём и прописываются все конфиги. Необходимые конфиги:
	1) В env.py устанавливаем для config URL БД
	
	```python
 	config.set_main_option('sqlalchemy.url', settings.SYNC_DATABASE_URL)
 	# Для аснихронного варианта 
	config.set_main_option(
	'sqlalchemy.url',
	 settings.ASYNC_DATABASE_URL + "?async_fallback=True"
	)
 	 ```
	2) В env.py устанавливаем `target_metadata` (импортируем Base + какую-то модель ). Комментарий `noqa`  для линтера.
	
```python
from app.db.db import Base

from app.db.models import Vacancy #noqa

target_metadata = Base.metadata
```
Также создаётся файл `script.py.mako` - скрипт на языке мако. По сути и генерирует все миграции. 

Также стоит добавить строчку `compare_server_default=True` в методе `context.configure` функции `run_migrations_online` в файле `migrations/env.py`.
Нужно это для того, чтобы alembic видел изменения в `server_default`.
Обновлённый метод.
```python
context.configure(
	connection=connection,
	target_metadata=target_metadata,
	compare_server_default=True
)
```
4. Создание миграции 
```python
alembic revision --autogenerate -m 'Инициализировал обновлённую БД'
# -m 'Инициализировал обновлённую БД' - этот коммент не обязателен
```
После в migrations/versions появляется файл миграции.
5. Далее накатываем все миграции в бд
```python
alembic upgrade head 
# Вместо head можно указать номер миграции, чтобы не накатывать все
```
6.  Далее при изменении каких-либо данных создаём миграцию пункт 4 и пункт 5.

**Дополнительно**.
Для того, чтобы откатить БД назад используется команда
```python
alembic downgrade 'номер миграции'
```
Чтобы полностью откатить все миграции

```python 
alembic downgrade base
```

Для красивого форматирования миграций можно задать форматировщика. Например `black`. Для этого нужно просто раскомментировать строки ниже в файле `alembic.ini`
```python
hooks = black
black.type = console_scripts
black.entrypoint = black
black.options = -l 79 REVISION_SCRIPT_FILENAME
```
## Дополнительно

**Для красивых логов sql запросов**
```python
class Base(DeclarativeBase):
	repr_cols_num = 3
	repr_cols = tuple()

	def __repr__(self):
	"""
		Relationships не используются в repr(), 
		т.к. могут вести к неожиданным подгрузкам
		"""
		
		cols = []
		for idx, col in enumerate(self.__table__.columns.keys()):
			if col in self.repr_cols or idx < self.repr_cols_num:
				cols.append(f"{col}={getattr(self, col)}")
		
		return f"<{self.__class__.__name__} {', '.join(cols)}>"
```
