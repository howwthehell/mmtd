import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Arc

# ============================================================
# ПАРАМЕТРЫ ЗАДАЧИ
# ============================================================

m = 2.0          # масса диска, кг
R = 2.0          # радиус диска, м

# Момент инерции однородного диска
I = 0.5 * m * R**2

print("РЕЗУЛЬТАТ:")
print(f"Момент инерции I = {I:.2f} кг·м²")


# ============================================================
# ВРАЩЕНИЕ
# ============================================================

omega = 1.5      # угловая скорость, рад/с

T_MAX = 8
fps = 30

time = np.linspace(0, T_MAX, T_MAX * fps)

phi = omega * time


# ============================================================
# СОЗДАНИЕ ОКНА
# ============================================================

fig = plt.figure(figsize=(13, 7))

ax = fig.add_axes([0.05, 0.10, 0.62, 0.82])
graph = fig.add_axes([0.73, 0.55, 0.24, 0.32])

ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)

ax.set_aspect("equal")
ax.grid(True, alpha=0.2)

ax.set_xlabel("x, м")
ax.set_ylabel("y, м")

ax.set_title(
    "Момент инерции однородного диска",
    fontsize=14
)


# ============================================================
# ОСЬ ВРАЩЕНИЯ
# ============================================================

ax.plot(
    [0, 0],
    [-3, 3],
    linestyle="--",
    linewidth=1.5
)

ax.text(
    0.15,
    2.7,
    "ось вращения",
    fontsize=11
)


# ============================================================
# ДИСК
# ============================================================

disk = Circle(
    (0, 0),
    R,
    alpha=0.35
)

ax.add_patch(disk)


# ============================================================
# РАДИУС
# ============================================================

radius_line, = ax.plot(
    [],
    [],
    linewidth=2
)

radius_text = ax.text(
    0,
    0,
    r"$R$",
    fontsize=13
)


# ============================================================
# ЭЛЕМЕНТАРНОЕ КОЛЬЦО
# ============================================================

ring = Circle(
    (0, 0),
    1.25,
    fill=False,
    linewidth=2
)

ax.add_patch(ring)

dr_text = ax.text(
    0,
    0,
    r"$dr$",
    fontsize=12
)


# ============================================================
# ВЕКТОР УГЛОВОЙ СКОРОСТИ
# ============================================================

omega_arrow = ax.annotate(
    "",
    xy=(0, 2.8),
    xytext=(0, 1.7),
    arrowprops=dict(
        arrowstyle="->",
        linewidth=2
    )
)

omega_text = ax.text(
    0.15,
    2.25,
    r"$\omega$",
    fontsize=13
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
graph.set_ylim(0, omega * 1.3)

graph.set_xlabel("t, с")
graph.set_ylabel("ω, рад/с")

graph.set_title("Угловая скорость")
graph.grid(True, alpha=0.3)

omega_line = graph.plot([], [], linewidth=2)[0]
current_point = graph.plot([], [], "o")[0]


# ============================================================
# UPDATE
# ============================================================

def update(frame):

    angle = phi[frame]

    # ----------------------------------------
    # Радиус вращается вместе с диском
    # ----------------------------------------

    xR = R * np.cos(angle)
    yR = R * np.sin(angle)

    radius_line.set_data(
        [0, xR],
        [0, yR]
    )

    radius_text.set_position(
        (
            xR / 2 + 0.1,
            yR / 2 + 0.1
        )
    )


    # ----------------------------------------
    # Элементарное кольцо
    # ----------------------------------------

    ring_angle = angle

    ring_x = 1.25 * np.cos(ring_angle)
    ring_y = 1.25 * np.sin(ring_angle)

    dr_text.set_position(
        (
            ring_x + 0.1,
            ring_y + 0.1
        )
    )


    # ----------------------------------------
    # Информация
    # ----------------------------------------

    info.set_text(
        f"$m = {m}$ кг\n"
        f"$R = {R}$ м\n"
        f"$\\omega = {omega}$ рад/с\n\n"
        f"$I = \\frac{{1}}{{2}}mR^2$\n"
        f"$I = {I:.2f}$ кг·м²"
    )


    # ----------------------------------------
    # График
    # ----------------------------------------

    omega_line.set_data(
        time[:frame + 1],
        np.full(frame + 1, omega)
    )

    current_point.set_data(
        [time[frame]],
        [omega]
    )

    return (
        disk,
        radius_line,
        radius_text,
        ring,
        dr_text,
        omega_arrow,
        omega_text,
        info,
        omega_line,
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