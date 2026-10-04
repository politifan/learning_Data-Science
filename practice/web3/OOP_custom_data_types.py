from typing import TypedDict
from time import time

print(time())

A = {"block_number":1234,"transactions":{"transaction":{"ammount":500,
                                                    "sender":"user1",
                                                    "reciepent":"user2",
                                                    "timestamp":time()
                                                    }
                                    }
    } # Проблема с тем, что мы не гарантируем какой ключ и значение (их типы)

class custom(TypedDict):
    hello:str
    int_data:int

result = custom(A)

print(result)