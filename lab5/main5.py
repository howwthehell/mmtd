import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle


# =========================
# ФИЗИЧЕСКИЕ ДАННЫЕ
# =========================

m1 = 2.0
m2 = 1.0

R1 = 1.4
R2 = 1.4

I1 = 2.0
I2 = 1.0

omega1 = 3.0
omega2 = -1.0

# Закон сохранения момента импульса:
omega_final = (
    I1 * omega1 + I2 * omega2
) / (I1 + I2)


# =========================
# НАСТРОЙКА СЦЕНЫ
# =========================

fig, ax = plt.subplots(figsize=(11, 6))

ax.set_xlim(-6, 6)
ax.set_ylim(-4, 4)

ax.set_aspect('equal')

ax.set_xlabel("x, м")
ax.set_ylabel("y, м")

ax.set_title(
    "Закон сохранения момента импульса при столкновении дисков"
)

ax.grid(True, alpha=0.25)


# =========================
# ДИСКИ
# =========================

disk1 = Circle(
    (-3.5, 0),
    R1,
    fill=False,
    linewidth=2.5
)

disk2 = Circle(
    (3.5, 0),
    R2,
    fill=False,
    linewidth=2.5
)

ax.add_patch(disk1)
ax.add_patch(disk2)


# =========================
# СПИЦЫ
# =========================

num_spokes = 8

spokes1 = []
spokes2 = []

for i in range(num_spokes):

    angle = 2 * np.pi * i / num_spokes

    line1, = ax.plot(
        [0, 0],
        [0, 0],
        linewidth=1.5
    )

    line2, = ax.plot(
        [0, 0],
        [0, 0],
        linewidth=1.5
    )

    spokes1.append(line1)
    spokes2.append(line2)


# =========================
# ПОДПИСИ ДИСКОВ
# =========================

text1 = ax.text(
    -3.5,
    -2.0,
    r"$m_1 = 2$ кг,  $I_1 = 2$ кг·м$^2$",
    ha="center",
    fontsize=11
)

text2 = ax.text(
    3.5,
    -2.0,
    r"$m_2 = 1$ кг,  $I_2 = 1$ кг·м$^2$",
    ha="center",
    fontsize=11
)


# =========================
# УГЛОВЫЕ СКОРОСТИ
# =========================

omega_text1 = ax.text(
    -3.5,
    2.0,
    r"$\omega_1 = 3$ рад/с",
    ha="center",
    fontsize=12
)

omega_text2 = ax.text(
    3.5,
    2.0,
    r"$\omega_2 = -1$ рад/с",
    ha="center",
    fontsize=12
)


# =========================
# ИНФОРМАЦИЯ
# =========================

info = ax.text(
    -5.7,
    3.1,
    r"$L = I_1\omega_1 + I_2\omega_2 = const$"
    + "\n"
    + r"$\omega = "
    + f"{omega_final:.1f}"
    + r"$ рад/с",
    fontsize=12,
    bbox=dict(
        boxstyle="round",
        alpha=0.15
    )
)


# =========================
# НАДПИСЬ СОСТОЯНИЯ
# =========================

state_text = ax.text(
    0,
    -3.2,
    "Диски вращаются независимо",
    ha="center",
    fontsize=13
)


# =========================
# ПАРАМЕТРЫ ДВИЖЕНИЯ
# =========================

T_APPROACH = 3.0
T_MAX = 6.0

FPS = 30

frames = int(T_MAX * FPS)


# Начальные и конечные координаты центров

x1_start = -3.5
x2_start = 3.5

x1_contact = -R1
x2_contact = R2


# =========================
# АНИМАЦИЯ
# =========================

def update(frame):

    t = frame / FPS

    # ---------------------------------
    # 1. Сближение дисков
    # ---------------------------------

    if t < T_APPROACH:

        progress = t / T_APPROACH

        x1 = x1_start + (
            x1_contact - x1_start
        ) * progress

        x2 = x2_start + (
            x2_contact - x2_start
        ) * progress

        # Каждый диск пока вращается
        # со своей начальной скоростью

        angle1 = omega1 * t
        angle2 = omega2 * t

        current_omega1 = omega1
        current_omega2 = omega2

        state_text.set_text(
            "Диски сближаются"
        )

    # ---------------------------------
    # 2. После столкновения
    # ---------------------------------

    else:

        x1 = x1_contact
        x2 = x2_contact

        contact_time = T_APPROACH

        # Угол, накопленный до столкновения

        angle1_contact = omega1 * contact_time
        angle2_contact = omega2 * contact_time

        # После столкновения оба диска
        # вращаются с общей угловой скоростью

        angle1 = (
            angle1_contact
            + omega_final * (t - contact_time)
        )

        angle2 = (
            angle2_contact
            + omega_final * (t - contact_time)
        )

        current_omega1 = omega_final
        current_omega2 = omega_final

        state_text.set_text(
            r"После столкновения: "
            r"$\omega_1 = \omega_2 = \omega$"
        )

    # ---------------------------------
    # Положение дисков
    # ---------------------------------

    disk1.center = (x1, 0)
    disk2.center = (x2, 0)

    # ---------------------------------
    # Спицы первого диска
    # ---------------------------------

    for i, line in enumerate(spokes1):

        initial_angle = (
            2 * np.pi * i / num_spokes
        )

        current_angle = (
            initial_angle + angle1
        )

        line.set_data(
            [
                x1,
                x1 + R1 * np.cos(current_angle)
            ],
            [
                0,
                R1 * np.sin(current_angle)
            ]
        )

    # ---------------------------------
    # Спицы второго диска
    # ---------------------------------

    for i, line in enumerate(spokes2):

        initial_angle = (
            2 * np.pi * i / num_spokes
        )

        current_angle = (
            initial_angle + angle2
        )

        line.set_data(
            [
                x2,
                x2 + R2 * np.cos(current_angle)
            ],
            [
                0,
                R2 * np.sin(current_angle)
            ]
        )

    # ---------------------------------
    # Позиции подписей
    # ---------------------------------

    text1.set_position(
        (x1, -2.0)
    )

    text2.set_position(
        (x2, -2.0)
    )

    omega_text1.set_position(
        (x1, 2.0)
    )

    omega_text2.set_position(
        (x2, 2.0)
    )

    # ---------------------------------
    # Текущие значения угловых скоростей
    # ---------------------------------

    if t < T_APPROACH:

        omega_text1.set_text(
            r"$\omega_1 = 3$ рад/с"
        )

        omega_text2.set_text(
            r"$\omega_2 = -1$ рад/с"
        )

    else:

        omega_text1.set_text(
            rf"$\omega = {omega_final:.1f}$ рад/с"
        )

        omega_text2.set_text(
            rf"$\omega = {omega_final:.1f}$ рад/с"
        )

    return (
        [disk1, disk2]
        + spokes1
        + spokes2
        + [
            text1,
            text2,
            omega_text1,
            omega_text2,
            state_text
        ]
    )


animation = FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=1000 / FPS,
    blit=False
)

plt.show()