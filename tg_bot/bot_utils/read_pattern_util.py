from api_site.utils.product_obj import Product


def read_pattern(any_product: Product) -> str:
    """
    Функция принимает объект со строковыми атрибутами и формирует паттерн для вывода результата на экран пользователю.
    Args:
        any_product: Product - объект товара.

    Returns:
        str: Описание товара.
    """
    pattern: str = (f"Название:  {any_product.get_product_title()}\n"
                    f"Рейтинг: {any_product.get_product_rating()}\n"
                    f"О товаре: {any_product.get_product_description()}\n"
                    f"Атрибуты: {any_product.get_product_attributes()}\n"
                    f"Цена: {any_product.get_price()} руб.\n"
                    f"Название магазина: {any_product.get_store_name()}\n"
                    f"Доставка: {any_product.get_shipping()}\n"
                    )
    if len(pattern) < 900:
        return pattern
    else:
        pattern: str = (f"Название:  {any_product.get_product_title()}\n"
                        f"Рейтинг: {any_product.get_product_rating()}\n"
                        f"О товаре: {any_product.get_product_description()}\n"
                        f"Цена: {any_product.get_price()} руб.\n"
                        f"Название магазина: {any_product.get_store_name()}\n"
                        f"Доставка: {any_product.get_shipping()}\n"
                        )
        if len(pattern) < 900:
            return pattern

        pattern: str = (f"Название:  {any_product.get_product_title()}\n"
                        f"Рейтинг: {any_product.get_product_rating()}\n"
                        f"Атрибуты: {any_product.get_product_attributes()}\n"
                        f"Цена: {any_product.get_price()} руб.\n"
                        f"Название магазина: {any_product.get_store_name()}\n"
                        f"Доставка: {any_product.get_shipping()}\n")

        if len(pattern) < 900:
            return pattern

        else:
            pattern: str = (f"Название:  {any_product.get_product_title()}\n"
                            f"Рейтинг: {any_product.get_product_rating()}\n"
                            f"Цена: {any_product.get_price()} руб.\n"
                            f"Название магазина: {any_product.get_store_name()}\n"
                            f"Доставка: {any_product.get_shipping()}\n"
                            )
            return pattern
