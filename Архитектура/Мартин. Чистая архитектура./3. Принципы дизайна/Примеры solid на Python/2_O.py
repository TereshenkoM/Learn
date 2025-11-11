#O — Open/Closed Principle (Принцип открытости/закрытости)
#Классы должны быть открыты для расширения, но закрыты для изменения


#Плохой пример. Если добавится новый тип клиента — придётся править код.

class Discount:
    def __init__(self, customer_type):
        self.customer_type = customer_type

    def get_discount(self, price):
        if self.customer_type == "vip":
            return price * 0.8
        elif self.customer_type == "regular":
            return price * 0.9
        else:
            return price

# Хороший пример. Добавить новый тип скидки можно просто создав новый класс.
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        pass

class RegularDiscount(DiscountStrategy):
    def apply(self, price):
        return price * 0.9

class VIPDiscount(DiscountStrategy):
    def apply(self, price):
        return price * 0.8

class PriceCalculator:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def calculate(self, price):
        return self.strategy.apply(price)
