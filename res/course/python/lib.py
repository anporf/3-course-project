from collections import deque
from sympy.geometry import Point2D, Segment2D, Circle

eps = 1e-5
lens = {}


def float_point(P):
    return Point2D(float(P.x), float(P.y))


class Vector:
    def __init__(self, A, B):
        self.x = B.x - A.x
        self.y = B.y - A.y

    def __xor__(self, other):
        return self.x * other.y - self.y * other.x


class Point:
    def __init__(self, A, num):
        self.A = A
        self.num = num

    def __eq__(self, other):
        return self.num == other.num and Segment2D(self.A, other.A).length < eps

    def __str__(self):
        return str(self.A) + " " + str(self.num)

    def dist(self, other=None):
        if other:
            return self.A.distance(other.A)
        return self.A.distance(Point2D(0, 0))


class Face:
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

    def make_next(self, edge):
        x, y = edge
        vertexes = [self.A, self.B, self.C]
        ver_nums = list(map(lambda x: x.num, vertexes))
        X = vertexes[ver_nums.index(x)]
        Y = vertexes[ver_nums.index(y)]
        vertexes.pop(vertexes.index(X))
        vertexes.pop(vertexes.index(Y))
        Z = vertexes.pop()
        num_D = ({1, 2, 3, 4} - set(ver_nums)).pop()
        XD = lens.get((X.num, num_D), lens.get((num_D, X.num), 0))
        YD = lens.get((Y.num, num_D), lens.get((num_D, Y.num), 0))
        # wx = Circle(X.A, XD)
        # wy = Circle(Y.A, YD)
        # try:
        #     D1, D2 = wx.intersection(wy)
        # except:
        XD, YD = float(XD), float(YD)
        X.A = float_point(X.A)
        Y.A = float_point(Y.A)
        wx = Circle(X.A, XD)
        wy = Circle(Y.A, YD)
        D1, D2 = wx.intersection(wy)

        XY = Vector(X.A, Y.A)
        XD1 = Vector(X.A, D1)
        XZ = Vector(X.A, Z.A)
        D = Point(D1, num_D)
        if (XY ^ XD1) * (XY ^ XZ) > 0:
            D = Point(D2, num_D)
        return Face(X, Y, D)

    def values(self):
        return self.A, self.B, self.C


def add(points, P, t):
    if P not in points and P.dist() < t:
        points.append(P)
        return True
    return False


def get_all_points(A, B, C, D, t):
    vertexes = [A, B, C, D]
    global lens
    lens = {}
    for i in range(len(vertexes)):
        for j in range(i):
            lens[(j + 1, i + 1)] = vertexes[i].distance(vertexes[j])

    A_p = Point(Point2D(A.x, A.y), 1)
    B_p = Point(Point2D(B.x, B.y), 2)
    C_p = Point(Point2D(C.x, C.y), 3)
    start = Face(A_p, B_p, C_p)
    q = deque()
    q.append((start, -1))
    points = [A_p, B_p, C_p]
    count = 0
    while len(q):
        face, last_edge = q.popleft()
        e1 = (face.A.num, face.B.num)
        e2 = (face.B.num, face.C.num)
        e3 = (face.C.num, face.A.num)
        edges = {e1, e2, e3} - {last_edge}
        faces = []
        for edge in edges:
            faces.append((face.make_next(edge), edge))
            count += 1
        for face_it, edge in faces:
            flag = False
            for point in face_it.values():
                flag = flag or add(points, point, t)
            if flag:
                q.append((face_it, edge))
    return points


def get_geodesics(points, precision=3):
    result = {}
    for A in points:
        for B in points:
            if A.num == B.num:
                continue
            geodesic_len = round(A.dist(B), precision)
            result[geodesic_len] = result.get(geodesic_len, 0) + 1
    return result
