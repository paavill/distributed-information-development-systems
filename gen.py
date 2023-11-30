import xmlrpc.client as client
import time
import random

server = client.ServerProxy("http://localhost:8012/RPC2")

def case1():
    print('Ping:', server.ping())

def case2():
    print('Server datetime:', server.now())

def case3():
    print('View, type, value:', server.type(2))

def case4():
    print ('Pow 2^3: ', server.pow(2, 3))

def default_case():
    print ('Sum 2 + 3 :', server.sum(2, 3))


# Задаем время работы цикла (в секундах)
duration = 20 * 60

# Время старта цикла
start_time = time.time()
while time.time() - start_time < duration:
    # Здесь вы можете добавить ваш код или логику выбора случая
    # В данном примере используется словарь вместо switch case

    user_choice = str(random.randint(1, 5))

    switch_cases = {
        '1': case1,
        '2': case2,
        '3': case3,
        '4': case4,
    }

    # Выполняем соответствующий случай или default_case, если ключ не найден
    switch_cases.get(user_choice, default_case)()