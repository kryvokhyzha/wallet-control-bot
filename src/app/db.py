from typing import Dict, List, Tuple, Union, Optional
from app.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from app.utils.config import DB_USER_COLLECTION_NAME, DB_CATEGORY_COLLECTION_NAME
from app.utils.constants import INIT_CATEGORY

from app.models.user import User
from app.models.expense import Expense

from motor.motor_asyncio import AsyncIOMotorClient


uri = "mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}" + \
      "?retryWrites=false"
uri = uri.format(DB_USER=DB_USER, DB_PASSWORD=DB_PASSWORD,
                 DB_HOST=DB_HOST, DB_NAME=DB_NAME)

print('Connection to MongoDB...')
client = AsyncIOMotorClient(uri)
print('Connection success!')

db = client.get_database(DB_NAME)


async def do_insert_one(collection_name: str, document: Union[User, Expense, Dict]):
    collection = db.get_collection(collection_name)
    await collection.insert_one(document)


async def do_insert_many(collection_name: str, documents: List[Union[User, Expense, Dict]]):
    collection = db.get_collection(collection_name)
    await collection.insert_many(documents)


async def do_find_one(collection_name: str, document: Union[User, Expense, Dict]) -> Optional[Dict]:
    collection = db.get_collection(collection_name)
    return await collection.find_one(document)


async def do_find(collection_name: str, document: Union[User, Expense, Dict]) -> List[Dict]:
    collection = db.get_collection(collection_name)
    result = []
    async for item in collection.find(document):
        result.append(item)
    return result


async def compute_sum(collection_name: str, field_name:str, document: Union[User, Expense, Dict]) -> List[Dict]:
    collection = db.get_collection(collection_name)
    summa = 0
    async for item in collection.find(document):
        summa += item[field_name]
    return summa


async def do_update(collection_name: str, document: Union[User, Expense, Dict]):
    collection = db.get_collection(collection_name)

    old_user = await do_find_one(collection_name, {'id': document['id']})
    _id = old_user['_id']

    await collection.replace_one({'_id': _id}, document)


async def fetchall(collection_name: str) -> List[Dict]:
    collection = db.get_collection(collection_name)
    result = []
    async for document in collection.find({}):
        result.append(document)
    return result


async def check_db_exists(*args, **kwargs):
    collist = await db.list_collection_names()
    categories = await do_find(DB_CATEGORY_COLLECTION_NAME, {})

    if DB_CATEGORY_COLLECTION_NAME not in collist or not categories:
        await _init_categories()


async def _init_categories():
    await do_insert_many(DB_CATEGORY_COLLECTION_NAME, INIT_CATEGORY)
