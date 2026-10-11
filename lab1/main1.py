import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

R = 5.0     
A = 2.0    
B = 0.5     
T_MAX = 4.0 

t = np.linspace(0, T_MAX, 400)
S = A*t + B*t**2
phi = S / R
V = A + 2*B*t
a_tau = 2*B
a_n = V**2 / R

idx = np.argmin(np.abs(a_tau - a_n))
t_eq = t[idx]

x = R*np.cos(phi)
y = R*np.sin(phi)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))


ax1.set_xlim(-R-1, R+1); ax1.set_ylim(-R-1, R+1)
ax1.set_aspect('equal'); ax1.grid(True)
theta = np.linspace(0, 2*np.pi, 200)
ax1.plot(R*np.cos(theta), R*np.sin(theta), 'k--', alpha=0.3)

point,  = ax1.plot([], [], 'ro', markersize=10)
vec_v,  = ax1.plot([], [], 'b-', lw=2, label='V')
vec_at, = ax1.plot([], [], 'g-', lw=2, label='a_τ')
vec_an, = ax1.plot([], [], 'm-', lw=2, label='a_n')
trail,  = ax1.plot([], [], 'r-', alpha=0.3, lw=1)
ax1.legend(loc='upper right')


ax2.plot(t, a_tau*np.ones_like(t), 'g-', label='a_τ = const')
ax2.plot(t, a_n, 'm-', label='a_n = V²/R')
ax2.axvline(t_eq, color='k', ls=':', alpha=0.6)
ax2.set_xlabel('t, с'); ax2.set_ylabel('a, м/с²')
ax2.grid(True); ax2.legend()
ax2.set_title(f'a_τ = a_n при t = {t_eq:.2f} с')

def update(i):
    point.set_data([x[i]], [y[i]])
    sv, sa = 1, 1
    
    vec_v.set_data([x[i], x[i] - np.sin(phi[i])*V[i]*sv],
                   [y[i], y[i] + np.cos(phi[i])*V[i]*sv])
    
    vec_at.set_data([x[i], x[i] - np.sin(phi[i])*a_tau*sa],
                    [y[i], y[i] + np.cos(phi[i])*a_tau*sa])

    vec_an.set_data([x[i], x[i] - np.cos(phi[i])*a_n[i]*sa],
                    [y[i], y[i] - np.sin(phi[i])*a_n[i]*sa])
    trail.set_data(x[:i+1], y[:i+1])
    return point, vec_v, vec_at, vec_an, trail

ani = FuncAnimation(fig, update, frames=len(t), interval=20, blit=True)
plt.tight_layout(); plt.show()