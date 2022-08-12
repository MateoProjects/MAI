from PyRT_Core import *
from PyRT_Integrators import *
import time


def sphere_test_scene(areaLS=False, use_env_map=False):
    # Create a scene object
    scene_ = Scene()
    i_a = RGBColor(0.5, 0.5, 0.5)
    scene_.set_ambient(i_a)

    # Create the materials (BRDF)
    white_diffuse = Lambertian(RGBColor(0.8, 0.8, 0.8))
    green_diffuse = Lambertian(RGBColor(0.2, 0.8, 0.2))

    # Create the Scene Geometry (3D objects)
    # sphere
    radius = 2
    sphere = Sphere(Vector3D(0.0, 0.0, -5.0), radius)
    sphere.set_BRDF(white_diffuse)
    scene_.add_object(sphere)

    # Finite plane
    side = 4 * radius
    half_side = side / 2
    plane_point = Vector3D(-half_side, -radius, -5.0 + half_side)
    right_vector = Vector3D(side, 0.0, 0.0)
    front_vector = Vector3D(0.0, 0.0, -side)
    plane = Parallelogram(plane_point, right_vector, front_vector)
    plane.set_BRDF(green_diffuse)
    scene_.add_object(plane)

    if not areaLS:  # For Monte Carlo-based integrators
        # Create a Point Light Source
        point_light = PointLight(Vector3D(0.0, 5.0, 0.0), RGBColor(80, 80, 80))
        scene_.add_point_light_sources(point_light)
    else:  # For Phong Integrator
        # Create an Area Light Source
        black_material = Lambertian(BLACK)
        light_source_point = Vector3D(-half_side, 3 * radius, -5.0 + half_side)
        i_l = 3.5
        area_light_source = Parallelogram(light_source_point,
                                          right_vector,
                                          front_vector,
                                          RGBColor(i_l, i_l, i_l))
        area_light_source.set_BRDF(black_material)
        scene_.add_object(area_light_source)

    if use_env_map:
        # Set up an environment map
        # env_map_path = 'env_maps/black_and_white.hdr'
        # env_map_path = 'env_maps/outdoor_umbrellas_4k.hdr'
        # env_map_path = 'env_maps/outdoor_umbrellas_4k_clamped.hdr'
        env_map_path = 'env_maps/arch_nozero.hdr'
        scene_.set_environment_map(env_map_path)

    # Create the camera
    width = 500
    height = 500
    vertical_fov = 60
    camera = Camera(width, height, vertical_fov)
    scene_.set_camera(camera)

    return scene_


def cornell_box_scene(dist, side, areaLS=False):
    # Create a scene object
    scene_ = Scene()
    i_a = RGBColor(1.0, 1.0, 0.3)
    scene_.set_ambient(i_a)

    # some useful values to create the box
    z_far = -(dist + side)
    x_left = -side / 2
    x_right = side / 2
    y_bottom = -side / 2
    y_top = side / 2
    plane_point_ll = Vector3D(x_left, y_bottom, z_far)  # lower left corner
    plane_point_ur = Vector3D(x_right, y_top, z_far)  # upper right corner

    # Create the materials (BRDF)
    floor_material = Lambertian(RGBColor(0.8, 0.8, 0.8))
    red_material = Lambertian(RGBColor(0.7, 0.2, 0.2))
    green_material = Lambertian(RGBColor(0.2, 0.7, 0.2))
    blue_material = Lambertian(RGBColor(0.2, 0.2, 0.7))
    black_material = Lambertian(BLACK)

    # Create the Scene Geometry (3D objects)
    # sphere
    sphere = Sphere(Vector3D(0.0, 0.0, -(dist + side / 2.0)), 0.25)
    sphere.set_BRDF(blue_material)
    scene_.add_object(sphere)
    # back wall
    right_vector = Vector3D(side, 0.0, 0.0)
    up_vector = Vector3D(0.0, side, 0.0)
    plane = Parallelogram(plane_point_ll, right_vector, up_vector)
    plane.set_BRDF(floor_material)
    scene_.add_object(plane)
    # floor
    back_vector = Vector3D(0.0, 0.0, side)
    plane = Parallelogram(plane_point_ll, right_vector, back_vector)
    plane.set_BRDF(floor_material)
    scene_.add_object(plane)
    # left wall
    plane = Parallelogram(plane_point_ll, up_vector, back_vector)
    plane.set_BRDF(red_material)
    scene_.add_object(plane)
    # ceiling
    left_vector = Vector3D(-side, 0.0, 0.0)
    plane = Parallelogram(plane_point_ur, left_vector, back_vector)
    plane.set_BRDF(floor_material)
    scene_.add_object(plane)
    # right wall
    bottom_vector = Vector3D(0.0, -side, 0.0)
    plane = Parallelogram(plane_point_ur, bottom_vector, back_vector)
    plane.set_BRDF(green_material)
    scene_.add_object(plane)

    if areaLS:
        # For Monte Carlo-based integrators
        # Create are light source
        side_ls = side / 2
        delta_ls = (side - side_ls) / 2
        light_source_point = Vector3D(x_left + delta_ls,
                                      y_top - 0.0001,
                                      -(dist + delta_ls))
        i_l = 1
        plane = Parallelogram(light_source_point,
                              Vector3D(side_ls, 0, 0),
                              Vector3D(0, 0, -side_ls),
                              RGBColor(i_l, i_l, i_l))
        plane.set_BRDF(black_material)
        scene_.add_object(plane)
    else:
        # For Phong Integrator: Create three Point Light Sources
        i_l = 0.5
        delta_y = 0.5
        point_light_1 = PointLight(Vector3D(0.0, side / 2 - delta_y, -(dist + side / 2.0)),
                                   RGBColor(i_l, i_l, i_l))
        scene_.add_point_light_sources(point_light_1)
        point_light_2 = PointLight(Vector3D(-side / 4, side / 2 - delta_y, -(dist + side / 2.0)),
                                   RGBColor(i_l, i_l, i_l))
        scene_.add_point_light_sources(point_light_2)
        point_light_3 = PointLight(Vector3D(side / 4, side / 2 - delta_y, -(dist + side / 2.0)),
                                   RGBColor(i_l, i_l, i_l))
        scene_.add_point_light_sources(point_light_3)

    # Set up an environment map
    env_map_path = 'env_maps/arch_nozero.hdr'
    scene_.set_environment_map(env_map_path)

    # Create the camera (always centred at 0,0,0)
    width = 500
    height = 500
    vertical_fov = 70
    camera = Camera(width, height, vertical_fov)
    scene_.set_camera(camera)

    return scene_


# --------------------------------------------------Set up variables
FILENAME = 'rendered_image'
DIRECTORY = '.\\out\\'

# -------------------------------------------------Main
# Create Integrator
#integrator = PhongIntegrator(DIRECTORY + FILENAME)
integrator = CMCIntegrator(40, DIRECTORY + FILENAME)

scene = sphere_test_scene(areaLS=False, use_env_map=True)
#scene = cornell_box_scene(0.75, 2, areaLS=False)

# Attach the scene to the integrator
integrator.add_scene(scene)

# Render!
start_time = time.time()
integrator.render()
end_time = time.time() - start_time
print("--- Rendering time: %s seconds ---" % end_time)

# -------------------------------------------------open saved npy image
image_nd_array = np.load(integrator.get_filename() + '.npy')
tonemapper = cv2.createTonemap(gamma=2.5)
image_nd_array_ldr = tonemapper.process(image_nd_array.astype(np.single)) * 255.0
cv2.imshow('Ray Tracer MLCG 2021-2022', cv2.cvtColor(image_nd_array_ldr.astype(np.uint8), cv2.COLOR_BGR2RGB))
cv2.waitKey(0)
