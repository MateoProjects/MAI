# Modules
from PyRT_Common import *
from abc import ABC, abstractmethod  # Abstract Base Class
from math import tan
import numpy as np


# -------------------------------------------------BRDF classes
class Scene:
    def __init__(self):
        self.camera = None
        self.env_map = None  # not initialized
        self.rendered_image = None
        self.object_list = []  # object list
        self.pointLights = []  # list of point light sources (for Phong Illumination)
        self.i_a = None # ambient lighting

    def set_ambient(self, i_a):
        self.i_a = i_a

    # set camera
    def set_camera(self, camera):
        self.camera = camera
        self.rendered_image = np.zeros((camera.height, camera.width, 3))

    # set environment map
    def set_environment_map(self, env_map_path):
        self.env_map = EnvironmentMap(env_map_path)

    # add objects
    def add_object(self, new_object):
        self.object_list.append(new_object)

    # add point light sources
    def add_point_light_sources(self, point_light):
        self.pointLights.append(point_light)

    def any_hit(self, ray):
        # ASSIGNMENT 1.2: PUT YOUR CODE HERE
        for i in range(len(self.object_list)):
            this_hit = self.object_list[i].intersect(ray)
            if this_hit.has_hit:  # Hit
                return True
        return False

    def closest_hit(self, ray):
        # find closest hit object, its distance, hit_point and normal
        # scan through primitives in scene, find closest
        hit_data = HitData()
        for i in range(len(self.object_list)):
            this_hit = self.object_list[i].intersect(ray)
            if this_hit.has_hit:  # Hit
                if this_hit.hit_distance < hit_data.hit_distance:  # Distance
                    hit_data = this_hit
                    hit_data.primitive_index = i
        return hit_data

    # save pixel array to file
    def save_image(self, full_filename):
        tonemapper = cv2.createTonemap(gamma=2.5)
        image_nd_array_ldr = tonemapper.process(self.rendered_image.astype(np.single))
        plt.imsave(full_filename + '.png', np.clip(image_nd_array_ldr, 0, 1))
        np.save(full_filename, self.rendered_image)
        cv2.imwrite(full_filename + '.hdr', cv2.cvtColor(self.rendered_image.astype('float32'), cv2.COLOR_RGB2BGR));
        print("Image Saved")

    # set pixel value
    def set_pixel(self, pixel_val, x, y):
        # pixel_val.clamp(0.0, 1.0)
        self.rendered_image[y, x, 0] = pixel_val.r
        self.rendered_image[y, x, 1] = pixel_val.g
        self.rendered_image[y, x, 2] = pixel_val.b


# -------------------------------------------------Primitive classes
class Primitive(ABC):
    def __init__(self, emission=BLACK):
        self.emission = emission
        self.BRDF = None

    @abstractmethod
    def intersect(self, ray):
        pass

    # Setters
    def set_BRDF(self, BRDF):
        self.BRDF = BRDF

    # Getters
    def get_BRDF(self):
        return self.BRDF


# Sphere
class Sphere(Primitive):
    # Initializer
    def __init__(self, sphere_origin, sphere_radius, emission=BLACK):
        super().__init__(emission)
        self.origin = sphere_origin
        self.radius = sphere_radius
        self.radius_squared = sphere_radius * sphere_radius  # optimization

    # Member Functions
    # Returns tuple of (bool hit, distance, hit_point, normal)
    def intersect(self, ray):
        ray_dir = Normalize(ray.d)
        temp = np.subtract(ray.o, self.origin)
        A = Dot(ray_dir, ray_dir)
        B = 2.0 * Dot(ray_dir, temp)
        C = Dot(temp, temp) - self.radius_squared

        disc = (B * B) - (4.0 * A * C)  # Discriminant

        if disc < 0.0:  # No Hit
            return HitData()  # return an 'empty' HitData object (no intersection)

        sqrt_disc = sqrt(disc)  # square root of discriminant

        t_small = (-B - sqrt_disc) / (2.0 * A)
        if t_small >= ray.t_min and t_small <= ray.t_max:  # Hit
            p = ray.get_hitpoint(t_small)
            n = Normalize((p - self.origin) / self.radius)
            return HitData(has_hit=True, hit_point=p, normal=n, hit_distance=t_small)

        t_large = (-B + sqrt_disc) / (2.0 * A)
        if t_large >= ray.t_min and t_large <= ray.t_max:  # Hit
            p = ray.get_hitpoint(t_large)
            n = Normalize((p - self.origin) / self.radius)
            return HitData(has_hit=True, hit_point=p, normal=n, hit_distance=t_large)

        # Ray did not intersect sphere
        return HitData()


# Plane
class InfinitePlane(Primitive):
    # Initializer
    def __init__(self, plane_origin, plane_normal, emission=BLACK):
        super().__init__(emission)
        self.origin = plane_origin
        self.normal = Normalize(plane_normal)

    # Member Functions
    # Returns tuple of (bool hit, distance, hit_point, normal)
    def intersect(self, ray):
        ray_dir = Normalize(ray.d)
        denominator = Dot(ray_dir, self.normal)
        if denominator == 0.0:  # Check for division by zero
            # ray is parallel, no hit
            return HitData()

        t = Dot(self.normal, (self.origin - ray.o)) / denominator
        if t >= ray.t_min and t <= ray.t_max:  # Hit
            p = ray.get_hitpoint(t)
            return HitData(has_hit=True, hit_point=p, normal=self.normal, hit_distance=t)

        # Ray did not intersect plane
        return HitData()


# Plane
class Parallelogram(Primitive):
    # Initializer
    def __init__(self, point, s1, s2, emission=BLACK):
        super().__init__(emission)
        self.point = point  # point (a corner of the rectangle
        self.s1 = s1  # side 1
        self.s2 = s2  # side 2
        self.s1_n = Normalize(s1)
        self.s2_n = Normalize(s2)
        self.s1_l = Length(s1)
        self.s2_l = Length(s2)
        self.normal = Normalize(Cross(s1, s2))

    # Member Functions
    # Returns tuple of (bool hit, distance, hit_point, normal)
    def intersect(self, ray):
        ray_dir = Normalize(ray.d)
        normal_ = self.normal
        denominator = Dot(ray_dir, normal_)
        if denominator == 0.0:  # Check for division by zero
            # ray is parallel, no hit
            return HitData()

        t = Dot(normal_, (self.point - ray.o)) / denominator
        if t >= ray.t_min and t <= ray.t_max:  # Hit
            p_hit = ray.get_hitpoint(t)
            # Check whether p is within the square limits
            p_ph = p_hit - self.point  # 3D vector from point to p_hit

            # Project p_ph onto s1 and s2
            p_ph_n = Normalize(p_ph)
            p_ph_l = Length(p_ph)
            cos_alpha1 = Dot(self.s1_n, p_ph_n)
            cos_alpha2 = Dot(self.s2_n, p_ph_n)
            q1 = cos_alpha1 * p_ph_l
            q2 = cos_alpha2 * p_ph_l

            if q1 < 0.0 or q2 < 0.0 or q1 > self.s1_l or q2 > self.s2_l:
                return HitData()

            if Dot(self.normal, ray_dir) > 0:
                normal_ = self.normal * (-1)
            return HitData(has_hit=True, hit_point=p_hit, normal=normal_, hit_distance=t)

        # Ray did not intersect plane
        return HitData()


# -------------------------------------------------BRDF classes
class BRDF(ABC):
    @abstractmethod
    def get_value(self, incoming, outgoing, normal):
        pass


# Lambertian (perfect diffuse material)
class Lambertian(BRDF):
    # Initializer
    def __init__(self, diffuse_colour):
        self.kd = diffuse_colour * INVERTED_PI

    # Member Functions
    # wi Direcio de llum
    def get_value(self, wi, wo, normal):
        cos_n_wi = Dot(normal, wi)
        if Dot(normal, wi) > 0.0:
            return self.kd * cos_n_wi  # Colour
        else:
            return BLACK


# -------------------------------------------------Point Light Source Class
class PointLight:
    def __init__(self, pos_, intensity_):
        self.pos = pos_
        self.intensity = intensity_


# -------------------------------------------------Camera Class
class Camera:
    # Initializer
    def __init__(self, width_, height_, vertical_fov_):
        self.width = width_
        self.height = height_
        self.vertical_fov = vertical_fov_ / 180 * PI
        self.aspect_ratio = width_ / height_

    def get_direction(self, x, y):
        # Convert from pixel coordinates to screen space
        x_ss = 2.0 * (x + 0.5) / self.width - 1.0
        y_ss = 1.0 - 2.0 * (y + 0.5) / self.height
        # Convert from screen space to camera space
        tan_half_fov = tan(self.vertical_fov / 2.0)
        x_cs = x_ss * tan_half_fov * self.aspect_ratio
        y_cs = y_ss * tan_half_fov
        p_cs = Vector3D(x_cs, y_cs, -1.0)
        # Compute the ray direction in camera space
        direction = Normalize(p_cs)  # because camera is always at (0,0,0)
        return direction
