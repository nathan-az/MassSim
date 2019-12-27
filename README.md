# MassSim

## Introduction
This project was started when a friend introduced me to the Chinese novel, The Three-Body Problem. Google yielded the wikipedia page for the Three Body Problem in classical mechanics. In this repository, my latest attempt to simulate n-bodies in N dimensions.

## Notes
I am fully aware that Python has modules that will far more effectively approximate ODEs (i.e. scipy.integrate.odeint). Implementing rk4 was a learning experience and a first stab at numerical analysis (broad familiarity with Euler method aside).

Secondarily, a class system was introduced for the sake of practicing Python OOP having learned with Java. I have not tested but it is likely that storing a single numpy array of initial parameters would improve the rk4 implementation (but if I was concerned with runtime, I wouldn't have implemented myself!)

## Methodology
My initial method calculated gravitational acceleration at each time step, incremented velocities by the given amount, and incremented position in each direction by the velocity vector. This proved a poor approximation, stepping by a full time unit each iteration. I considered using scipy.integrate.odeint but found it to be inflexible. Despite no further use for this project, I wanted an implementation that would be entirely flexible in the number of bodies (n) and the dimension. This may still have been posible with the scipy module but I hastile scratched together a python implementation that iterated across each body and its neighbours (flexible in n) and performed operations at a vector level for position and velocity (flexible in dim).

### Sources
[Initial reference on RK4](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods)
[Initial reference on Three-body problem](https://en.wikipedia.org/wiki/Three-body_problem)
[Research on first-order setup of gravitational systems](http://spiff.rit.edu/richmond/nbody/OrbitRungeKutta4.pdf) Note that this document has an error on the k-coefficients of the position ODE, must be addition e.g. k2r = k1r + k1v * (h/2), not k2r = k1r * k1v * (h/2)
[Matplotlib documentation and examples for animation, particlarly double-pendulum example](https://matplotlib.org/3.1.1/gallery/animation/double_pendulum_sgskip.html)
