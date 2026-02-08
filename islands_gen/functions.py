import math
from random import randint, sample

from noise import get_height


def is_normal_height(h):
    return 40 <= h <= 70


"""
arr - список для визуальной картинки расположения
alf - начальный угол; alf_step - шаг угла. 
spread - разброс островов (ближе - дальше к центру), чтобы они не были четко на линии окружности
heightmap - карта высот
output_arr - итоговый список с координатами островов
is_nether - карта для nether или overworld
"""


def create_circle(arr: list, center: tuple, rad: int, alf: int, alf_step: tuple, spread: tuple, heightmap, image,
                  output_arr: list, is_nether=False):
    #зеленые полосы
    for x in range(628):  #628, потому что длина окружности 2пи, 6,28 * 100 масштаб
        tx = rad * math.sin(x / 100) + center[0]
        ty = rad * math.cos(x / 100) + center[1]
        try:
            if image != None:
                image.point((tx + 2047, ty + 2047), fill="green")
        except:
            continue

    #Обход окружности
    while alf < 628 - alf_step[1] * 0.8:
        #точка со случайным смещением ближе/дальше от центра spread)
        x = rad * math.sin(alf / 100) + center[0] + randint(spread[0], spread[1])
        y = rad * math.cos(alf / 100) + center[1] + randint(spread[0], spread[1])
        #Шаг угла
        alf += randint(alf_step[0], alf_step[1])

        #Ограничение по карте
        if not (-2045 <= x <= 2045) or not (-2045 <= y <= 2045):
            continue

        try:
            #обрисовка острова цветов на картинке
            for cur_x in range(int(x) - 4, int(x) + 5):
                for cur_y in range(int(y) - 4, int(y) + 5):
                    arr[cur_x][cur_y] = 1
            #По умолчанию высота, потом она меняется в зависимости от дальности колец и редкости островов
            output_arr.append([int(x), 0, int(y)])

            #Размер острова в зависимости от дистанции
            distance = (x ** 2 + y ** 2) ** 0.5
            down = False
            if distance <= 190:  #Только мелкие
                output_arr[-1].append(0)
            elif distance <= 250:  #Мелкие и средние
                output_arr[-1].append(1)
                down = True
            elif distance <= 500:  #Мелкие, средние и большие (шанс меньше)
                output_arr[-1].append(2)
                down = True
            else:
                output_arr[-1].append(3)
            output_arr[-1][1] = get_height(heightmap, x, y, can_down=down, is_nether=is_nether)
        except Exception as e:
            print(f"Ошибка: {e} на координатах x: {int(x)} y: {int(y)}")
            continue


def rare_chance(dist_num: int):
    size = [0, 1, 2]  #Размеры
    if dist_num == 0:
        return 0
    elif dist_num == 1:
        #20% средний
        if randint(0, 9) < 2: return 1
        #80 на мелкий
        return 0
    elif dist_num == 2:
        chance = randint(0, 99)
        #10% на большой
        if chance < 10: return 2
        #65% средний
        if chance < 75: return 1
        #25 на мелкий
        return 0
    elif dist_num == 3:
        chance = randint(0, 99)
        # 70% на большой
        if chance < 70: return 2
        # 25% средний
        if chance < 95: return 1
        # 5 на мелкий
        return 0


dic_colors = {
    0: (255, 255, 255),  #Маленький
    1: (35, 255, 30),  #Средний
    2: (0, 255, 240),  #Большой
    101: (220, 255, 0),  #квестовый
    50: (255, 100, 250),  #вишня
    102: (246, 255, 0),
    103: (255, 126, 0),
    104: (255, 0, 0)
}


def give_size(arr: list, image, is_nether=False):
    if not is_nether:
        #Житель квестовый
        #Подходящие позиции, то есть острова на первых двух линиях
        quests = [cur for cur in arr if 80 <= (cur[0] ** 2 + cur[2] ** 2) ** 0.5 <= 145]
        index = randint(0, len(quests) - 1)
        quests[index][3] = 101

    for cur_island in range(len(arr)):
        cur_x = arr[cur_island][0]
        cur_z = arr[cur_island][2]

        if arr[cur_island][3] == 101:
            continue

        #В зависимости от дальности разный размер
        size = rare_chance(arr[cur_island][3])

        # Если остров большой, то в радиусе 25 блоков не должно быть никаких островов
        if size == 2:
            range_x = list(range(cur_x - 25, cur_x + 26))
            range_z = list(range(cur_z - 25, cur_z + 26))
            for cur in arr:
                if cur[0] in range_x and cur[2] in range_z:  #Если нашелся остров в этом квадрате
                    if cur[0] != cur_x and cur[2] != cur_z:  #При этом его координаты не равны исходному
                        size = 1
                        break

        # Если остров средний, то в радиусе 20 блоков не должно быть никаких островов
        if size == 1:
            range_x = list(range(cur_x - 20, cur_x + 21))
            range_z = list(range(cur_z - 20, cur_z + 21))
            for cur in arr:
                if cur[0] in range_x and cur[2] in range_z:  # Если нашелся остров в этом квадрате
                    if cur[0] != cur_x and cur[2] != cur_z:  # При этом его координаты не равны исходному
                        size = 0
                        break

        #Задаем размер
        arr[cur_island][3] = size

        #отрисовка
        try:
            for x in range(cur_x - 4, cur_x + 5):
                for y in range(cur_z - 4, cur_z + 5):
                    image.point((x + 2047, y + 2047), fill=dic_colors[size])
        except Exception:
            print(size)

    if is_nether:
        #Крепость проклятых душ
        quests = [cur for cur in arr if
                  (350 <= (cur[0] ** 2 + cur[2] ** 2) ** 0.5 <= 700) and is_normal_height(cur[1])]
        for x in quests: x[-1] += 100
        return

    #пещерные острова
    caves = [cur for cur in arr if (cur[1] <= 25)]
    for x in caves: x[-1] = -1  #размер пещерного

    #Вишня 3 острова
    quests = [cur for cur in arr if
              (30 <= (cur[0] ** 2 + cur[2] ** 2) ** 0.5 < 500) and is_normal_height(cur[1]) and cur[3] != 101]
    for x in sample(range(0, len(quests)), 3):
        quests[x][-1] += 50

    #Старый остров (используются значения как и у морского царя)
    #Морской царь
    quests = [cur for cur in arr if
              (300 <= (cur[0] ** 2 + cur[2] ** 2) ** 0.5 <= 750) and is_normal_height(cur[1]) and
                not (50 <= cur[3] <= 53)]
    for x in quests: x[-1] += 200
    #Песчаная библиотека
    quests = [cur for cur in arr if (830 <= (cur[0] ** 2 + cur[2] ** 2) ** 0.5 <= 1300) and is_normal_height(cur[1])]
    for x in quests: x[-1] += 300
    #Элеум Лойс
    quests = [cur for cur in arr if (1430 <= (cur[0] ** 2 + cur[2] ** 2) ** 0.5 <= 1900) and is_normal_height(cur[1])]
    for x in quests: x[-1] += 400

    for cur_island in range(len(arr)):
        cur_x = arr[cur_island][0]
        cur_z = arr[cur_island][2]

        size = arr[cur_island][3]
        size = 50 if (50 <= size <= 53) else size

        if size in (50, 101):
            # отрисовка квестового острова
            for x in range(cur_x - 4, cur_x + 5):
                for y in range(cur_z - 4, cur_z + 5):
                    image.point((x + 2047, y + 2047), fill=dic_colors[size])
