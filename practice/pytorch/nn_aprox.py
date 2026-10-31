
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

# Данные
# Обучающая выборка

X = np.linspace(-np.pi/2, np.pi/2, 200).reshape(-1, 1)
Y = np.sin(X) 

# Нейросеть: 1 -> 32 -> 32 -> 1
np.random.seed(42)

W1 = np.random.randn(1, 32) * 0.5
b1 = np.zeros((1, 32))

W2 = np.random.randn(32, 32) * 0.2
b2 = np.zeros((1, 32))

W3 = np.random.randn(32, 1) * 0.2
b3 = np.zeros((1, 1))

# learning rate - скорость обучения
lr = 0.01

plt.ion()
fig, ax = plt.subplots()

for epoch in range(1000):
    # Прямой проход
    z1 = X @ W1 + b1
    a1 = np.tanh(z1)

    z2 = a1 @ W2 + b2
    a2 = np.tanh(z2)

    pred = a2 @ W3 + b3

    # MSE
    loss = np.mean((pred - Y) ** 2)

    # Обратное распространение
    d3 = 2 * (pred - Y) / len(X)

    dW3 = a2.T @ d3
    db3 = np.sum(d3, axis=0, keepdims=True)

    d2 = (d3 @ W3.T) * (1 - a2 ** 2)
    dW2 = a1.T @ d2
    db2 = np.sum(d2, axis=0, keepdims=True)

    d1 = (d2 @ W2.T) * (1 - a1 ** 2)
    dW1 = X.T @ d1
    db1 = np.sum(d1, axis=0, keepdims=True)

    # Обновление весов
    W3 -= lr * dW3
    b3 -= lr * db3

    W2 -= lr * dW2
    b2 -= lr * db2

    W1 -= lr * dW1
    b1 -= lr * db1

    # График
    ax.clear()
    ax.plot(X, Y, label="sin(x)", color="blue")
    ax.plot(X, pred, label="Нейросеть", color="red")
    ax.set_ylim(-1.5, 1.5)
    ax.set_title(f"Эпоха: {epoch + 1} | MSE: {loss:.6f}")
    ax.legend()
    ax.grid(True)
    #plt.pause(0.05)  # Задержка 1 секунда
    fig.canvas.draw()
plt.ioff()
plt.show()
