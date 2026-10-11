import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Rectangle

# ============================================================
# ПАРАМЕТРЫ ЗАДАЧИ
# ============================================================

m0 = 2.0        # масса блока, кг
m1 = 3.0        # масса первого груза, кг
m2 = 1.0        # масса второго груза, кг

R = 1.0         # радиус блока, м
g = 9.81        # ускорение свободного падения, м/с²

# Момент инерции однородного диска
I = 0.5 * m0 * R**2

# Ускорение системы
a = (m1 - m2) * g / (
    m1 + m2 + I / R**2
)

# Угловое ускорение блока
beta = a / R

# Натяжения нитей
T1 = m1 * (g - a)
T2 = m2 * (g + a)

print("РЕЗУЛЬТАТ:")
print(f"Ускорение a = {a:.2f} м/с²")
print(f"Угловое ускорение β = {beta:.2f} рад/с²")
print(f"T1 = {T1:.2f} Н")
print(f"T2 = {T2:.2f} Н")


# ============================================================
# ВРЕМЯ И ДВИЖЕНИЕ
# ============================================================

T_MAX = 4
fps = 30

time = np.linspace(0, T_MAX, T_MAX * fps)

# Максимальный путь ограничим визуально
s = 0.5 * a * time**2

# Скорость
v = a * time

# Угол вращения блока
phi = beta * time**2 / 2


# ============================================================
# СОЗДАНИЕ ОКНА
# ============================================================

fig = plt.figure(figsize=(14, 8))

ax = fig.add_axes([0.05, 0.10, 0.62, 0.82])
graph = fig.add_axes([0.73, 0.55, 0.24, 0.32])

ax.set_xlim(-5, 5)
ax.set_ylim(-6, 5)

ax.set_aspect("equal")
ax.grid(True, alpha=0.2)

ax.set_xlabel("x, м")
ax.set_ylabel("y, м")

ax.set_title(
    "Динамика вращательного движения\n"
    "Грузы и массивный блок",
    fontsize=14
)


# ============================================================
# БЛОК
# ============================================================

pulley_center = (0, 2.5)

pulley = Circle(
    pulley_center,
    R,
    alpha=0.35
)

ax.add_patch(pulley)


# Ось блока
ax.plot(
    [-0.2, 0.2],
    [2.5, 2.5],
    linewidth=3
)


# ============================================================
# ГРУЗЫ
# ============================================================

block_width = 1.0
block_height = 1.0

mass1 = Rectangle(
    (-3.0, 0),
    block_width,
    block_height
)

mass2 = Rectangle(
    (2.0, 0),
    block_width,
    block_height
)

ax.add_patch(mass1)
ax.add_patch(mass2)


# ============================================================
# НИТЬ
# ============================================================

rope_left, = ax.plot([], [], linewidth=2)
rope_right, = ax.plot([], [], linewidth=2)


# ============================================================
# ПОДПИСИ ГРУЗОВ
# ============================================================

label1 = ax.text(
    -2.5,
    0.5,
    r"$m_1$",
    fontsize=14,
    ha="center",
    va="center"
)

label2 = ax.text(
    2.5,
    0.5,
    r"$m_2$",
    fontsize=14,
    ha="center",
    va="center"
)


# ============================================================
# ВЕКТОРЫ СИЛ
# ============================================================

# Для первого груза: mg вниз
mg1_arrow = ax.annotate(
    "",
    xy=(-2.5, -1.3),
    xytext=(-2.5, 0),
    arrowprops=dict(
        arrowstyle="->",
        linewidth=2
    )
)

mg1_text = ax.text(
    -2.85,
    -0.5,
    r"$m_1g$",
    fontsize=12
)


# Для второго груза: mg вниз
mg2_arrow = ax.annotate(
    "",
    xy=(2.5, -1.3),
    xytext=(2.5, 0),
    arrowprops=dict(
        arrowstyle="->",
        linewidth=2
    )
)

mg2_text = ax.text(
    2.8,
    -0.5,
    r"$m_2g$",
    fontsize=12
)


# Натяжение T1 вверх
T1_arrow = ax.annotate(
    "",
    xy=(-2.5, 2.0),
    xytext=(-2.5, 1.0),
    arrowprops=dict(
        arrowstyle="->",
        linewidth=2
    )
)

T1_text = ax.text(
    -2.9,
    1.5,
    r"$T_1$",
    fontsize=12
)


# Натяжение T2 вверх
T2_arrow = ax.annotate(
    "",
    xy=(2.5, 2.0),
    xytext=(2.5, 1.0),
    arrowprops=dict(
        arrowstyle="->",
        linewidth=2
    )
)

T2_text = ax.text(
    2.8,
    1.5,
    r"$T_2$",
    fontsize=12
)


# ============================================================
# УГЛОВАЯ СКОРОСТЬ БЛОКА
# ============================================================

omega_arrow = ax.annotate(
    "",
    xy=(0, 4.3),
    xytext=(0.9, 3.7),
    arrowprops=dict(
        arrowstyle="->",
        linewidth=2
    )
)

omega_text = ax.text(
    0.9,
    4.0,
    r"$\beta$",
    fontsize=12
)


# ============================================================
# ИНФОРМАЦИЯ
# ============================================================

info = ax.text(
    0.02,
    0.97,
    "",
    transform=ax.transAxes,
    fontsize=12,
    verticalalignment="top",
    bbox=dict(
        facecolor="white",
        alpha=0.9
    )
)


# ============================================================
# ГРАФИК
# ============================================================

graph.set_xlim(0, T_MAX)
graph.set_ylim(0, max(v) * 1.2)

graph.set_xlabel("t, с")
graph.set_ylabel("v, м/с")

graph.set_title("Скорость груза m₁")

graph.grid(True, alpha=0.3)

velocity_line = graph.plot([], [], linewidth=2)[0]
current_point = graph.plot([], [], "o")[0]


# ============================================================
# UPDATE
# ============================================================

def update(frame):

    current_s = s[frame]

    # ----------------------------------------
    # Движение грузов
    # ----------------------------------------

    y1 = current_s
    y2 = -current_s

    mass1.set_xy(
        (-3.0, y1)
    )

    mass2.set_xy(
        (2.0, y2)
    )


    # ----------------------------------------
    # Подписи грузов
    # ----------------------------------------

    label1.set_position(
        (-2.5, y1 + 0.5)
    )

    label2.set_position(
        (2.5, y2 + 0.5)
    )


    # ----------------------------------------
    # Нити
    # ----------------------------------------

    rope_left.set_data(
        [-2.5, -1.0],
        [y1 + 1, 2.5]
    )

    rope_right.set_data(
        [1.0, 2.5],
        [2.5, y2 + 1]
    )


    # ----------------------------------------
    # Векторы сил двигаются вместе с грузами
    # ----------------------------------------

    # m1g
    mg1_arrow.xy = (-2.5, y1 - 1.3)
    mg1_arrow.set_position(
        (-2.5, y1)
    )

    mg1_text.set_position(
        (-2.85, y1 - 0.7)
    )


    # T1
    T1_arrow.xy = (-2.5, y1 + 2)
    T1_arrow.set_position(
        (-2.5, y1 + 1)
    )

    T1_text.set_position(
        (-2.9, y1 + 1.5)
    )


    # m2g
    mg2_arrow.xy = (2.5, y2 - 1.3)
    mg2_arrow.set_position(
        (2.5, y2)
    )

    mg2_text.set_position(
        (2.8, y2 - 0.7)
    )


    # T2
    T2_arrow.xy = (2.5, y2 + 2)
    T2_arrow.set_position(
        (2.5, y2 + 1)
    )

    T2_text.set_position(
        (2.8, y2 + 1.5)
    )


    # ----------------------------------------
    # Информация
    # ----------------------------------------

    info.set_text(
        f"$m_0 = {m0}$ кг\n"
        f"$m_1 = {m1}$ кг     $m_2 = {m2}$ кг\n"
        f"$R = {R}$ м\n\n"
        f"$a = {a:.2f}$ м/с²\n"
        f"$\\beta = {beta:.2f}$ рад/с²\n"
        f"$T_1 = {T1:.2f}$ Н\n"
        f"$T_2 = {T2:.2f}$ Н"
    )


    # ----------------------------------------
    # График
    # ----------------------------------------

    velocity_line.set_data(
        time[:frame + 1],
        v[:frame + 1]
    )

    current_point.set_data(
        [time[frame]],
        [v[frame]]
    )

    return (
        pulley,
        mass1,
        mass2,
        rope_left,
        rope_right,
        label1,
        label2,
        mg1_arrow,
        mg1_text,
        T1_arrow,
        T1_text,
        mg2_arrow,
        mg2_text,
        T2_arrow,
        T2_text,
        omega_arrow,
        omega_text,
        info,
        velocity_line,
        current_point
    )


# ============================================================
# АНИМАЦИЯ
# ============================================================

animation = FuncAnimation(
    fig,
    update,
    frames=len(time),
    interval=1000 / fps,
    blit=False
)

plt.show()