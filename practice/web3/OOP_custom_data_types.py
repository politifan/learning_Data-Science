from typing import TypedDict
from time import time

print(time())

class Transaction(TypedDict):
    amount: int
    sender: str
    recipient: str
    timestamp: float

class Transactions(TypedDict):
    transactions: Transaction

class Block(TypedDict):
    block_number: int
    transactions: Transactions


A = {"block_number":1234,"transactions":{"transaction":{"amount":500,
                                                    "sender":"user1",
                                                    "recipient":"user2",
                                                    "timestamp":time()
                                                    }
                                    }
    } # Проблема с тем, что мы не гарантируем какой ключ и значение (их типы)

class custom(TypedDict):
    hello:str
    int_data:int

result = custom(A)

print(result)


### Разбор typing


python.py
from typing import List, Dict, Union

matrix_data: List[float] = [1.5, 2.5, 3.5]
slovar: Dict[str, int] = {'Иван': 25, 'Петр': 30}

stock_prices: Dict[str, list[int]] = {'Apple': [150, 155, 148]}

def process_age(age: int | str):
    print(f'Обработка возраста: {age}')


# Any 
# Tuple - это как список, но его нельзя заменить
# В web3 кортежи постоянно используются для передачи неизменяемых пар данных
# например: Публичный_ключ, Приватный_ключ, Имя_токена, баланс
#  

from typing import Tuple

# Кортеж строго из двух элементов: первый — строка (str), второй — число (int)
wallet_info: Tuple[str, int] = ('Bitcoin_Wallet_Address', 2)
# ЛИБО tuple - с маленькой буквы
# В Python 3.9+ можно писать проще, с маленькой буквы:
# wallet_info: tuple[str, int] = ("Bitcoin_Wallet_Address", 2)

def convert_currency(crypto: Tuple[str, int], rate: float) -> float:
    coin_count = crypto[1]
    return coin_count * rate


#Literal - для безопасности транзакций в Web3
#send(отправить монеты другому человеку), receive(получить монеты), 
# stake(положить монеты под процент)
from typing import Literal
# Мы жестко говорим: аргумент action может быть ТОЛЬКО одной из этих трех строк
def create_transaction(amount: float, action: Literal['send', 'receive', 'stake']):
    print(f'Выполняется действие: {action} на сумму {amount} BTC')
def manage_wallet(status: Literal['active', 'frozen'], balance: int | float):
    print(f'{status}, {balance}')

# Пройдены: 
# List[тип] - для списков( массивы транзакций, цены)
# Dict[тип_ключа, тип_значения] - для словарей (базы данных пользователей, балансы кошелька)
# Tuple[тип1, тип2] - для неизменяемых связок данных(адрес + балнс, логин + пароль) 
# Union[тип1, тип2] или (или тип1 | тип2) - когда тип может быть разным (число или строка, целое или дробное) 
# Optional[тип] (или тип | None) - когда данные могут отсутствовать 
# Literal["значение1", "значение2"] - жесткое ограничение строк или чисел конкретным списком



"СИСТЕМА МОНИТОРИНГА СМАРТ-КОНТРАКТА"

### Пишем бэк для отслеживания транзакций в блокчейне
# Сначала создаем функцию, в ней сначала принимаем список транзакций и статус сети
# Затем выводим информацию
def process_blockchain_data(transactions: list[dict[str, str|int]], network_status: Literal['online', 'offline', 'maintenance']) -> None:
    print(f'Статус сети {network_status}, транзакция {transactions}')

Callable
from typing import Callable

# 1. У нас есть обычная функция, которая переводит рубли в доллары
# Она принимает float и возвращает float
def usd_converter(rub: float) -> float:
    return rub / 80.0

# 2. А теперь пишем функцию, которая ПРИНИМАЕТ этот конвертер как аргумент
# Обрати внимание на аннотацию: Callable[[float], float]
# Это значит: "Сюда нужно передать функцию, которая берет float и возвращает float"
def print_converted_price(price: float, converter: Callable[[float], float]) -> None:
    result = converter(price)
    print(f"Цена в долларах: {result}")

# 3. Вызываем её, передавая саму функцию usd_converter БЕЗ круглых скобок!
print_converted_price(8000.0, usd_converter)

from typing import Callable

def secure_payment(amount: int, check_function: Callable[[int], str]) -> None:
    status = check_function(amount)
    print(f'Результат проверки транзакции: {status}')


#
