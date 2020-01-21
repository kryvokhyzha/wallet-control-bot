from typing import Dict, List, NamedTuple

from app.utils.config import DB_CATEGORY_COLLECTION_NAME

import app.db as db


class Category(Dict):
    """
        Category structure
    """
    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


class Categories:
    async def _init(self):
        self._categories = await self._load_categories()

    async def _load_categories(self) -> List[Category]:
        """Возвращает справочник категорий расходов из БД"""
        categories = await db.fetchall(DB_CATEGORY_COLLECTION_NAME)
        categories = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories: List[Dict]) -> List[Category]:
        """Заполняет по каждой категории aliases, то есть возможные
        названия этой категории, которые можем писать в тексте сообщения.
        Например, категория «кафе» может быть написана как cafe,
        ресторан и тд."""
        categories_result = []
        for category in categories:
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(Category(
                codename=category['codename'],
                name=category['name'],
                is_base_expense=category['is_base_expense'],
                aliases=aliases
            ))

        return categories_result

    def get_all_categories(self) -> List[Dict]:
        """Возвращает справочник категорий."""
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """Возвращает категорию по одному из её алиасов."""
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded
