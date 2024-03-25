import numpy as np
from lib import get_all_points, get_geodesics, Point
import graphix
import json
import math


def draw_data(data):
    data = {float(k): v for k, v in data.items()}
    graphix.draw_geodesic_counts_func(data, 'The number of different lengths of geodesics', 'The number of different lengths of geodesics', draw=False, save_name='Disphenoid/default')
    graphix.draw_geodesic_counts_func(data, 'The number of different lengths of geodesics', 'Exponent indicator', lambda k, v: math.log(v), draw=False, save_name='Disphenoid/Exp')
    graphix.draw_geodesic_counts_func(data, 'The number of different lengths of geodesics', 'Sub-exponent indicator', lambda k, v: math.log(math.log(v))/math.log(k), draw=False, save_name='Disphenoid/sub-exp')


def count():
    A = np.array(0, 0, 0)
    B = np.array(1, 0, 0)
    C = np.array(1 / 2, np.sqrt(3) / 2, 0)
    D = np.array(1 / 2, np.sqrt(3) / 6, np.sqrt(6) / 3)
    r = 5

    points = get_all_points(A, B, C, D, r)

    # count = 10
    # max_r = 5.5
    # start = 1
    # for r in np.linspace(start, max_r, count):
    #     print(f'now {r}')
    #     points = get_all_points(A, B, C, D, r)
    #     # graphix.draw_points(points)
    #     all_geodesic = get_geodesics(points)
    #     # graphix.draw_geodesic(all_geodesic)
    #     with open("points.json", "r") as inp:
    #         old_data = json.load(inp)
    #     old_data[r] = len(all_geodesic)
    #     with open("points.json", "w") as out:
    #         json.dump(old_data, out, indent=2)
    #     # graphix.draw_geodesic_counts(old_data)
    #     print(f'done {r}')


def main():
    # draw_data()
    # count()
    with open("julia/points_irreg2.json", "r") as inp:
        data = json.load(inp)
    with open("julia/info_irreg2.json", "r") as inp:
        info = json.load(inp)
    print(len(data))
    graphix.draw_points_out(data, info)

    # with open("julia/data_35.0.json", "r") as inp:
    #     data = json.load(inp)
    # print(len(data))

    # rdata = {}
    # for k, v in data.items():
    #     k = float(k)
    #     if abs(k - 1) < 1e-7:
    #         rdata[k] = v
    #         continue
    #     rdata[k] = math.log(math.log(v)) / math.log(k)
    # print(rdata[30.0])

    # draw_data(data)
    # rdata = {}
    # for k in data:
    #     if float(k) > 15:
    #         rdata[float(k)] = data[k]
    # graphix.draw_geodesic_counts_func(rdata, 'The number of different lengths of geodesics', 'Sub-exponent indicator', lambda k, v: math.log(math.log(v))/math.log(k), draw=False, save_name='Disphenoid/sub-exp-tail')

    # data = {float(k): v for k, v in data.items()}
    # graphix.draw_geodesic_counts_func(data, 'The number of different lengths of geodesics', 'Sub-exponent indicator', lambda k, v: math.log(math.log(v))/math.log(k), draw=False, save_name='sub-exp')

    # graphix.draw_geodesic(rdata)

if __name__ == '__main__':
    main()
