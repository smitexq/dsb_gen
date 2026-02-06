import matplotlib.pyplot as plt

"""
Рисует точки в 3D пространстве.
:x,y,z: список координат
block - если выводится еще 2d график, то этот потом не блокируется, иначе поток блокируется
"""
def plot_height_3d_xy_as_height(x, y, z=None, title="3D график высот", xlabel="X", ylabel="Высота (Y)", zlabel="Z", line = False, block = False):
    if z is None:
        z = [0] * len(x)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # линии, соединяющие точки
    if line:
        ax.plot(x, y, z, color='blue', alpha=0.5, linewidth=1)

    # точки, цвет по высоте (y)
    sc = ax.scatter(x, y, z, c=y, cmap='terrain', s=20)
    fig.colorbar(sc, ax=ax, label="Высота (Y)")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

    plt.show(block = block)



"""
Рисует точки высоты по координатам x, y
:x,y: список координат
"""
def plot_height_points(x, y, title="Профиль высоты", xlabel="X", ylabel="Высота", line = False):

    plt.figure(figsize=(10, 5))

    plt.scatter(x, y, color="blue", s=20)  # s = размер точки
    if line:
        plt.plot(x, y, color="green", linewidth=2)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()