import numpy as np
from MassSim.masses import Particle, Particles
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


def two_body_orbit(G: float = 1):
    r1 = np.array([8, 15])
    r2 = np.array([8, 8])
    m1 = 1
    m2 = 100
    dist = np.linalg.norm(r2 - r1)
    # see formula for orbital velocity of a small mass around a large
    # not perfect in this case since the moon's mass is not negligible (a bit over 1%) but works closely
    dx1 = (G * m2 / dist) ** 0.5
    dx2 = 0
    dy1 = 0
    dy2 = 0
    v1 = [dx1, dy1]
    v2 = [dx2, dy2]
    p1 = Particle(r1, v1, m1)
    p2 = Particle(r2, v2, m2)
    return [p1, p2]


particles = Particles(two_body_orbit(G=1), G=1)
fig, ax = plt.subplots()
ax.set_xlim(0, 30)
ax.set_ylim(0, 16)
earth, = ax.plot(-100, -100, color="green", marker="o", markersize=4)
moon, = ax.plot(-100, -100, color="grey", marker="o", markersize=1)
moonline, = ax.plot(0, 0, color="black", linestyle="dashed", linewidth=1)
earthline, = ax.plot(0, 0, color="grey", linewidth=1)
x_data = []
y_data = []


def animate(i):
    this_x = [p.pos[0] for p in particles.particles]
    this_y = [p.pos[1] for p in particles.particles]
    x_data.append(this_x)
    y_data.append(this_y)

    for j in range(200):
        particles.displace(h=0.001)

    moonline.set_data(np.array(x_data).T[0, :i], np.array(y_data).T[0, :i])
    earthline.set_data(np.array(x_data).T[1, :i], np.array(y_data).T[1, :i])
    moon.set_data(this_x[0], this_y[0])
    earth.set_data(this_x[1], this_y[1])

    return moonline, earthline, moon, earth


animation = FuncAnimation(fig, func=animate, interval=100, blit=True)
plt.show()
