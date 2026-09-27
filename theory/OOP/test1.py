from random import randint

class Wallet:
    
    '''A class that performs wallet operations.'''

    def __init__(self, address: str, balance:float):
        self.address = address
        self.balance = balance

    def send(self, recipient:"Wallet", amount:float):

        if self.balance < amount:
            raise ValueError('Not enough money')

        self.balance -= amount
        recipient.balance += amount

################# Кастомный тип данных, который изменяется
class L:
    def __init__(self,*args):
        self.data = [*args]
    def __get__(self, index:int):
        return self.data[index]
    def __len__(self) -> int:
        return len(self.data)**2
    def __str__(self) -> str:
        return str(self.data)
    def append(self,arg) -> None:
        self.data += [arg]

data = L(1,2,"hello")
print(data)
data.append("world")
print(len(data))
print(data.__get__(0))
print(data)

##################
a = [1,2,3,4,4,4,6,6,5]
b = 5
# Если тип данных изменяем (по умолчанию любой тип данных изменяемый)
# Если тип данных изм., то у него будут методы для измения.
# Изменяемые типы данных: любой новый класс, list, set, dict,
# Неизменяемые типы данных: tuple, str, int, float, bool, frozenset

def test1(a:int):
    a = a + 1
    print(a)
    return 0

print(b)
test1(b)
print(b)


def test(l:list[int]):
    d = l.copy()
    d.append(5)
    print(d)
    return []

print(a)
test(a)
print(a)
################


class Transaction:

    '''
    A class that performs transaction operations.

    Sender - the wallet that sends money

    Recipient - the wallet that receives money

    Amount - the amount of money that is sent
    
    '''
    def __init__(self, sender:Wallet, recipient:Wallet, amount:float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.status = 'pending'
    
    def execute(self):

        ''' Transaction execution '''

        try:
            self.sender.send(self.recipient, self.amount)
            self.status = 'completed'

        except ValueError:
            self.status = 'failed'


class Wallet_v2(Wallet):
    def __init__(self, address, balance):
        super().__init__(address, balance)
        self.uid = randint(1000, 9999)

    def __eq__(self, wallet:"Wallet_v2"):
        return self.uid == wallet.uid

    def __gt__(self, wallet:"Wallet_v2"):
        return self.balance > wallet.balance

    def is_equal(self,wallet:"Wallet_v2"):
        return self.uid == wallet.uid

    def send(self, recipient:"Wallet_v2", amount):
        print(f"Транзакция от {self.uid} -> {recipient.uid} ")
        return super().send(recipient, amount)

a = [Wallet_v2("hello",1), Wallet_v2("hello",1)]
b,c = Wallet_v2("hello",1), Wallet_v2("hello",1)
print(b > c)
print(b == c)

for i in a:
    print(i.uid)

a[0].send(a[1],1)
