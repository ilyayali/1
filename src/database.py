import asyncio
import sqlite3


class Database:
    """Класс подключения и работы с БД"""

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    async def __aenter__(self) -> None:
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.connection:
            self.connection.commit()
            self.connection.close()

    async def create_table(self) -> None:
        """Функция создания таблицы"""
        # Удаляем таблицу, если она уже существует
        self.cursor.execute("DROP TABLE IF EXISTS products_wb")

        self.cursor.execute(
            """
        CREATE TABLE products_wb (
        id_product INTEGER,
        total_price REAL,
        cash_back INTEGER,
        category_name TEXT,
        category_url TEXT,
        shard TEXT,
        query TEXT,
        id_category INTEGER
        ) """
        )
        self.connection.commit()

    async def insert_product(self, product: dict) -> None:
        """Функция добавления товара в БД"""
        self.cursor.execute(
            f"""
        INSERT INTO products_wb (id_product, total_price, cash_back, category_name, category_url, shard, query, id_category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                product["id_product"],
                product["total_price"],
                product["cash_back"],
                product["catalog"]["category_name"],
                product["catalog"]["category_url"],
                product["catalog"]["shard"],
                product["catalog"]["query"],
                product["catalog"]["id_category"],
            ),
        )
        self.connection.commit()

    async def filter_product(self, category_name: str) -> tuple:
        """Функция фильтрации товаров по категории"""
        self.cursor.execute(
            f"""
        SELECT * FROM products_wb WHERE category_name =?""",
            (category_name,),
        )
        products = self.cursor.fetchall()
        return products
