# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet
import matplotlib.pyplot as plt
import os


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            object_type = line.split()[0].lower()
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return objects


def parse_star_parameters(line, star):

    """Считывает данные о звезде из строки.
    Входная строка должна иметь слеюущий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.
    Пример строки:
    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.
    **star** — объект звезды.
    """

    star.R = float(line.split()[1])
    star.color = line.split()[2].upper()
    star.m = float(line.split()[3])
    star.x = float(line.split()[4])
    star.y = float(line.split()[5])
    star.Vx = float(line.split()[6])
    star.Vy = float(line.split()[7])

def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
    Пример строки:
    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """

    planet.R = float(line.split()[1])
    planet.color = line.split()[2].upper()
    planet.m = float(line.split()[3])
    planet.x = float(line.split()[4])
    planet.y = float(line.split()[5])
    planet.Vx = float(line.split()[6])
    planet.Vy = float(line.split()[7])


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            print("%s %d %s %f %f %f %f %f" % (obj.type, obj.R, obj.color, obj.m, obj.x, obj.y, obj.Vx, obj.Vy), file = out_file)

# FIXME: хорошо бы ещё сделать функцию, сохранающую статистику в заданный файл...

def write_spase_objects_statistic_to_file(spase_objects, time):
    """Сохраняет статистику о планетах в файл.
    Строка имеет формат <скорость> <расстояние до звезды> <физическое время>
    Параметры:
    **spase_objects** - список тел
    **time** - физическое время
    """

    with open('statistic_of_the_last_launch.txt', 'a') as st_file:
        for obj in spase_objects:
            if obj.type != 'star':
                for object in spase_objects:
                    if object.type == 'star':
                        r = ((obj.x - object.x)**2 +(obj.y - object.y)**2)**0.5
                v = (obj.Vx**2 + obj.Vy**2)**0.5
                print(v, r, time, file = st_file)


def delete_statistic_file():
    """удаляет старый файл статистики
    """
    if os.path.exists('statistic_of_the_last_launch.txt'):
        os.remove('statistic_of_the_last_launch.txt')



def graphics():
    """функция, рисующая графики по статистике, сохраненной в файл
    """
    v = []
    r = []
    time = []
    with open('statistic_of_the_last_launch.txt') as st_file:
        for line in st_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            line = list(map(float, line.strip().split()))
            v.append(line[0])
            r.append(line[1])
            time.append(line[2])
    sp = plt.subplot(221)
    plt.title(r'Зависимость скорости объекта от времени', fontsize=12)
    plt.plot(time, v)
    sp = plt.subplot(222)
    plt.title(r'Зависимость скорости объекта от расстояния до звезды', fontsize=12)
    plt.plot(r, v)
    sp = plt.subplot(223)
    plt.title(r'Зависимость расстояния до звезды от времени', fontsize=12)
    plt.plot(time, r)
    sp = plt.subplot(224)
    plt.title(r'Зависимость времени от времени', fontsize=12)
    plt.plot(time, time)
    plt.show()
                


if __name__ == "__main__":
    print("This module is not for direct call!")
