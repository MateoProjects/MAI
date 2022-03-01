from math import sqrt, acos, cos, sin, atan2, floor, pi
import cv2
from random import random
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod  # Abstract Base Class

# Used coordinate system: right-handed
# Constants
EPSILON = 0.0001  # very small value
HUGEVALUE = 1000000.0  # 1 million
PI = 3.1415926535897932384
TWO_PI = 6.2831853071795864769
INVERTED_PI = 0.3183098861837906912

# -------------------------------------------------Vector3D class
class Vector3D:
    # Initializer
    def __init__(self, x_element, y_element, z_element):
        self.x = x_element
        self.y = y_element
        self.z = z_element

    # Operator Overloading
    def __sub__(self, v):
        return Vector3D(self.x - v.x, self.y - v.y, self.z - v.z)

    def __add__(self, v):
        return Vector3D(self.x + v.x, self.y + v.y, self.z + v.z)

    def __mul__(self, s):
        return Vector3D(self.x * s, self.y * s, self.z * s)

    def __truediv__(self, s):
        return Vector3D(self.x / s, self.y / s, self.z / s)

    def __repr__(self):
        return f'Vector3D({self.x}, {self.y}, {self.z})'



# -------------------------------------------------Ray class
class Ray:
    # Initializer
    def __init__(self, origin=Vector3D(0,0,0),
                 direction=Vector3D(0,0,0), tmax=HUGEVALUE):
        self.o = origin
        self.d = direction
        self.t_max = tmax
        self.t_min = EPSILON

    # Member Functions
    def get_hitpoint(self, t):
        return self.o + self.d * t


# -------------------------------------------------Structure to hold hit information
class HitData:
    def __init__(self, has_hit=False, hit_point=Vector3D(0,0,0), normal=Vector3D(0,0,0),
                 hit_distance=HUGEVALUE, primitive_index=-1):
        self.has_hit = has_hit  # whether or not this object represents a hit
        self.hit_point = hit_point  # hit point
        self.normal = normal  # normal at the surface
        self.hit_distance = hit_distance  # intersection distance along the ray
        self.primitive_index = primitive_index  # index of the object (primitive) hit by the ray


# Return dot product between two vectors
def Dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z


# Return perpendicular vector
def Cross(a, b):
    return Vector3D(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)


# Return length of vector
def Length(v):
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z)


# Return normalized vector (unit vector)
def Normalize(v):
    return v * (1.0 / Length(v))


# Return normal that is pointing on the side as the passed direction
def orient_normal(normal, direction):
    if Dot(normal, direction) < 0.0:
        return normal * -1.0  # flip normal
    else:
        return normal


# -------------------------------------------------RGBColour class
class RGBColor:
    # Initializer
    def __init__(self, red, green, blue):
        self.r = red
        self.g = green
        self.b = blue

    # Operator Overloading
    def __add__(self, c):
        return RGBColor(self.r + c.r, self.g + c.g, self.b + c.b)

    def __sub__(self, c):
        return RGBColor(self.r - c.r, self.g - c.g, self.b - c.b)

    def __mul__(self, s):
        return RGBColor(self.r * s, self.g * s, self.b * s)

    def __truediv__(self, s):
        return RGBColor(self.r / s, self.g / s, self.b / s)

    # this alows us to multipy by another RGBColour
    def multiply(self, c):
        return RGBColor(self.r * c.r, self.g * c.g, self.b * c.b)

    # Member Functions
    def cp(self, minimum, maximum):
        # red
        if (self.r > maximum): self.r = maximum
        if (self.r < minimum): self.r = minimum
        # green
        if (self.g > maximum): self.g = maximum
        if (self.g < minimum): self.g = minimum
        # blue
        if (self.b > maximum): self.b = maximum
        if (self.b < minimum): self.b = minimum

    def __repr__(self):
        return f'RGBColor({self.r}, {self.g}, {self.b})'


# Constants
BLACK = RGBColor(0.0, 0.0, 0.0)
WHITE = RGBColor(1.0, 1.0, 1.0)
GREEN = RGBColor(0.0, 1.0, 0.0)
RED = RGBColor(1.0, 0.0, 0.0)  # for testing


# ------------------------------------------------- Free Functions
# Return normal that is pointing on the side as the passed direction
def orient_normal(normal, direction):
    if Dot(normal, direction) < 0.0:
        return normal * -1.0  # flip normal
    else:
        return normal


# Convert a point set defined on the unit sphere from euclidean coordinates (3D) to 2D polar coordinates (disk)
# Returns two np arrays
def euclidean_to_disk(sample_set):
    ns = len(sample_set)
    r = np.zeros(ns)
    phi = np.zeros(ns)
    normal = Vector3D(0, 1, 0)
    for i in range(ns):
        current_dir = sample_set[i]
        r_i = acos(Dot(normal, current_dir))
        phi_i = atan2(current_dir.x, current_dir.z)
        r[i] = r_i
        phi[i] = phi_i
    return r, phi


def sample_set_hemisphere(n_samples, pdf):
    sample_set = []
    sample_prob = []
    for i in range(n_samples):
        u1 = random()
        u2 = random()
        omega_i = pdf.generate_dir(u1, u2)
        sample_set.append(omega_i)
        sample_prob.append(pdf.get_val(omega_i))
        # plt.plot(omega_i.x, omega_i.z, 'o')
    # plt.show()
    return sample_set, sample_prob


# Visualize the samples on a disk
def visualize_sample_set(sample_set, weights=[]):
    r, phi = euclidean_to_disk(sample_set)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    if len(weights) == 0:
        ax.scatter(phi, r)
    else:
        av_weight_val = 1.0 / len(weights)
        delta = 0.3 * av_weight_val
        cm = plt.get_cmap('jet')
        sc = plt.scatter(phi, r, vmin=av_weight_val - delta, vmax=av_weight_val + delta, c=weights, cmap=cm)
        fig.colorbar(sc)
        ax = plt.gca()
    ax.axis([0, 2 * pi, 0, pi / 2])
    plt.show()


def oriented_hemi_dir(pdf, u1, u2, new_normal):
    dir_ = pdf.generate_dir(u1, u2)  # random point on hemisphere
    return center_around_normal(dir_, new_normal)  # normalized


def rotate_around_y(alpha, dir_):
    sin_alpha = sin(alpha)
    cos_alpha = cos(alpha)
    new_x = dir_.x * cos_alpha + dir_.z * sin_alpha
    new_z = -dir_.x * sin_alpha + dir_.z * cos_alpha
    return Vector3D(new_x, dir_.y, new_z)


def center_around_normal(dir, normal):
    # create orthonormal basis around normal
    w = normal
    v = Cross(Vector3D(0.00319, 1.0, 0.0078), w)  # jittered up
    v = Normalize(v)  # normalize
    u = Cross(v, w)

    hemi_dir = (v * dir.x) + (w * dir.y) + (u * dir.z)  # project the original direction dir onto the new frame
    return Normalize(hemi_dir)


# -------------------------------------------------Environment Map Source Class
class EnvironmentMap:
    # Initializer
    def __init__(self, env_map_path):
        # IMREAD_ANYDEPTH is needed because even though the data is stored in 8-bit channels
        # when it's read into memory it's represented at a higher bit depth
        self.env_map_hdr = cv2.imread(env_map_path, flags=cv2.IMREAD_ANYDEPTH)
        self.env_map_hdr = cv2.cvtColor(self.env_map_hdr, cv2.COLOR_RGB2BGR)
        self.height = self.env_map_hdr.shape[0]
        self.width = self.env_map_hdr.shape[1]

    def euclideanToLatLong(self, d):
        uLatLong = (1 + (1 / PI) * atan2(d.x, -d.z)) / 2.0
        vLatLong = (1 / PI) * acos(d.y)
        return (uLatLong, vLatLong)

    def getValue(self, d):
        (u, v) = self.euclideanToLatLong(d)
        tx = floor(u * (self.width - 1))  # texel x coordinate
        ty = floor(v * (self.height - 1))  # texel y coordinate
        res = self.env_map_hdr[ty, tx, :]
        return RGBColor(res[0], res[1], res[2])


# -------------------------------------------------Functions over the hemisphere
class Function(ABC):
    def __init__(self, integral_value):
        self.ground_truth = integral_value

    @abstractmethod
    def eval(self, omega_i):
        pass

    @abstractmethod
    def get_integral(self):
        pass


class Constant(Function):
    def __init__(self, const_value_):
        self.const_value = const_value_
        integral = self.get_integral()
        super().__init__(integral)

    def eval(self, omega_i):
        return self.const_value

    def get_integral(self):
        return 2 * pi * self.const_value


class CosineLobe(Function):
    def __init__(self, exp_):
        self.exp = exp_
        integral = self.get_integral()
        super().__init__(integral)

    def eval(self, omega_i):
        normal = Vector3D(0, 1, 0)
        return Dot(normal, omega_i) ** self.exp

    def get_integral(self):
        return 2 * pi / (self.exp + 1)


# -------------------------------------------------Base class for pdfs oer the hemisphere 2*pi
class PDF(ABC):

    @abstractmethod
    def get_val(self, omega_i):
        pass

    @abstractmethod
    def generate_dir(self, u1, u2):
        pass


# Uniform PDF over the hemisphere: p(omega) = 1/(2*pi)
class UniformPDF(PDF):

    def get_val(self, omega_i):
        return 1 / (2 * pi)

    def generate_dir(self, u1, u2):
        # compute the y coordinate (up)
        y = u2
        # compute the x and z coordinates
        phi = TWO_PI * u1  # azimuth angle (aka rotation angle)
        aux_sqrt = sqrt(1 - u2 ** 2)
        x = sin(phi) * aux_sqrt
        z = cos(phi) * aux_sqrt
        return Vector3D(x, y, z)


# PDF: p(omega) = (n+1)/(2*pi) * cos(theta)**n
class CosinePDF(PDF):
    def __init__(self, exp_):
        self.exp = exp_

    def get_val(self, omega_i):
        normal = Vector3D(0.0, 1.0, 0.0)
        cos_theta = Dot(normal, omega_i)
        return (self.exp + 1) / (2 * pi) * cos_theta ** self.exp

    def generate_dir(self, u1, u2):
        # compute the y coordinate (up)
        y = pow(u2, 1.0 / (self.exp + 1.0))
        # compute the x and z coordinates
        phi = TWO_PI * u1  # azimuth angle (aka rotation angle)
        aux_power = 2.0 / (self.exp + 1.0)
        aux_sqrt = sqrt(1 - u2 ** aux_power)
        x = sin(phi) * aux_sqrt
        z = cos(phi) * aux_sqrt
        return Vector3D(x, y, z)
