from PIL import Image,ImageDraw
from smite import create
from colors import *


#14,19,23
for number in range(1):
    file = open(fr'C:\Users\Максим\Desktop\SkyBlock\шаблоны генерации\функции\{number}.mcfunction', 'w', encoding='utf-8')

    arr = create()

    new_img = Image.new("RGBA", (len(arr), len(arr)), "black")
    img = ImageDraw.Draw(new_img)
    for x in range(len(arr)):
        for y in range(len(arr)):
            img.point((x, y), fill=dic[arr[x][y]])

    # new_img.save(r"C:\Users\Максим\Desktop\test.png",dpi = (3,3))
    new_img.save(fr'output\arr.png', dpi=(3, 3))
    new_img.save(fr'C:\Users\Максим\Desktop\SkyBlock\шаблоны генерации\{number}.png', dpi=(3, 3))
    file.write(f"data modify storage dsb_gen:gen List set value {arr}")
    file.close()
    print(len(arr[0]))