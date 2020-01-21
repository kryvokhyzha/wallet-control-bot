import app.db as db

from app.models.category import Categories


async def get_categories_list():
    categories = Categories()
    await categories._init()
    categories = categories.get_all_categories()

    answer_message = "Категории трат:\n\n* " +\
            ("\n* ".join([c['name']+' ('+", ".join(c['aliases'])+')' for c in categories]))

    return answer_message
