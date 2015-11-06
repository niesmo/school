import numpy as np
import matplotlib.pyplot as plt

def gaussian_2d(x, y, x0, y0, xsig, ysig):
    return np.exp(-0.5*(((x-x0) / xsig)**2 + ((y-y0) / ysig)**2))

delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = gaussian_2d(X, Y, 0., 0., 1., 1.)
Z2 = gaussian_2d(X, Y, 1., 1., 1.5, 0.5)
# difference of Gaussians
Z = 10.0 * (Z2 - Z1)

# Create a contour plot with labels using default colors.  The
# inline argument to clabel will control whether the labels are draw
# over the line segments of the contour, removing the lines beneath
# the label
plt.clf()
CS = plt.contour(X, Y, Z)
plt.clabel(CS, inline=1, fontsize=10)
plt.title('Simplest default with labels')
plt.show()