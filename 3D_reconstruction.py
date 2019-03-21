import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D
import image_preprocessing
import init_parameters


camera_parameters = init_parameters.init_parameter()

# for time saving
preprocess = False
if preprocess:
    image_preprocessing.image_preprocessing()


def point_projection(world_points, camera_id):
    pro_point, jacobin = cv2.projectPoints(
        objectPoints=world_points,
        rvec=camera_parameters['RotationVectors'][camera_id],
        tvec=camera_parameters['TranslationVectors'][camera_id],
        cameraMatrix=camera_parameters['IntrinsicMatrix'],
        distCoeffs=camera_parameters['DistCoeffs'])
    return pro_point + camera_parameters['PrincipalPoint']


def check_projection():
    points = init_parameters.get_points()
    num_points = points['WorldPoints'].shape[0]
    world_points = np.zeros((num_points, 3))
    for i in range(num_points):
        world_points[i, 0:2] = points['WorldPoints'][i]

    for i in range(camera_parameters['NumPatterns']):
        reprojected_points = points['ReprojectedPoints'][:, :, i]
        pro_point, jacobin = cv2.projectPoints(
            objectPoints=world_points,
            rvec=camera_parameters['RotationVectors'][i],
            tvec=camera_parameters['TranslationVectors'][i],
            cameraMatrix=camera_parameters['IntrinsicMatrix'],
            distCoeffs=camera_parameters['DistCoeffs'])
        pro_point = pro_point.reshape(num_points, 2) + camera_parameters['PrincipalPoint']
        print("picture {} max error".format(i), np.abs(pro_point - reprojected_points).max())


def save_point_cloud(points, file_name):
    print(points.shape[0])
    file = open(file_name, "w")
    file.write(str(points.shape[0]) + "\n")

    for i in range(points.shape[0]):
        file.write(str(points[i, 0]) + " ")
        file.write(str(points[i, 1]) + " ")
        file.write(str(points[i, 2]) + "\n")


def reconstruction(x_limit, y_limit, z_limit, delta, recalculate=True, show_result=False):
    """ x_limit: (x_min, x_max)
        y_limit: (y_min, y_max)
        z_limit: (z_min, z_max)
        delta: step size
    """
    x_net_size = round((x_limit[1] - x_limit[0])/delta)
    x_net = np.linspace(x_limit[0], x_limit[1], x_net_size).astype(np.float)

    y_net_size = round((y_limit[1] - y_limit[0])/delta)
    y_net = np.linspace(y_limit[0], y_limit[1], y_net_size).astype(np.float)

    z_net_size = round((z_limit[1] - z_limit[0])/delta)
    z_net = np.linspace(z_limit[0], z_limit[1], z_net_size).astype(np.float)

    word_points = np.zeros((x_net_size*y_net_size*z_net_size, 3))

    # generate 3D point cloud
    n = 0
    for i in range(x_net_size):
        for j in range(y_net_size):
            for k in range(z_net_size):
                word_points[n] = np.array([x_net[i], y_net[j], z_net[k]])
                n += 1

    point_size = word_points.shape[0]

    voter_file = "voter.npy"
    if recalculate:
        voter = np.zeros((point_size, camera_parameters['NumPatterns'])).astype(np.int)

        # cv2.namedWindow("fuck", cv2.WINDOW_NORMAL)

        for camera_id in range(camera_parameters['NumPatterns']):
            print("dealing with picture {}".format(camera_id))

            picture_points = point_projection(word_points, camera_id).round().squeeze().astype(np.int)
            # read image
            folder_name = "camera-calibration"
            image = cv2.imread(folder_name + "/{}_result_undistorted.jpg".format(camera_id))

            for id in range(point_size):
                x, y = picture_points[id][0], picture_points[id][1]
                # print(x, y)
                if x < 0 or x >= camera_parameters['ImageSize'][1] or y < 0 or y >= camera_parameters['ImageSize'][0]:
                    continue
                if image[y, x].all() != 0:
                    voter[id, camera_id] = 1

        print(voter.sum(axis=1).max())
        voter = voter.sum(axis=1) > 20
        np.save(voter_file, voter)
    else:
        voter = np.load(voter_file)
    print(voter.shape)
    x, y, z = word_points[voter, 0], word_points[voter, 1], word_points[voter, 2]
    bias = np.array([(x_limit[0] + x_limit[1])/2.0, (y_limit[0] + y_limit[1])/2.0, (z_limit[0] + z_limit[1])/2.0])
    save_point_cloud(word_points[voter] - bias, "point_cloud.dat")

    print("total have {} points".format(x.shape[0]))
    # print(x.max(), x.min(), y.max(), y.min(), z.max(), z.min())
    if show_result:
        ax = plt.subplot(111, projection='3d')
        ax.scatter(x, y, z)

        ax.set_zlabel('Z')
        ax.set_ylabel('Y')
        ax.set_xlabel('X')
        plt.show()


if __name__ == "__main__":
    # check_projection()
    reconstruction(x_limit=(-10, 100),
                   y_limit=(190, 270),
                   z_limit=(-110, 0),
                   delta=0.5,
                   recalculate=False,
                   show_result=False)
    # points = np.random.randint(0, 20, (5, 3)).astype(np.float32)
    # print(points)
    # os.

