
import numpy as np


# Y = W*X + b
# Полносвязный слой

class Dense:
    def __init__(self, input_size, output_size):
        self.W = np.random.randn(input_size, output_size) * np.sqrt(2 / input_size)
        self.b = np.zeros((1, output_size))

    def forward(self, x):
        self.x = x
        return x @ self.W + self.b

    def backward(self, grad, lr):
        dW = self.x.T @ grad
        db = np.sum(grad, axis=0, keepdims=True)

        dx = grad @ self.W.T

        self.W -= lr * dW
        self.b -= lr * db

        return dx

# y = max(0,x)
# Функция активации ReLU
class ReLU:
    def forward(self, x):
        self.x = x
        return np.maximum(0, x)

    def backward(self, grad):
        return grad * (self.x > 0)


class MSE:
    def forward(self, predicted, target):
        self.predicted = predicted
        self.target = target

        return np.mean((predicted - target) ** 2)

    def backward(self):
        return 2 * (self.predicted - self.target) / self.predicted.size

# Нейронная сеть
class NeuralNetwork:
    def __init__(self):
        self.fc1 = Dense(784, 128)
        self.relu1 = ReLU()

        self.fc2 = Dense(128, 64)
        self.relu2 = ReLU()

        self.fc3 = Dense(64, 10)

        self.loss_fn = MSE()

    def forward(self, x):
        x = self.fc1.forward(x)
        x = self.relu1.forward(x)

        x = self.fc2.forward(x)
        x = self.relu2.forward(x)

        x = self.fc3.forward(x)

        return x

    def train_step(self, x, y, lr=0.01):
        logits = self.forward(x)

        # Превращаем номера классов в векторы
        target = np.eye(10)[y]

        loss = self.loss_fn.forward(logits, target)

        grad = self.loss_fn.backward()

        grad = self.fc3.backward(grad, lr)
        grad = self.relu2.backward(grad)

        grad = self.fc2.backward(grad, lr)
        grad = self.relu1.backward(grad)

        self.fc1.backward(grad, lr)

        return loss

    def predict(self, x):
        logits = self.forward(x)
        return np.argmax(logits, axis=1)


# Создание модели
model = NeuralNetwork()

# Пример формата данных (не настоящий MNIST)
X = np.random.rand(32, 784)
y = np.random.randint(0, 10, size=32)

# Один шаг обучения
loss = model.train_step(X, y)

print("Loss:", loss)
print("Predictions:", model.predict(X))
