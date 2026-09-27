from time import time
a = int(input("Введите число: ")) #
variant = int(input("""Введите вариант счисления:
2. Двоичная
4. 4-ричная
8. 8-ричная
10. 10-ричная
16. 16-ричная
"""))

number = ""
b = int(a)

start = time()
while b > 0:
    number += str(b%variant)
    b //= variant
    
number = number[::-1]
end = time() - start 
print(number)
print(end)


#if variant in ["1","2","3","4","5"]:
#    if variant == "1":
#        ...
#else:
#    raise ValueError("Такого варианта нет!")