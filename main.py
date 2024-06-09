import math

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use("agg")

def save_graphic(set1: np.array, set2: np.array, set3: np.array):
    global number_of_graphic

    fig, ax = plt.subplots(figsize=(6, 6), layout="constrained")
    ax.scatter(set1.T[0], set1.T[1])
    ax.plot(set1.T[0], set1.T[1],)
    ax.scatter(set2.T[0], set2.T[1])
    ax.plot(set2.T[0], set2.T[1])
    ax.scatter(set3.T[0], set3.T[1], color="red")
    ax.plot(set3.T[0], set3.T[1], color="red")
    plt.savefig(f"images\\image{number_of_graphic}.png", dpi=100)
    number_of_graphic += 1

    plt.close(fig)

# Глобальная переменная для определения имени каждого графика
number_of_graphic = 0

"""Функция delta1.
Аргументы: w - вектор решения, 
s - количество элементов в подмножестве p1, 
u - коэффициенты в разложении вектора w."""
def delta1(w, s, p, u):
    m1 = [j for j in range(s) if u[j] > 0]
    return max([np.dot(p[j], w) for j in m1]) - min([np.dot(p[j], w) for j in range(s)])

"""Функция delta2.
Аргументы: w - вектор решения, 
s - количество элементов в подмножестве p1, 
m - количество элементов в множестве p,
u - коэффициенты в разложении вектора w."""
def delta2(w, s, m, p, u):
    m2 = [j for j in range(s, m) if u[j] > 0]
    return max([np.dot(p[j], -1 * w) for j in m2]) - min([np.dot(p[j], -1 * w) for j in range(s, m)])

"""Функция delta.
Аргументы: w - вектор решения, 
s - количество элементов в подмножестве p1, 
m - количество элементов в множестве p,
u - коэффициенты в разложении вектора w."""
def delta(w, s, m, p, u):
    return max(delta1(w, s, p, u), delta2(w, s, m, p, u))

def next_appr_mdm(p, w1, w2, s, m, u):
    w = w1 - w2
    if delta(w, s, m, p, u) == 0:
        return w1, w2, u
    else:
        m1 = [j for j in range(s) if u[j] > 0]
        indexes_for_max = [[np.dot(p[j], w), j] for j in m1]
        indexes_for_min = [[np.dot(p[j], w), j] for j in range(s)]
        j_stroke = max(indexes_for_max)[1]
        j_stroke_stroke = min(indexes_for_min)[1]

        m2 = [j for j in range(s, m) if u[j] > 0]
        indexes_for_max = [[np.dot(p[j], -w), j] for j in m2]
        indexes_for_min = [[np.dot(p[j], -w), j] for j in range(s, m)]
        l_stroke = max(indexes_for_max)[1]
        l_stroke_stroke = min(indexes_for_min)[1]

        if delta1(w1-w2, s, p, u) >= delta2(w1-w2, s, m, p, u):
            # Определяем t_k
            p_inter = p[j_stroke] - p[j_stroke_stroke]
            t_k_lodge = delta(w1-w2, s, m, p, u) / (u[j_stroke] * math.pow(np.dot(p_inter, p_inter), 2))
            t_k = min(1, t_k_lodge)

            # Меняем w1
            w1_new = w1 - t_k * u[j_stroke] * p_inter

            # Меняем все коэффициенты u
            u_new = u
            for j in range(len(u)):
                if j == j_stroke:
                    u_new[j_stroke] = (1 - t_k) * u[j_stroke]
                elif j == j_stroke_stroke:
                    u_new[j] += u[j_stroke_stroke] + t_k * u[j_stroke]
            return w1_new, w2, u_new
        else:
            # Определяем t_k
            p_inter = p[l_stroke] - p[l_stroke_stroke]
            t_k_lodge = delta(w1-w2, s, m, p, u) / (u[l_stroke] * math.pow(np.dot(p_inter, p_inter), 2))
            t_k = min(1, t_k_lodge)

            # Меняем w2
            w2_new = w2 - t_k * u[l_stroke] * p_inter

            # Меняем все коэффициенты u
            u_new = u
            for l in range(len(u)):
                if l == l_stroke:
                    u_new[l_stroke] = (1 - t_k) * u[l_stroke]
                elif l == l_stroke_stroke:
                    u_new[l] += u[l_stroke_stroke] + t_k * u[l_stroke]
            return w1, w2_new, u_new

def delta_u(w, p, i_stroke, i_stroke_stroke):
    return np.linalg.norm(w) ** 2 - np.dot(w, p[i_stroke] - p[i_stroke_stroke])

def e(dim, i) -> np.array:
    return np.array([int(i == j) for j in range(dim)])

def next_appr_gsk(p, w1, w2, s, m, u):
    w = w1 - w2

    indexes_for_min = [[np.dot(p[j], w), j] for j in range(s)]
    i_stroke = min(indexes_for_min)[1]

    indexes_for_max = [[np.dot(p[j], w), j] for j in range(s, m)]
    i_stroke_stroke = max(indexes_for_max)[1]

    delt = delta_u(w1 - w2, p, i_stroke, i_stroke_stroke)
    if delt == 0:
        return w1, w2, u
    else:
        lambda_k = min(1, delt / np.linalg.norm(w - p[i_stroke] + p[i_stroke_stroke]) ** 2)
        dim = len(u)
        u_new = (1 - lambda_k) * u + lambda_k * (e(dim, i_stroke) + e(dim, i_stroke_stroke))
        w1_new = sum([u_new[j] * p[j] for j in range(s)])
        w2_new = sum([u_new[j] * p[j] for j in range(s, m)])

        return w1_new, w2_new, u_new

