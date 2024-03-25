import matplotlib.pyplot as plt


def draw_points_py(points):
    vertex_factor = [[] for i in range(4)]
    for point in points:
        vertex_factor[point.num - 1].append(point.A)
    for i, factor in enumerate(vertex_factor, start=1):
        X = list(map(lambda x: x.x, factor))
        Y = list(map(lambda x: x.y, factor))
        plt.scatter(X, Y, label=i)
    plt.legend()
    plt.show()

def draw_points_out(points, info):
    plt.figure(figsize=(10, 8))
    vertex_factor = [[] for i in range(4)]
    for point in points:
        vertex_factor[point[1] - 1].append(point[0])
    for i, factor in enumerate(vertex_factor, start=1):
        X = list(map(lambda x: x[0], factor))
        Y = list(map(lambda x: x[1], factor))
        plt.scatter(X, Y, s=5, label=f'{i}: {tuple(map(lambda x: round(x, 3), info[i - 1]))}')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(right=0.75)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig('res.png')
    # plt.show()

def draw_geodesic(geodesics):
    X = []
    Y = []
    for key, value in sorted(geodesics.items()):
        X.append(key)
        Y.append(value)
    plt.scatter(X, Y)
    plt.savefig('res_geod.png')
    plt.show()
    

def draw_geodesic_counts_func(counts, title, y_label, func=lambda k, v: v, draw=True, save_name=None):   
    plt.figure(figsize=(10, 8))
    X = []
    Y = []
    for key, value in counts.items():
        X.append(key)
        Y.append(func(key, value))
    fig = plt.figure()
    ax = fig.add_axes([0.15, 0.15, 0.75, 0.75])
    ax.axis('equal')
    ax.scatter(X, Y)
    ax.set_title(title)
    ax.set_xlabel("radius")
    ax.set_ylabel(y_label)
    if draw:
        plt.show()
    else:
        fig.savefig(f"{save_name}.png")
