import numpy as np
from MassSim.masses import Particle, Particles
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


def figure_eight():
    vals = [-0.0347,
            1.1856,
            0.2693,
            -1.0020,
            -0.2328,
            -0.5978,
            0.2495,
            -0.1076,
            0.2059,
            -0.9396,
            -0.4553,
            1.0471]

    r1 = vals[0:2]
    r2 = vals[2:4]
    r3 = vals[4:6]
    v1 = vals[6:8]
    v2 = vals[8:10]
    v3 = vals[10:12]
    p1 = Particle(r1, v1)
    p2 = Particle(r2, v2)
    p3 = Particle(r3, v3)
    return [p1, p2, p3]


particles = Particles(figure_eight(), G=1)
fig, ax = plt.subplots()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
bod1, = ax.plot(-100, -100, color="green", marker="o", markersize=4)
bod2, = ax.plot(-100, -100, color="red", marker="o", markersize=4)
bod3, = ax.plot(-100, -100, color="black", marker="o", markersize=4)
bod1l, = ax.plot(0, 0, color="green", linestyle="dashed", linewidth=1)
bod2l, = ax.plot(0, 0, color="red", linestyle="dashed", linewidth=1)
bod3l, = ax.plot(0, 0, color="black", linestyle="dashed", linewidth=1)
x_data = []
y_data = []


def animate(i):
    this_x = [p.pos[0] for p in particles.particles]
    this_y = [p.pos[1] for p in particles.particles]
    x_data.append(this_x)
    y_data.append(this_y)

    for j in range(200):
        # much smaller step was needed for this system to have a stable simulation
        # certainly would be more pleasant to work out the period, create the array of x and y values, then repeat the animation (not done here for consistency's sake)
        particles.displace(h=0.0001)

    bod1l.set_data(np.array(x_data).T[0, :i], np.array(y_data).T[0, :i])
    bod2l.set_data(np.array(x_data).T[1, :i], np.array(y_data).T[1, :i])
    bod3l.set_data(np.array(x_data).T[2, :i], np.array(y_data).T[2, :i])
    bod1.set_data(this_x[0], this_y[0])
    bod2.set_data(this_x[1], this_y[1])
    bod3.set_data(this_x[2], this_y[2])

    return bod1l, bod2l, bod3l, bod1, bod2, bod3


animation = FuncAnimation(fig, func=animate, interval=100, blit=True)
plt.show()
