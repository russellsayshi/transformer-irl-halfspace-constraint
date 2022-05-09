import numpy as np
import math

def comparison(first, second):
    print("(%6.3f, %6.3f, %6.3f), (%6.3f, %6.3f, %6.3f), diff = %.5f" % (first[0], first[1], first[2], second[0], second[1], second[2], math.sqrt(sum((first-second) ** 2))))


comparison(np.array([-0.57735027, -0.57735027, -0.57735027]), np.array([-0.54568012, -0.62385571, -0.55949732]))
comparison(np.array([-0.70710678, -0.70710678, 0.]), np.array([-0.75224069, -0.65689909, -0.05116176]))
comparison(np.array([ 0., -1., 0.]), np.array([ 0.00163879, -0.99999732, 0.00163735]))
comparison(np.array([0., 0., 0.]), np.array([0., 0., 0.]))
comparison(np.array([ 0.57735027, -0.57735027, -0.57735027]), np.array([ 0.59687721, -0.58439448, -0.54974603]))
comparison(np.array([ 0.70710678, -0.70710678, 0.]), np.array([ 0.74601426, -0.6646704, -0.04093888]))
comparison(np.array([1., 0., 0.]), np.array([ 0.99798093, -0.06259407, -0.0107721]))
comparison(np.array([ 0.57735027, 0.57735027, -0.57735027]), np.array([ 0.57366019, 0.58094844, -0.57741917]))
comparison(np.array([0., 0.70710678, 0.70710678]), np.array([-0.04070287, 0.7339494, 0.67798345]))
comparison(np.array([0.57735027, 0.57735027, 0.57735027]), np.array([0.57518374, 0.56965486, 0.58707496]))

