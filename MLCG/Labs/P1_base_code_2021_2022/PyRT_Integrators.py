from PyRT_Common import *
from random import randint
from PyRT_Core import *

# -------------------------------------------------Integrator Classes
# the integrators also act like a scene class in that-
# it stores all the primitives that are to be ray traced.
class Integrator(ABC):
    # Initializer - creates object list
    def __init__(self, filename_, experiment_name=''):
        # self.primitives = []
        self.filename = filename_ + experiment_name
        # self.env_map = None  # not initialized
        self.scene = None

    @abstractmethod
    def compute_color(self, ray):
        pass

    # def add_environment_map(self, env_map_path):
    #    self.env_map = EnvironmentMap(env_map_path)
    def add_scene(self, scene):
        self.scene = scene

    def get_filename(self):
        return self.filename

    # Simple render loop: launches 1 ray per pixel
    def render(self):
        # YOU MUST CHANGE THIS METHOD IN ASSIGNMENTS 1.1 and 1.2:
        cam = self.scene.camera  # camera object
        
        print('Rendering Image: ' + self.get_filename())
        for x in range(0, cam.width):
            for y in range(0, cam.height):
                pixel = self.compute_color(Ray(direction=cam.get_direction(x,y)))
                self.scene.set_pixel(pixel, x, y)  # save pixel to pixel array
            progress = (x / cam.width) * 100
            print('\r\tProgress: ' + str(progress) + '%', end='')
        # save image to file
        print('\r\tProgress: 100% \n\t', end='')
        full_filename = self.get_filename()
        self.scene.save_image(full_filename)


class LazyIntegrator(Integrator):
    def __init__(self, filename_):
        super().__init__(filename_ + '_Intersection')

    def compute_color(self, ray):
        return BLACK


class IntersectionIntegrator(Integrator):

    def __init__(self, filename_):
        super().__init__(filename_ + '_Intersection')

    def compute_color(self, ray):
        # ASSIGNMENT 1.2: PUT YOUR CODE HERE
        if self.scene.any_hit(ray):
            return RED
        else: return BLACK


class DepthIntegrator(Integrator):

    def __init__(self, filename_, max_depth_=10):
        super().__init__(filename_ + '_Depth')
        self.max_depth = max_depth_

    def compute_color(self, ray):
        # ASSIGNMENT 1.3: PUT YOUR CODE HERE
        hitData = self.scene.closest_hit(ray)
        if hitData.has_hit:
            x = min(1-(hitData.hit_distance/self.max_depth), 1)
            return RGBColor(x, x, x)
        else: return BLACK


class NormalIntegrator(Integrator):

    def __init__(self, filename_):
        super().__init__(filename_ + '_Normal')

    def compute_color(self, ray):
        # ASSIGNMENT 1.3: PUT YOUR CODE HERE
        hitData = self.scene.closest_hit(ray)
        if hitData.has_hit:
            result = (hitData.normal + Vector3D(1, 1, 1))/ 2
            return RGBColor(result.x, result.y, result.z)
        else: return BLACK


class PhongIntegrator(Integrator):

    def __init__(self, filename_):
        super().__init__(filename_ + '_Phong')

    def compute_color(self, ray):
        hitData = self.scene.closest_hit(ray)
        if hitData.has_hit:
            # if not occluded
            point_light = self.scene.pointLights[0].pos # tupla de 3 valors x , y , z
            # intersection of two points
            direction = point_light - hitData.hit_point
            direction_arr = np.array([direction.x, direction.y, direction.z],dtype=np.float64)
            distanceLight = np.linalg.norm(direction_arr)
            direction = direction / distanceLight
            rayLight = Ray(hitData.hit_point, direction, distanceLight)
            hitDataShadow = self.scene.any_hit(rayLight)
            primitiva = self.scene.object_list[hitData.primitive_index]

            if not hitDataShadow:
                #direction = ray.d.__mul__(-1)
                value = primitiva.BRDF.get_value(normal=hitData.normal,wo=1, wi=direction)
                intensity = self.scene.pointLights[0].intensity

                value = value.multiply(intensity/(distanceLight**2))
                return value + primitiva.BRDF.kd.multiply(self.scene.i_a)

            else:  
                return primitiva.BRDF.kd.multiply(self.scene.i_a)
    
        else: return BLACK
        


class CMCIntegrator(Integrator):  # Classic Monte Carlo Integrator

    def __init__(self, n, filename_, experiment_name=''):
        filename_mc = filename_ + '_MC_' + str(n) + '_samples' + experiment_name
        super().__init__(filename_mc)
        self.n_samples = n

    def compute_color(self, ray):
        # 1/N + sum(1-N)(fx_i / px_i)
        pass


class BayesianMonteCarloIntegrator(Integrator):
    def __init__(self, n, myGP, filename_, experiment_name=''):
        filename_bmc = filename_ + '_BMC_' + str(n) + '_samples' + experiment_name
        super().__init__(filename_bmc)
        self.n_samples = n
        self.myGP = myGP

    def compute_color(self, ray):
        pass
