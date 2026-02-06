import argparse
import time
from PIL import ImageDraw
import os

from noise import *
from functions import *
from plot import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--count",
        type = int,
        default = 1,
        help = "Количество сгенерированных карт"
    )

    parser.add_argument(
        "-l", "--line",
        type=bool,
        default=False,
        help="Соединять линиями точки"
    )

    parser.add_argument(
        "-s3", "--show_3d",
        type=bool,
        default=False,
        help="Вывести график 3D"
    )

    parser.add_argument(
        "-s2", "--show_2d",
        type=bool,
        default=False,
        help="Вывести график 2D"
    )

    parser.add_argument(
        "-png", "--show_png",
        type=bool,
        default=False,
        help="Вывести картинку вид сверху"
    )


    input_count = parser.parse_args().count
    line = parser.parse_args().line

    for count in range(input_count):
        seed = int(time.time_ns())
        heightmap = generate_heightmap(256, 35, seed)

        #Для рисовки островов визуально
        arr = [[0 for __ in range(4096)] for _ in range(4096)]

        x_center = 0
        y_center = 0

        new_img = Image.new("RGBA", (len(arr), len(arr)), "black") #черное изображение
        draw_heightmap(new_img, heightmap)
        img = ImageDraw.Draw(new_img)

        #Список с координатами островов
        output_arr = []

        #Файл для сохранения
        os.makedirs('../output/functions', exist_ok=True)
        file_list = open(f'../output/functions/{count}.mcfunction', 'w+', encoding='utf-8')
        rad = 0
        for x in range(19):  # кол-во колец
            #начальный угол
            alf = randint(-20, 35)

            if x < 2:  # каждую группу колец меняются значения
                # старое
                # alf_step = (80 - x * 20, 120 - x * 15)
                alf_step = (70 - x * 30, 110 - x * 40)

                spread = (-13 - int(5 * x ** 2.5), 13 + int(5 * x ** 2.5))
                rad += randint(55, 70) + randint(x * 3, max(int(x ** 2.5), x * 3 + 3))  # радиус от центра

            elif x < 6:
                # старое
                # alf_step = (max(45 - int(x ** 2.5), 12), 70 - x * 2)
                alf_step = (max(12, 30 - int(x**2)), 45 - int(x ** 2))

                spread = (-15 - int(x ** 2.3), 15 + int(x ** 2.3))
                rad += randint(65, 70) + randint(x * 3, max(int(x ** 2), x * 5 + 3))

            else:
                alf = randint(-10, 40)
                # старое
                # alf_step = (30 - x * 2, max(60 - int(x * 4), 9))
                alf_step = (max(20 - x * 2, 1), max(23 - int(x * 1.5), 2))

                spread = (-40 - x * 4, 40 + x * 4)
                # старое
                # rad += randint(80, 90) + randint(x * 4, max(int(x ** 2.2), x * 5 + 3))
                rad += randint(70, 90) + randint(x * 3, int(x ** 2))

            # Рисует кольцо с заданным параметрами
            create_circle(arr, (x_center, y_center), rad, alf, alf_step, spread, heightmap, img, output_arr)

        # Добавляем нулевой остров, чтобы ему задалась высота
        start_island = [0, get_height(heightmap, 0, 0), 0]

        # После отрисовки всех колец задаем им размер
        give_size(output_arr, img)

        print(len(output_arr), "всего", end=" ")
        print([x[1] in range(85, 300) for x in output_arr].count(True), "высоких", end=" ")
        print([x[1] in range(-60, 25) for x in output_arr].count(True), "низких")

        #сохраняем фото + функцию
        os.makedirs('../output/images', exist_ok=True)
        new_img.save(f'../output/images/{count}.png', dpi=(3, 3))

        file_list.write(f"data modify storage dsb_gen:gen Islands set value {output_arr}\n")
        file_list.write(
            f"data modify storage dsb_gen:gen StartIsland set value {{x:{start_island[0]}, y:{start_island[1]}, z:{start_island[2]}}}")
        file_list.close()

        ###Вывод фото, графиков
        if parser.parse_args().show_png:
            new_img.show(f'../output/{count}.png')

        args_x = []
        args_y = []
        args_z = []
        for i in output_arr:
            args_x.append(i[0])
            args_y.append(i[1])
            args_z.append(i[2])

        show_2d = parser.parse_args().show_2d
        if parser.parse_args().show_3d:
            plot_height_3d_xy_as_height(args_x, args_y, args_z, line = line, block = not(show_2d))
        if show_2d:
            plot_height_points(args_x, args_y, line = line)

if __name__ == "__main__":
    main()