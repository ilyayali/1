from typing import Generator

import requests

__base_url_for_get_products = "https://catalog.wb.ru/catalog/{shard}/v2/catalog?ab_testing=false&appType=1&cat={id_category}&curr=rub&dest=123585825"
__url_product = "https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=123585825&spp=30&ab_testing=false&nm={id_product}"


def get_catalogs_wb() -> list:
    """
    Функция получения всего каталога WB
    :return:
    """
    url = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json"
    response = requests.get(url)
    data = response.json()
    data_list = []
    for d in data:
        try:
            for child in d["childs"]:
                try:
                    category_name = child["name"]
                    category_url = child["url"]
                    shard = child["shard"]
                    query = child["query"]
                    id_category = child["id"]
                    data_list.append(
                        {
                            "category_name": category_name,
                            "category_url": category_url,
                            "shard": shard,
                            "query": query,
                            "id_category": id_category,
                        }
                    )
                except Exception:
                    continue
                try:
                    for sub_child in child["childs"]:
                        category_name = sub_child["name"]
                        category_url = sub_child["url"]
                        shard = sub_child["shard"]
                        query = sub_child["query"]
                        id_category = sub_child["id"]
                        data_list.append(
                            {
                                "category_name": category_name,
                                "category_url": category_url,
                                "shard": shard,
                                "query": query,
                                "id_category": id_category,
                            }
                        )
                except Exception:
                    continue
        except Exception:
            continue
    return data_list


def get_categorise() -> dict:
    """
    Функция получения всех категорий из каталога WB
    :return: dict('category_name': ['child_category_name',], )
    """
    url = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json"
    response = requests.get(url)
    data = response.json()
    category_dict = {}
    for d in data:
        try:
            sub_category_name = [sub_cat['name'] for sub_cat in d["childs"]]
            category_dict[d["name"]] = sub_category_name
        except KeyError:
            continue
    return category_dict

def search_category_in_catalog(url: str, catalog_list: list):
    try:
        for catalog in catalog_list:
            if catalog["category_url"] == url.split("https://www.wildberries.ru")[-1]:
                print(f'Найдено совпадение {catalog["category_name"]}')
                name_category = catalog["category_name"]
                shard = catalog["shard"]
                query = catalog["query"]
                id_category = catalog["id_category"]
                return name_category, shard, query, id_category
            else:
                pass
    except Exception:
        print("Не найдено совпадение")


def get_product_wb() -> Generator[int, dict, None]:
    """
    Функция генератор возвращает список всех id всех товаров
    :return: Generator[int, dict, None]
    """
    data_list = get_catalogs_wb()
    for data in data_list:
        response = requests.get(
            __base_url_for_get_products.format(
                shard=data["shard"], id_category=data["id_category"]
            )
        )
        if response.status_code == 200:
            try:
                data_products = response.json()
                for i in data_products["data"]["products"]:
                    yield i["id"], data
            except requests.exceptions.JSONDecodeError:
                print("Invalid JSON received")
                continue


def get_feedbackPoints_and_total_price() -> Generator[int, float, int | dict]:
    """
    Функция генератор возвращает словарь из стоимости товара, его id, кэшбэка и вложеного словаря с данными по каталогу
    :return: Generator{int, int, int, dict}
    """
    for id in get_product_wb():
        try:
            response = requests.get(__url_product.format(id_product=id[0]))
            data_product = response.json()
            yield {
                "id_product": data_product["data"]["products"][0]["id"],
                "total_price": data_product["data"]["products"][0]["sizes"][0]["price"][
                    "total"
                ]
                / 100,
                "cash_back": data_product["data"]["products"][0]["feedbackPoints"],
                "catalog": id[1],
            }
        except KeyError:
            continue


if __name__ == "__main__":
    print(get_categorise())
