from typing import Dict, List, Tuple
from app.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_USER_COLLECTION_NAME, DB_CATEGORY_COLLECTION_NAME
from app.utils.constants import INIT_CATEGORY

from motor.motor_asyncio import AsyncIOMotorClient


uri = "mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}" + \
      "?retryWrites=false"
uri = uri.format(DB_USER=DB_USER, DB_PASSWORD=DB_PASSWORD,
                 DB_HOST=DB_HOST, DB_NAME=DB_NAME)

print('Connection to MongoDB...')
client = AsyncIOMotorClient(uri)
print('Connection success!')

db = client.get_database(DB_NAME)
user_collection = db.get_collection(DB_USER_COLLECTION_NAME)


async def do_insert(document: Dict, collection=user_collection):
    await collection.insert_one(document)


async def do_insert_many(documents: List, collection=user_collection):
    await collection.insert_many(documents)


async def do_find_one(document: Dict, collection=user_collection):
    return await collection.find_one(document)


async def do_update(document: Dict, collection=user_collection):
    old_user = await do_find_one({'id': document['id']})
    _id = old_user['_id']

    await collection.replace_one({'_id': _id}, document)


async def check_db_exists(*args, **kwargs):
    collist = await db.list_collection_names()
    
    if DB_CATEGORY_COLLECTION_NAME not in collist:
        await _init_categories()


async def _init_categories():
    category_coll = db[DB_CATEGORY_COLLECTION_NAME]
    await do_insert_many(INIT_CATEGORY, collection=category_coll)


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

# check_db_exists()
