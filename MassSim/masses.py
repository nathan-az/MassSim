import numpy as np
from typing import List, Dict


class Particle():
    def __init__(self, pos: List[float] = [0, 0, 0], vel: List[float] = [0, 0, 0], mass=1):
        # pos and vel in vector form, stored as numpy arrays for ease of calculations (addition of multiple body effects, vector norms, etc)
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.mass = mass

    def move(self):
        # artifact from previous iteration
        self.pos = self.pos + self.vel

    def dists(self, p2: "Particle") -> Dict[str, float]:
        # returns vector difference and norm (euclid dist)
        return dict(pos_diff=p2.pos - self.pos, dist=np.linalg.norm(p2.pos - self.pos))

    def __copy__(self):
        return Particle(self.pos, self.vel, self.mass)

    def __eq__(self, other):
        if isinstance(other, Particle):
            return bool(
                (not False in self.pos == other.pos) * (not False in self.vel == other.pos) * (self.mass == other.mass))
        return False

    def print(self):
        print("Location: {}, Velocity: {}, Mass: {}".format(self.pos, self.vel, self.mass))

    def get_accel(self, other, G):
        # returns gravitational acceleration. Note that since distance vector in dists method is in the form other-self, no negative is applied
        # denominator is to the third power since the distance vector multiplies the numerator
        dists = self.dists(other)
        return G * other.mass * dists["pos_diff"] / dists["dist"] ** 3


class Particles():
    def __init__(self, particles: List[Particle] = [], G=1):
        self.particles = particles
        self.G = G
        self.num_bodies = len(particles)

    def __copy__(self):
        ret = []
        return Particles([particle.__copy__ for particle in self.particles], self.G)

    def displace(self, h: float = 0.001):
        G = self.G
        # temporary lists to hold positions and velocities of each body at each step
        # these must be updated after step occurs for all bodies, not before (beneath loop)
        positions = []
        velocities = []

        for i in range(self.num_bodies):
            # index for all bodies except the one currently considered is kept. Probably not necessary since distance is 0 but avoids another method call and implementing a failsafe for zero division
            # perhaps better way to implement rk4 for n>2 n-body system but as factors are dependent on their previous, and each factor must iterate across all bodies,  I was unable to find one
            # see wikipedia and other sources for details of rk4 algorithm first-order ODE setup of orbital systems
            other_bodies = [x for x in range(self.num_bodies) if x != i]

            curr_pos = self.particles[i].pos

            k1v = np.zeros(curr_pos.shape)
            for j in other_bodies:
                k1v += self.particles[i].get_accel(self.particles[j], self.G)

            k1r = self.particles[i].vel
            k2v = np.zeros(curr_pos.shape)
            for j in other_bodies:
                k2v += Particle(pos=(curr_pos + k1r * h / 2)).get_accel(self.particles[j], G)

            k2r = k1r + k1v * h / 2

            k3v = np.zeros(curr_pos.shape)
            for j in other_bodies:
                k3v += Particle(pos=(curr_pos + k2r * h / 2)).get_accel(self.particles[j], G)

            k3r = k1r + k2v * h / 2

            k4v = np.zeros(curr_pos.shape)
            for j in other_bodies:
                k4v += Particle(pos=(curr_pos + k3r * h)).get_accel(self.particles[j], G)

            k4r = k1r + k3v * h

            #at end of current iteration, store the outputs of next step for current body in list, but do not update until step for all bodies is complete
            velocities.append(k1r + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v))
            positions.append(curr_pos + h / 6 * (k1r + 2 * k2r + 2 * k3r + k4r))

        for i in range(self.num_bodies):
            #update body values for current step
            self.particles[i].pos = positions[i]
            self.particles[i].vel = velocities[i]

    def print(self):
        print("System gravitational constant: {}\n".format(self.g_const))
        for i in range(len(self.particles)):
            self.particles[i].print()
            if i == (len(self.particles) - 1):
                print("\n")
