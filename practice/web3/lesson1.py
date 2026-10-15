###

# Install options for code:

#  Loading libraries: 'os', 'dotenv', 'time', 'web3', 'logger' 

###

from os import getenv # получить переменную из .env файла окружения
from dotenv import load_dotenv # загрузка окружения в данной папке (окружение - .env файл)
import logging # библиотека для красивого вывода данных с форматированием
from time import sleep

from web3 import Web3, HTTPProvider # Библиотека для работы с криптовалютой

from logger import setup_logging # Наша собственная библиотека 
from OOP_custom_data_types import Transaction

###

# Configuring logging

###

logger = setup_logging(logging.DEBUG)

# Загружаем переменные из .env | Load environment variables from .env

load_dotenv()

###

# Получаем настройки подключения и лимит | Get connection settings and the limit

###

API_KEY = getenv("API_KEY")
LIMIT = int(getenv("LIMIT"))

provider = Web3(HTTPProvider(API_KEY))

# logger.debug(provider.eth.block_number) # DEBUG - для отладки (информация, нужная только разрабу для своих тестов)
# logger.info(provider.eth.block_number) # INFO - Обычная информация о том что происходит
# logger.warning(provider.eth.block_number) # WARNING - Так быть не должно, но это ничего не ломает. Но исправить надо
# logger.error(provider.eth.block_number) # ERROR - полноценный баг. Так быть явно не должно и надо фиксить
# logger.critical(provider.eth.block_number) # CRITICAL - сценарий СИЛЬНО влияющий на проект явно в плохую сторону


# Задача: Мы должны в живом времени сканировать N блоков 
# и собирать с них все транзакции + расшифровывать их

class BlockchainScanner:
    """
    Класс для сканирования блоков Ethereum и сбора комиссий транзакций.
    Class for scanning Ethereum blocks and collecting transaction fees.

    """

    def __init__(self, api_key, limit):

        # Сохраняем настройки внутри объекта | Store settings inside the object

        self.api_key = api_key
        self.limit = limit

        # Создаём подключение к Ethereum | Create an Ethereum connection

        self.provider = Web3(HTTPProvider(api_key))

        # Получаем номер текущего последнего блока | Get the current latest block number

        self.last_block = self.provider.eth.block_number 
        
        # последний блок
        
        self.target_block = self.last_block + LIMIT # лимит (я поставил 50)

        # Храним номер последнего обработанного блока | Store the latest processed block number

        self.latest_block = 0

        # Создаём список для собранных данных | Create a list for collected data

        self.fees = []
        self.transactions_data = []

    def get_trx_data(self,hash:str) -> Transaction:
        """Получает данные о транзакции

        Args:
            hash (str): номер транзакции ETH

        Returns:
            Transaction: данные транзакции (см. файл OOP_custom_data_types)
        Examples:
        Пример 1
        ```python
        data = BlockchainScanner.get_trx_data("....")
        print(data.amount)
        ```
        """
        ...

    def get_transaction_fee(self, tx_hash):
        

        # Получаем квитанцию по хэшу транзакции | Get the receipt using the transaction hash | receipt - квитанция транзакции

        receipt = self.provider.eth.get_transaction_receipt(tx_hash)

        # Рассчитываем фактическую комиссию в wei | Calculate the actual fee in wei

        fee_wei = receipt["gasUsed"] * receipt["effectiveGasPrice"]

        # Возвращаем рассчитанную комиссию | Return the calculated fee

        return fee_wei


    def scan(self):

        """
        Получает последние блоки и собирает данные транзакций.
        Fetches the latest blocks and collects transaction data.
        
        """

        # Продолжаем, пока номер блока не превысит целевой
        # Continue while the block number does not exceed the target
    
        while self.last_block <= self.target_block:

            # Получаем последний блок вместе с полными транзакциями
            # Get the latest block, including full transaction objects
    
            block = self.provider.eth.get_block("latest",full_transactions=True) 

            # Сохраняем номер полученного блока | Store the retrieved block number

            self.last_block = block["number"]

            # Проверяем, появился ли новый блок | Check whether a new block has appeared
    
            if self.latest_block < self.last_block:
                self.latest_block = self.last_block

                logger.info(
                   f"Найден блок: {self.last_block}, "
                   f"цель: {self.target_block}"
                           )

                # Перебираем все транзакции блока | Iterate through all transactions in the block
    
                for transaction in block["transactions"]:

                    # Получаем комиссию по хэшу транзакции
                    # Get the transaction fee using its hash
    
                    fee_wei = self.get_transaction_fee(transaction["hash"])

                    # Получаем размер входных данных в байтах
                    # Get the size of the input data in bytes
                
                    input_size_bytes = len(transaction["input"])

                    # Создаём запись с нужными данными транзакции
                    # Create a record containing the required transaction data

                    # TODO: Оберни в отдельный тип данных по типу Transaction
                    transaction_data = {
                        "hash": transaction["hash"],
                        "fee_wei": fee_wei,
                        "input_size_bytes": input_size_bytes
                    }

                    # Добавляем запись в общий список
                    # Add the record to the collection
    
                    self.transactions_data.append(transaction_data)

                    return self.transactions_data
                
    def calculate_average_fee(self):
        """

        Рассчитываем среднюю комиссию.
        Calculates the average transaction fee.

        """

        # Проверяем, есть ли собранные транзакции
        # Check whether any transactions were collected

        if not self.transactions_data:
            logger.warning("Нет данных для расчёта среднего")
            return None

        # Извлекаем комиссии всех транзакций
        # Extract the fees from all transactions

        fees = []

        for transaction in self.transactions_data:
            fees.append(transaction["fee_wei"])

        # Считаем среднее арифметическое
        # Calculate the arithmetic mean

        average_fee = sum(fees) / len(fees)

        # Возвращаем среднюю комиссию в wei
        # Return the average fee in wei

        return average_fee

    def calculate_min_max_fee(self):

        # Проверяем, есть ли собранные транзакции
        # Check whether any transactions were collected

        if not self.transactions_data:
            logger.warning("Нет данных для расчёта среднего")
            return None

        # Извлекаем комиссии всех транзакций
        # Extract the fees from all transactions

        fees_for_min_max = []
        
        for transaction in self.transactions_data:
            fees_for_min_max.append(transaction["fee_wei"])

        # Находим максимальные и минимальные комиссии

        max_fees, min_fees = max(fees_for_min_max), min(fees_for_min_max)

        return max_fees, min_fees        

   
# Создаём сканер с настройками из .env | Create a scanner using settings from .env

scanner = BlockchainScanner(API_KEY, LIMIT)

# Запускаем сканирование | Start scanning

scanner.scan()

average_fee = scanner.calculate_average_fee()

if average_fee is not None:
    print(f"Средняя комиссия: {average_fee} wei")
    print(f"Средняя комиссия: {average_fee / 10**18:.18f} ETH")

#len(scanner.transactions_data) — считает количество собранных записей.

print("Всего собрано транзакций:", len(scanner.transactions_data))


#[:5] — показывает первые пять записей, чтобы не выводить тысячи строк в консоль.

for transaction in scanner.transactions_data[:5]:

    print(transaction)

result_min_max = scanner.calculate_min_max_fee()

if result_min_max is not None:
    max_fee, min_fee = result_min_max

    print(f"Максимальная комиссия: {max_fee} wei")
    print(f"Минимальная комиссия: {min_fee} wei")

average_fee = scanner.calculate_average_fee()

if average_fee is not None:

    print(f"Средняя комиссия: {average_fee} wei")
    print(f"Средняя комиссия: {average_fee / 10**18:.18f} ETH")