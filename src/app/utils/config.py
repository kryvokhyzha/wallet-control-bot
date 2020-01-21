import os


DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '')
DB_NAME = os.getenv('DB_NAME', '')
DB_USER_COLLECTION_NAME = os.getenv('DB_USER_COLLECTION_NAME', 'users')
DB_CATEGORY_COLLECTION_NAME = os.getenv('DB_CATEGORY_COLLECTION_NAME', 'categories')
DB_EXPENSES_COLLECTION_NAME = os.getenv('DB_EXPENSES_COLLECTION_NAME', 'expenses')
