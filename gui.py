import time
import tkinter as tk
import threading
from PIL import Image, ImageTk

from main import *


class StartFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background="#FFFFFF")

        self.thr2 = threading.Thread()
        self.thr1 = threading.Thread()
        self.parent = parent

        # Фрейм для настроек
        left_frame = tk.Frame(self, background="#FFFFFF", height=600, width=400)
        left_frame.pack(side="left", expand=1, fill="both")

        # Кнопки выбора алгоритма
        self.var = tk.IntVar()
        self.var.set(1)
        radiobuttonMDM = tk.Radiobutton(left_frame, text="МДМ метод", value=1, variable=self.var,
                                        background="#FFFFFF", font=("Times New Roman", 16),
                                        activebackground="#FFFFFF")
        radiobuttonMDM.pack(anchor="w", padx=10, pady=(10, 5))
        radiobuttonGSK = tk.Radiobutton(left_frame, text="Метод условного градиента", value=2, variable=self.var,
                                        background="#FFFFFF", font=("Times New Roman", 16),
                                        activebackground="#FFFFFF")
        radiobuttonGSK.pack(anchor="w", padx=10, pady=5)

        # Список точек на каждой итерации
        list_of_points_frame = tk.Frame(left_frame, background="#FFFFFF", height=300, width=300)
        list_of_points_frame.pack(anchor="w", padx=10, pady=5)

        # Текстовый блок для отображения списка точек
        self.list_of_points = []
        self.points_var = tk.Variable(value=["Здесь будет отображаться список точек"])
        listbox = tk.Listbox(list_of_points_frame,
                             relief="solid",
                             border=2,
                             font=("Times New Roman", 12),
                             selectbackground="#E8E8E8",
                             listvariable=self.points_var,
                             width=35,
                             height=15)
        listbox.pack(anchor="sw", side="left", fill="both", padx=5, pady=5)

        scrollbar = tk.Scrollbar(list_of_points_frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(anchor="sw", side="right", fill="y", padx=(5, 11), pady=5)
        listbox["yscrollcommand"] = scrollbar.set

        # Фрейм для количества итераций
        frame_for_iter = tk.Frame(left_frame, background="#FFFFFF")
        frame_for_iter.pack(anchor="w", padx=10, pady=5)

        label1 = tk.Label(frame_for_iter, text="Количество итераций:", font=("Times New Roman", 16),
                          background="#FFFFFF")
        label1.pack(side="left", padx=5)

        self.count_of_iter = tk.IntVar()
        entry = tk.Entry(frame_for_iter, font=("Times New Roman", 16), width=9, textvariable=self.count_of_iter,
                         border=2, relief="solid")
        entry.pack(side="right", padx=5)

        # Фрейм для количества кадров в секунду
        frame_for_count_of_frames = tk.Frame(left_frame, background="#FFFFFF")
        frame_for_count_of_frames.pack(anchor="w", padx=10, pady=5)

        label2 = tk.Label(frame_for_count_of_frames, text="Количество кадров в сек.:", font=("Times New Roman", 16),
                          background="#FFFFFF")
        label2.pack(side="left", padx=5)

        self.count_of_frames = tk.IntVar()
        entry = tk.Entry(frame_for_count_of_frames, font=("Times New Roman", 16), width=6,
                         textvariable=self.count_of_frames,
                         border=2, relief="solid")
        entry.pack(side="right", padx=5)

        # Кнопка начала программы
        button = tk.Button(left_frame, font=("Times New Roman", 16), text="Start", background="#FFFFFF",
                           relief="solid", activebackground="#FFFFFF", width=26, height=2,
                           command=lambda: self.start(self.count_of_iter.get(), self.count_of_frames.get(),
                                                      self.var.get()))
        button.pack(anchor="w", padx=10, pady=5)

        # Фрейм для графика
        right_frame = tk.Frame(self, background="#FFFFFF", height=600, width=600)
        right_frame.pack(side="right", expand=1, fill="both")

        # График
        self.image = Image.open("example.png")
        self.imageTk = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(right_frame, image=self.imageTk, background="#FFFFFF", relief="solid",
                              border=2)
        self.label.pack(fill="both", expand=1)
        time.sleep(0.000001)
        self.set_window()
        self.pack(expand=1, fill="both")

    def start(self, count_of_iters, count_of_frames, algorithm):

        # Очищаем список точек
        self.list_of_points = []

        p1 = np.array([[1, 1], [0, 1], [0, 0], [1, 0], [1, 1]])
        p2 = np.array([[2, 2], [1, 2], [0, 2], [2, 1.5], [2, 2]])

        # Множество всех точек
        p = np.concatenate([p1, p2])
        # Размерность пространства
        dim = len(p1[0])
        # Количество элементов множества p1
        s = len(p1)
        # Количество элементов множества p
        m = len(p)
        # Начальные коэффициенты в приближении,
        # при которых в равной степени учитываются
        # все вектора оболочек p1 и p2
        u = np.array([1 / s for _ in range(s)] + [1 / (m - s) for _ in range(m - s)])
        u1 = np.concatenate([[u] for _ in range(dim)]).T
        # Определяем начальные вектора w1 и w2
        w1 = np.array([np.sum([p[0:s] * u1[0:s]], axis=1)]).flatten()
        w2 = np.array([np.sum([p[s:m] * u1[s:m]], axis=1)]).flatten()

        # Сохраняем первое приближение
        save_graphic(p1, p2, np.array([w1, w2]))

        # Добавляем в список точек - начальную точку
        self.list_of_points.append([w1, w2])

        # Запускаем поток, который будет обновлять
        # картинку и список точек на экране
        self.thr1 = threading.Thread(target=self.reload_image, args=(count_of_frames,),
                                     name="thr-1", daemon=True)
        self.thr1.start()

        # Запускаем поток, который будет
        # выполнять итерации алгоритма
        self.thr2 = threading.Thread(target=self.next_iter, args=(p, p1, p2, w1, w2, s, m, u, count_of_iters, algorithm, ),
                                     name="thr-2", daemon=True)
        self.thr2.start()

    def next_iter(self, p, p1, p2, w1, w2, s, m, u, count_of_iters, algorithm):
        while True:
            global current_number_of_iter

            if current_number_of_iter < count_of_iters:
                if algorithm == 1:
                    w1, w2, u = next_appr_mdm(p, w1, w2, s, m, u)
                else:
                    w1, w2, u = next_appr_gsk(p, w1, w2, s, m, u)
                save_graphic(p1, p2, np.array([w1, w2]))
                self.list_of_points.append([w1, w2])

                current_number_of_iter += 1

            time.sleep(0.000001)

    def reload_image(self, count_of_frames):
        while True:
            global current_number_of_point

            if current_number_of_point + 1 <= len(self.list_of_points):
                self.image = Image.open(f"images\\image{current_number_of_point}.png")
                self.imageTk = ImageTk.PhotoImage(self.image)
                self.label["image"] = self.imageTk
                self.points_var.set(self.list_of_points[:current_number_of_point])

                current_number_of_point += 1

            time.sleep(1. / count_of_frames)


    def set_window(self):
        width = 1000
        height = 600

        self.parent.title("Алгоритмы MVP")
        self.parent.config(bg="#FFFFFF")

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - width) / 2
        y = (screen_height - height) / 2

        self.parent.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.parent.resizable(False, False)


def main():
    window = tk.Tk()
    StartFrame(window)
    window.mainloop()


if __name__ == "__main__":
    current_number_of_point = 0
    current_number_of_iter = 0
    main()
