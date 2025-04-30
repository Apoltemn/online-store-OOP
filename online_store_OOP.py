from abc import ABC, abstractmethod
from datetime import datetime
import sys

# Базовые классы
class Product(ABC):
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
    
    @abstractmethod
    def display_info(self):
        pass

    def __str__(self):
        return f"{self.name} - {self.price} руб."

class Electronics(Product):
    def __init__(self, name, price, warranty_period):
        super().__init__(name, price, "Электроника")
        self.warranty_period = warranty_period
    
    def display_info(self):
        return f"{self.name} - {self.price} руб. (Гарантия: {self.warranty_period} мес.)"

class Clothing(Product):
    def __init__(self, name, price, size):
        super().__init__(name, price, "Одежда")
        self.size = size
    
    def display_info(self):
        return f"{self.name} - {self.price} руб. (Размер: {self.size})"

class Book(Product):
    def __init__(self, name, price, author):
        super().__init__(name, price, "Книги")
        self.author = author
    
    def display_info(self):
        return f"{self.name} - {self.author} - {self.price} руб."

# Исключения
class InsufficientFundsException(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Недостаточно средств. На счету: {balance}, требуется: {amount}")

class InvalidInputException(Exception):
    pass

# Класс пользователя
class User:
    def __init__(self, name, balance=0):
        self.name = name
        self.__balance = balance
        self.cart = []
        self.purchase_history = []
    
    @property
    def balance(self):
        return self.__balance
    
    def add_funds(self, amount):
        if amount <= 0:
            raise InvalidInputException("Сумма пополнения должна быть положительной")
        self.__balance += amount
        return f"Счет пополнен на {amount} руб. Новый баланс: {self.__balance} руб."
    
    def add_to_cart(self, product):
        self.cart.append(product)
        return f"{product.name} добавлен в корзину"
    
    def remove_from_cart(self, product_index):
        if 0 <= product_index < len(self.cart):
            return self.cart.pop(product_index)
        raise InvalidInputException("Неверный индекс товара")
    
    def checkout(self):
        total = sum(product.price for product in self.cart)
        if total > self.__balance:
            raise InsufficientFundsException(self.__balance, total)
        
        self.__balance -= total
        purchase = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'products': self.cart.copy(),
            'total': total
        }
        self.purchase_history.append(purchase)
        self.cart.clear()
        return f"Покупка на сумму {total} руб. оформлена. Остаток: {self.__balance} руб."

# Класс магазина
class Store:
    def __init__(self):
        self.categories = {
            "Электроника": [
                Electronics("Смартфон", 25000, 12),
                Electronics("Ноутбук", 65000, 24),
                Electronics("Наушники", 5000, 6)
            ],
            "Одежда": [
                Clothing("Футболка", 1500, "L"),
                Clothing("Джинсы", 3000, "M"),
                Clothing("Куртка", 8000, "XL")
            ],
            "Книги": [
                Book("Python для начинающих", 1200, "Иван Иванов"),
                Book("Паттерны проектирования", 2500, "Петр Петров"),
                Book("Искусство программирования", 3500, "Дональд Кнут")
            ]
        }
    
    def get_products_by_category(self, category_name):
        return self.categories.get(category_name, [])

# Главное меню
def main():
    store = Store()
    user = User("Алексей", 10000)
    
    while True:
        print("\n=== Главное меню ===")
        print("1. Посмотреть категории")
        print("2. Перейти в корзину")
        print("3. Перейти в историю покупок")
        print("4. Посмотреть счет")
        print("5. Выход")
        
        try:
            choice = input("Выберите действие: ")
            
            if choice == "1":
                # Просмотр категорий
                print("\nКатегории товаров:")
                for i, category in enumerate(store.categories.keys(), 1):
                    print(f"{i}. {category}")
                
                cat_choice = input("Выберите категорию (0 - назад): ")
                if cat_choice == "0":
                    continue
                
                try:
                    cat_index = int(cat_choice) - 1
                    category_name = list(store.categories.keys())[cat_index]
                    products = store.get_products_by_category(category_name)
                    
                    print(f"\nТовары в категории '{category_name}':")
                    for i, product in enumerate(products, 1):
                        print(f"{i}. {product.display_info()}")
                    
                    prod_choice = input("Выберите товар для добавления в корзину (0 - назад): ")
                    if prod_choice == "0":
                        continue
                    
                    try:
                        prod_index = int(prod_choice) - 1
                        selected_product = products[prod_index]
                        print(user.add_to_cart(selected_product))
                    except (ValueError, IndexError):
                        print("Ошибка: неверный номер товара")
                
                except (ValueError, IndexError):
                    print("Ошибка: неверный номер категории")
            
            elif choice == "2":
                # Корзина
                if not user.cart:
                    print("Корзина пуста")
                    continue
                
                print("\n=== Ваша корзина ===")
                total = 0
                for i, product in enumerate(user.cart, 1):
                    print(f"{i}. {product.display_info()}")
                    total += product.price
                print(f"\nОбщая сумма: {total} руб.")
                print(f"Баланс: {user.balance} руб.")
                
                print("\n1. Оформить покупку")
                print("2. Удалить товар")
                print("3. Назад")
                
                cart_choice = input("Выберите действие: ")
                
                if cart_choice == "1":
                    try:
                        print(user.checkout())
                    except InsufficientFundsException as e:
                        print(f"Ошибка: {e}")
                elif cart_choice == "2":
                    try:
                        remove_index = int(input("Введите номер товара для удаления: ")) - 1
                        removed = user.remove_from_cart(remove_index)
                        print(f"{removed.name} удален из корзины")
                    except (ValueError, IndexError, InvalidInputException):
                        print("Ошибка: неверный номер товара")
            
            elif choice == "3":
                # История покупок
                if not user.purchase_history:
                    print("История покупок пуста")
                    continue
                
                print("\n=== История покупок ===")
                for i, purchase in enumerate(user.purchase_history, 1):
                    print(f"\nПокупка #{i} ({purchase['date']})")
                    for product in purchase['products']:
                        print(f"- {product.display_info()}")
                    print(f"Итого: {purchase['total']} руб.")
            
            elif choice == "4":
                # Счет
                print(f"\nТекущий баланс: {user.balance} руб.")
                add_funds = input("Введите сумму для пополнения (0 - отмена): ")
                if add_funds != "0":
                    try:
                        amount = int(add_funds)
                        print(user.add_funds(amount))
                    except (ValueError, InvalidInputException):
                        print("Ошибка: введите положительное число")
            
            elif choice == "5":
                print("До свидания!")
                sys.exit()
            
            else:
                print("Неверный ввод. Попробуйте еще раз.")
        
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()