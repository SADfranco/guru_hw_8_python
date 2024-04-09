"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product
from models import Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():
    return Cart()

class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(0)
        assert product.check_quantity(999)
        assert product.check_quantity(1000)
        assert product.check_quantity(1001) == False


    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        assert product.buy(0) == product.quantity
        assert product.buy(999) == product.quantity


    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии

        with pytest.raises(ValueError):
            product.buy(1001)



class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_cart_add_product(self, product, cart):
        # TODO проверка на добавление товара в корзину
        cart.add_product(product)
        assert cart.products[product] == 1

        cart.add_product(product, 10)
        assert cart.products[product] == 11

        cart.add_product(product, 0)
        assert cart.products[product] == 0


    def test_cart_remove_product_from(self, cart, product):
        # TODO проверка на удаление товаров из корзины
        cart.add_product(product, 10)
        cart.remove_product(product, 5)
        assert cart.products[product] == 5

        cart.add_product(product, 5)
        cart.remove_product(product, 10)
        assert product not in cart.products

        cart.add_product(product, 2)
        cart.remove_product(product)
        assert product not in cart.products

        cart.add_product(product,0)
        cart.remove_product(product, 0)
        assert product not in cart.products

    def test_cart_clear(self, product, cart):
        # TODO проверка полной очистки корзины
        cart.add_product(product, 5)
        cart.clear()
        assert product not in cart.products

        cart.add_product(product, 0)
        cart.clear()
        assert product not in cart.products

    def test_cart_get_total_price(self, product, cart):
        # TODO проверка полной стоимости товара в корзине
        cart.add_product(product, 10)
        assert cart.get_total_price() == 1000

        cart.remove_product(product, 10)
        assert cart.get_total_price() == 0

        cart.add_product(product, 10)
        cart.clear()
        assert cart.get_total_price() == 0

        cart.add_product(product, 0)
        assert cart.get_total_price() == 0

    def test_cart_buy(self, product, cart):
        # TODO проверка остатка товара после покупки
        cart.add_product(product, 999)
        cart.buy()
        assert product.check_quantity(1)

        product.quantity = 1000
        cart.add_product(product, 1000)
        cart.buy()
        assert product.check_quantity(0)

        product.quantity = 1000
        cart.add_product(product, 0)
        cart.buy()
        assert product.check_quantity(1000)

        product.quantity = 1000
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            cart.buy()

