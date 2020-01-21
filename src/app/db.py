from typing import Dict, List, Tuple
from app.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_USER_COLLECTION_NAME

from motor.motor_asyncio import AsyncIOMotorClient


uri = "mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}" + \
      "?retryWrites=false"
uri = uri.format(DB_USER=DB_USER, DB_PASSWORD=DB_PASSWORD,
                 DB_HOST=DB_HOST, DB_NAME=DB_NAME)

print('Connection to MongoDB...')
client = AsyncIOMotorClient(uri)
print('Connection success!')

db = client.get_database(DB_NAME)
collection = db.get_collection(DB_USER_COLLECTION_NAME)

async def do_insert(document: Dict):
    await collection.insert_one(document)


async def do_find_one(document: Dict):
    return await collection.find_one(document)


async def do_update(document: Dict):
    old_user = await do_find_one({'id': document['id']})
    _id = old_user['_id']

    await collection.replace_one({'_id': _id}, document)


def insert(table: str, column_values: Dict):
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open(os.path.join("app", "createdb.sql"), "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='expense'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

# check_db_exists()
