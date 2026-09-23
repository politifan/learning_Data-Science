def test(a,b):
    return a,b

test(1,2)

class Fruit():
    weight = 0
    def __init__(self,weight):
        weight = weight # kg
    def eat():...

#class Fruit():
#    def __init__(self,weight:float):
#        self.weight = weight # kg
#    def eat(self):
#        self.weight = 0

Fruit(5.5)

class Apple(Fruit): ...

apple1 = Apple(2.54)
apple2 = Apple(2.54)
apple1.eat()
#print(apple2.weight, apple1.weight)


# Класс, метод, функция, декоратор, свойства, собственные значения 
# Класс - шаблон, содержащий методы, свойства и собственные значения
# Метод - функция, доступная только внутри класса
# Функция - своя команда, которая принимает данные и возвращает на выходе новые данные
# Свойства - значения/переменные, принадлежащие классу
# Экземпляр класса - инициализированный класс со своими значениями
# Собственные значения - значения, которые задаются при создании экзмепляра класса
# Полиморфизм - перенос свойств одного класса в другой




# Как оформлять код:
# 1) сначала import (1. встроенные библиотеки (built-in) 2. Сторонние (third-part) 3. Свои собственные классы, функции и константы
# 2) Свои собственные константы только в текущем файле
# 3) Вспомогательные функции (их название начинается с одного "_") + Базовые классы
# Базовые классы - классы для полиморфизма
# 4) Главные функции (те, что используются в самом файле или) и классы
# 5) (Опциональный)) if __name__ == "__main__": - проверка - запускается ли файл на прямую

mail = "roman@mail.ru"

def validate_email(mail_address:str) -> bool:
    two_parts = mail_address.split("@")

    if len(two_parts) != 2:
        raise ValueError
    
    # first_check, second_check = False, False
    
    first_check = False
    second_check = False

    if all(i.isalpha() for i in two_parts[0]):
        first_check = True
    if "." in two_parts[1]:
        second_check = True

    return first_check and second_check

def _validate_first_part(first_part:str) -> bool:
    return all(i.isalpha() for i in first_part)

def _validate_second_part(second_part:str) -> bool:
    return "." in second_part


def validate_email(mail_address:str) -> bool:
    """Function that validates simple email address

    Args:
        mail_address (str): mail address

    Raises:
        ValueError: If there is not one "@" symbol in email address

    Returns:
        bool: True if pass else False
    """
    two_parts = mail_address.split("@")

    if len(two_parts) != 2: raise ValueError

    first, second = two_parts

    first_check = _validate_first_part(first)
    second_check = _validate_second_part(second)

    return first_check and second_check
    
    



from math import pi
PI = 3.14
print(pi)
# 