import os


DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '')
DB_NAME = os.getenv('DB_NAME', '')
DB_USER_COLLECTION_NAME = os.getenv('DB_USER_COLLECTION_NAME', 'users')
DB_CATEGORY_COLLECTION_NAME = os.getenv('DB_CATEGORY_COLLECTION_NAME', 'categories')
DB_EXPENSES_COLLECTION_NAME = os.getenv('DB_EXPENSES_COLLECTION_NAME', 'expenses')
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', '')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', '')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', '3001')
DEVELOP = os.getenv('DEVELOP', 'True')
