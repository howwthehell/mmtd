import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D


m1 = 2.0          
m2 = 1.0         

F = 12.0         
alpha = 25        
mu = 0.15        
g = 9.81          

alpha_rad = np.radians(alpha)

Fx = F * np.cos(alpha_rad)
Fy = F * np.sin(alpha_rad)


N1 = m1 * g - Fy
N2 = m2 * g


Ftr1 = mu * N1
Ftr2 = mu * N2


a = (Fx - Ftr1 - Ftr2) / (m1 + m2)


T = m2 * a + Ftr2

print("РЕЗУЛЬТАТ:")
print(f"Ускорение a = {a:.2f} м/с²")
print(f"Натяжение T = {T:.2f} Н")


T_MAX = 4
fps = 30

time = np.linspace(0, T_MAX, T_MAX * fps)


x0 = 1.0


x = x0 + 0.5 * a * time**2
v = a * time

fig = plt.figure(figsize=(15, 8))

ax = fig.add_axes([0.05, 0.10, 0.62, 0.82])
graph = fig.add_axes([0.73, 0.55, 0.24, 0.32])

ax.set_xlim(-2, 25)
ax.set_ylim(-2.5, 5.5)

ax.set_aspect("equal")
ax.grid(True, alpha=0.2)

ax.set_xlabel("x, м")
ax.set_ylabel("y, м")

ax.set_title(
    "Динамика двух связанных тел\n"
    "Второй закон Ньютона",
    fontsize=14
)

# ============================================================
# ПОВЕРХНОСТЬ
# ============================================================

ground = ax.plot(
    [-2, 25],
    [0, 0],
    linewidth=3
)[0]

# ============================================================
# ТЕЛА
# ============================================================

body1 = Rectangle(
    (x0, 0),
    1.5,
    1.0
)

body2 = Rectangle(
    (x0 + 3.2, 0),
    1.5,
    1.0
)

ax.add_patch(body1)
ax.add_patch(body2)

# Подписи тел
label1 = ax.text(
    x0 + 0.75,
    0.5,
    r"$m_1$",
    fontsize=14,
    ha="center",
    va="center"
)

label2 = ax.text(
    x0 + 3.95,
    0.5,
    r"$m_2$",
    fontsize=14,
    ha="center",
    va="center"
)

# ============================================================
# НИТЬ
# ============================================================

rope = ax.plot(
    [],
    [],
    linewidth=2
)[0]

# ============================================================
# ФУНКЦИЯ ДЛЯ ВЕКТОРОВ
# ============================================================

def draw_arrow(start, vector, label, color, text_offset=(0, 0)):

    x_start, y_start = start
    dx, dy = vector

    arrow = ax.annotate(
        "",
        xy=(x_start + dx, y_start + dy),
        xytext=(x_start, y_start),
        arrowprops=dict(
            arrowstyle="->",
            linewidth=2,
            color=color
        )
    )

    text = ax.text(
        x_start + dx / 2 + text_offset[0],
        y_start + dy / 2 + text_offset[1],
        label,
        fontsize=12,
        color=color,
        ha="center",
        va="center",
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.8
        )
    )

    return arrow, text


F_arrow, F_text = draw_arrow(
    (x0 + 0.75, 0.7),
    (
        2.0 * np.cos(alpha_rad),
        2.0 * np.sin(alpha_rad)
    ),
    r"$F$",
    "red",
    (0.0, 0.25)
)

T1_arrow, T1_text = draw_arrow(
    (x0 + 1.5, 0.5),
    (-1.3, 0),
    r"$T$",
    "purple",
    (0, 0.25)
)

N1_arrow, N1_text = draw_arrow(
    (x0 + 0.75, 0),
    (0, 1.2),
    r"$N_1$",
    "green",
    (0.35, 0)
)

mg1_arrow, mg1_text = draw_arrow(
    (x0 + 0.75, 0.0),
    (0, -1.5),
    r"$m_1g$",
    "blue",
    (0.4, 0)
)

Ftr1_arrow, Ftr1_text = draw_arrow(
    (x0 + 0.1, 0.3),
    (-1.2, 0),
    r"$F_{\rm тр1}$",
    "orange",
    (0, -0.25)
)

a1_arrow, a1_text = draw_arrow(
    (x0 + 0.75, 1.0),
    (1.4, 0),
    r"$a$",
    "black",
    (0, 0.25)
)

T2_arrow, T2_text = draw_arrow(
    (x0 + 3.2, 0.5),
    (1.3, 0),
    r"$T$",
    "purple",
    (0, 0.25)
)

N2_arrow, N2_text = draw_arrow(
    (x0 + 3.95, 0),
    (0, 1.2),
    r"$N_2$",
    "green",
    (0.35, 0)
)

mg2_arrow, mg2_text = draw_arrow(
    (x0 + 3.95, 0),
    (0, -1.5),
    r"$m_2g$",
    "blue",
    (0.4, 0)
)

Ftr2_arrow, Ftr2_text = draw_arrow(
    (x0 + 4.6, 0.3),
    (-1.2, 0),
    r"$F_{\rm тр2}$",
    "orange",
    (0, -0.25)
)

a2_arrow, a2_text = draw_arrow(
    (x0 + 3.95, 1.0),
    (1.4, 0),
    r"$a$",
    "black",
    (0, 0.25)
)


x_axis = ax.annotate(
    "",
    xy=(5, -1.6),
    xytext=(1, -1.6),
    arrowprops=dict(
        arrowstyle="->",
        linewidth=1.5
    )
)

x_axis_text = ax.text(
    5.2,
    -1.6,
    "$Ox$",
    fontsize=12
)


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


graph.set_xlim(0, T_MAX)
graph.set_ylim(
    0,
    max(v) * 1.2
)

graph.set_xlabel("t, с")
graph.set_ylabel("v, м/с")

graph.set_title("Скорость")

graph.grid(True, alpha=0.3)

velocity_line = graph.plot([], [], linewidth=2)[0]
current_point = graph.plot([], [], "o")[0]


def update(frame):

    current_x = x[frame]
    
    body1.set_xy(
        (current_x, 0)
    )

    body2.set_xy(
        (current_x + 3.2, 0)
    )

    label1.set_position(
        (current_x + 0.75, 0.5)
    )

    label2.set_position(
        (current_x + 3.95, 0.5)
    )

    rope.set_data(
        [
            current_x + 1.5,
            current_x + 3.2
        ],
        [
            0.5,
            0.5
        ]
    )


    def move_arrow(arrow, text, start, vector):

        sx, sy = start
        dx, dy = vector

        arrow.xy = (
            sx + dx,
            sy + dy
        )

        arrow.set_position(
            (sx, sy)
        )

        text.set_position(
            (
                sx + dx / 2 + text.get_position()[0] - text.get_position()[0],
                sy + dy / 2
            )
        )


    F_start = (
        current_x + 0.75,
        0.7
    )

    F_end = (
        F_start[0] + 2 * np.cos(alpha_rad),
        F_start[1] + 2 * np.sin(alpha_rad)
    )

    F_arrow.xy = F_end
    F_arrow.set_position(F_start)

    F_text.set_position(
        (
            (F_start[0] + F_end[0]) / 2,
            (F_start[1] + F_end[1]) / 2 + 0.25
        )
    )


    vectors = [
        (
            T1_arrow,
            T1_text,
            (current_x + 1.5, 0.5),
            (-1.3, 0),
            (0, 0.25)
        ),

        (
            N1_arrow,
            N1_text,
            (current_x + 0.75, 0),
            (0, 1.2),
            (0.35, 0)
        ),

        (
            mg1_arrow,
            mg1_text,
            (current_x + 0.75, 0),
            (0, -1.5),
            (0.4, 0)
        ),

        (
            Ftr1_arrow,
            Ftr1_text,
            (current_x + 0.1, 0.3),
            (-1.2, 0),
            (0, -0.25)
        ),

        (
            a1_arrow,
            a1_text,
            (current_x + 0.75, 1),
            (1.4, 0),
            (0, 0.25)
        ),

        (
            T2_arrow,
            T2_text,
            (current_x + 3.2, 0.5),
            (1.3, 0),
            (0, 0.25)
        ),

        (
            N2_arrow,
            N2_text,
            (current_x + 3.95, 0),
            (0, 1.2),
            (0.35, 0)
        ),

        (
            mg2_arrow,
            mg2_text,
            (current_x + 3.95, 0),
            (0, -1.5),
            (0.4, 0)
        ),

        (
            Ftr2_arrow,
            Ftr2_text,
            (current_x + 4.6, 0.3),
            (-1.2, 0),
            (0, -0.25)
        ),

        (
            a2_arrow,
            a2_text,
            (current_x + 3.95, 1),
            (1.4, 0),
            (0, 0.25)
        )
    ]

    for arrow, text, start, vector, offset in vectors:

        sx, sy = start
        dx, dy = vector

        arrow.xy = (
            sx + dx,
            sy + dy
        )

        arrow.set_position(
            start
        )

        text.set_position(
            (
                sx + dx / 2 + offset[0],
                sy + dy / 2 + offset[1]
            )
        )


    velocity_line.set_data(
        time[:frame + 1],
        v[:frame + 1]
    )

    current_point.set_data(
        [time[frame]],
        [v[frame]]
    )

    # ----------------------------------------
    # Информация
    # ----------------------------------------

    info.set_text(
        f"$m_1 = {m1}$ кг     $m_2 = {m2}$ кг\n"
        f"$F = {F}$ Н     $\\alpha = {alpha}^\\circ$\n"
        f"$\\mu = {mu}$\n\n"
        f"$a = {a:.2f}$ м/с²\n"
        f"$T = {T:.2f}$ Н"
    )

    return (
        body1,
        body2,
        rope,
        label1,
        label2,
        velocity_line,
        current_point,
        info
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