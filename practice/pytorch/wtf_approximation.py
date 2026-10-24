import math

x = float(input("Введите число, для  которого считаем аппроксимацию: "))
epsilon = float(input("Введите требуемую точность: "))

def  approx(x:float, epsilon:float) -> float:
    """Разработка кода,  для вычисления аппроксимацию по двум  данным

    Args:
        x (float): аргумент,  для которого проверяем аппроксимацию
        epsilon (float): точность   вычисления

    Returns:
        float: результат  вычислений
    
    
    """
    if x == 0:
        return 1.0
    # total - накопленный результат вычислений
    # addend - слагаемое
    # n - счетчик
    total, addend, n = 1, 1, 1
    
    while epsilon < abs(addend):
        addend_new = addend * (x/n) 
        total += addend_new
        addend = addend_new
        n += 1
        print(addend_new,  total)

        
    return total

result  = approx(x, epsilon)
exact = math.exp(x)
print(result)
print("Точное значение:", exact)
print("Абсолютная ошибка:", abs(exact - result))
print(f"Относительная ошибка: {abs(exact  - result)/abs(exact)*100:.6f}%")
