from math import e
a = [[1,2,3],
     [4,5,6],
     [7,8,9]]

plain_a = []
[plain_a.extend(i) for i in a]


def sigmoid(x:float) -> float:
    return 1/(1+e**-x)

def linear(x:float, w:float=2.5, b:float=-1) -> float:
    return w*x + b

sigmoid(linear(
    sigmoid(linear(0.8))
    )) 