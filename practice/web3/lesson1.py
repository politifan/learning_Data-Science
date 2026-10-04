from os import getenv # получить переменную из .env файла окружения
from dotenv import load_dotenv # загрузка окружения в данной папке (окружение - .env файл)
import logging # библиотека для красивого вывода данных с форматированием
from time import sleep

from web3 import Web3, HTTPProvider # Библиотека для работы с криптовалютой

from logger import setup_logging # Наша собственная библиотека 

logger = setup_logging(logging.DEBUG)

load_dotenv()

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

last_block = provider.eth.block_number # последний блок
target_block = last_block + LIMIT # лимит (я поставил 50)
latest_block = 0

while last_block <= target_block:
    block = provider.eth.get_block("latest",full_transactions=True) # Получаем данные последнего блока + транзакции

    last_block = block["number"]

    if latest_block < last_block:
        latest_block = last_block

        
    sleep(1)



a = {"hello":"world"}

word = a["hello"]

print(word)
print(word)