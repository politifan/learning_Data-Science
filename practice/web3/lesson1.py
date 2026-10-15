###

# Install options for code:

#  Loading libraries: 'os', 'dotenv', 'time', 'web3', 'logger' 

###

from os import getenv # получить переменную из .env файла окружения
from dotenv import load_dotenv # загрузка окружения в данной папке (окружение - .env файл)
import logging # библиотека для красивого вывода данных с форматированием
from time import sleep
from math import sqrt

from web3 import Web3, HTTPProvider # Библиотека для работы с криптовалютой

from logger import setup_logging # Наша собственная библиотека 

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

    def __init__(self, api_key, limit: int):
        """ Initialize the blockchain scanner.

        Args:
            api_key (_type_): _description_
            limit (_type_): _description_
        """


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


    def get_transaction_fee(self, tx_hash:str) -> float:

        """ Function for obtaining the transaction fee

        Args: 
            str: the transaction hash

        Returns:
            float: the calculated fee
        """

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
    
                    transaction_data = {
                        "hash": transaction["hash"],
                        "fee_wei": fee_wei,
                        "input_size_bytes": input_size_bytes
                    }

                    # Добавляем запись в общий список
                    # Add the record to the collection
    
                    self.transactions_data.append(transaction_data)
    def calculate_average_fee(self) -> float | None:

        """Calculates the average transaction fee.

        Returns:
            float | None: The average fee in wei, or None if no data exists.
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

    def calculate_min_max_fee(self) -> float | None:

        """ find the maximum and minimum commissions

        Returns:
            float | None: Max and min fee in wei, or None if no data exists.

        """

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
    
    def calculate_fee_variance(self) -> float | None:
        """ 
        Calculate the population variance of transaction fees.
        Рассчитывает дисперсию комиссий собранных транзакций.

        Args: list - словарь списков транзакций transactions_data

        Returns:
            float | None: готовая дисперсия в wei ^2 or None if no data exists.
        """

        # Проверяем, есть ли собранные транзакции
        # Check whether any transactions were collected
        if not self.transactions_data:
            logger.warning("Нет данных для расчёта дисперсии")
            return None

        # Извлекаем комиссии всех транзакций
        # Extract fees from all transactions
        fees = []

        for transaction in self.transactions_data:
            fees.append(transaction["fee_wei"])

        # Рассчитываем среднее арифметическое
        # Calculate the arithmetic mean
        average_fee = sum(fees) / len(fees)

        # Суммируем квадраты отклонений от среднего
        # Sum the squared deviations from the mean
        squared_deviations_sum = 0

        for fee in fees:
            difference = fee - average_fee
            squared_deviations_sum += difference ** 2

        # Делим сумму квадратов отклонений на количество значений
        # Divide the sum of squared deviations by the number of values
        variance = squared_deviations_sum / len(fees)

        # Возвращаем дисперсию в wei в кввадрате
        # Return the variance in wei squared
        return variance
    
    def calculate_fee_input_correlation(self) -> float | None:
        """ 
        Calculate the correlation between transaction fees and input sizes.
        Рассчитывает корреляцию между комиссиями и размерами input.

        Returns:
            float | None: готовая корреляция значений | ready-made correlation of values or None if no data exists.
        """

        # Проверяем, есть ли минимум две транзакции.
        # Check whether at least two transactions are available.
        if len(self.transactions_data) < 2:
            logger.warning("Недостаточно транзакций для корреляции")
            return None

        # Создаём пустые списки для комиссий и размеров input.
        # Create empty lists for fees and input sizes.
        fees = []
        input_sizes = []

        # Перебираем все собранные транзакции.
        # Iterate through all collected transactions.
        for transaction in self.transactions_data:
            # Добавляем комиссию в список.
            # Add the fee to the list.
            fees.append(transaction["fee_wei"])

            # Добавляем размер input в список.
            # Add the input size to the list.
            input_sizes.append(transaction["input_size_bytes"])

        average_fee = sum(fees) / len(fees)
        average_sizes = sum(input_sizes) / len(input_sizes)

        # Создаём накопители для расчёта корреляции.
        # Initialize accumulators for the correlation calculation.
        numerator = 0
        fee_squared_deviations = 0
        size_squared_deviations = 0

        # Сопоставляем каждую комиссию с размером input той же транзакции.
        # Pair each fee with the input size of the same transaction.
        for fee, input_size in zip(fees, input_sizes):

            # Находим отклонение комиссии от среднего.
            # Calculate the fee's deviation from its mean.
            fee_difference = fee - average_fee

            # Находим отклонение размера input от среднего.
            # Calculate the input size's deviation from its mean.
            size_difference = input_size - average_sizes

            # Суммируем произведения парных отклонений.
            # Sum the products of paired deviations.
            numerator += fee_difference * size_difference

            # Суммируем квадраты отклонений комиссий.
            # Sum the squared deviations of fees.
            fee_squared_deviations += fee_difference ** 2

            # Суммируем квадраты отклонений размеров input.
            # Sum the squared deviations of input sizes.
            size_squared_deviations += size_difference ** 2

        # Вычисляем знаменатель формулы корреляции.
        # Calculate the denominator of the correlation formula.
        denominator = sqrt(
            fee_squared_deviations * size_squared_deviations
        )

        # Проверяем, не равен ли знаменатель нулю.
        # Check whether the denominator is zero.
        if denominator == 0:
            logger.warning("Корреляция не определена")
            return None

        # Вычисляем коэффициент корреляции Пирсона.
        # Calculate the Pearson correlation coefficient.
        correlation = numerator / denominator

        # Возвращаем рассчитанный коэффициент.
        # Return the calculated coefficient.
        return correlation


   
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

variance = scanner.calculate_fee_variance()

if variance is not None:
    print(f"Дисперсия комиссий: {variance} wei²")

# Вычисляем корреляцию комиссии и размера input
# Calculate the correlation between fees and input sizes
correlation = scanner.calculate_fee_input_correlation()

if correlation is not None:
    print(f"Корреляция комиссии и input: {correlation:.4f}")
else:
    print("Не удалось рассчитать корреляцию")