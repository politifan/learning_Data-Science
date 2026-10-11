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

###

# Configuring logging

###

logger = setup_logging(logging.DEBUG)

load_dotenv()

###

# Assign API key values ​​and set a limit

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

    def __init__(self, api_key, limit):

        self.api_key = api_key
        self.limit = limit

        self.provider = Web3(HTTPProvider(api_key))
        self.last_block = self.provider.eth.block_number # последний блок
        self.target_block = self.last_block + LIMIT # лимит (я поставил 50)
        self.latest_block = 0


    def scan(self):

        while self.last_block <= self.target_block:

            block = self.provider.eth.get_block("latest",full_transactions=True) # Получаем данные последнего блока + транзакции
            self.last_block = block["number"]

            if self.latest_block < self.last_block:
                self.latest_block = self.last_block
            
            sleep(1)

scanner = BlockchainScanner(API_KEY, LIMIT)
scanner.scan()

def get_data(hash:str):
    receipt = provider.eth.get_transaction_receipt(hash)
    print(receipt["gasUsed"]*receipt["effectiveGasPrice"] * 10**-18)
    


get_data("0x67906ff04bd249d67902609fa5b98d6f228df110d26c03f07060f59df31951db")

# TODO: Доработать
# BUG: 
# while last_block <= target_block:
#     block = provider.eth.get_block("latest",full_transactions=True) # Получаем данные последнего блока + транзакции
# 
#     last_block = block["number"]
# 
#     if latest_block < last_block:
#         latest_block = last_block
#         for transaction in block["transactions"]:
#             from_user = transaction["from"]
#             to_user = transaction["to"] 
#             transaction["maxPriorityFeePerGas"]
#             print(transaction["hash"].to_0x_hex())
# 
# 
# 
#         
#     sleep(1)
