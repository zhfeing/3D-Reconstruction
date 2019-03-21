import cv2
import split


re_split = False


def init_undistort_image(parameters):
    camera_matrix = parameters['IntrinsicMatrix'].transpose()
    image_size = (parameters['ImageSize'][1], parameters['ImageSize'][0])
    new_camera_matrix, retval = cv2.getOptimalNewCameraMatrix(
        cameraMatrix=camera_matrix,
        distCoeffs=parameters['DistCoeffs'],
        imageSize=image_size,
        alpha=0
    )

    map1, map2 = cv2.initUndistortRectifyMap(
        cameraMatrix=camera_matrix,
        distCoeffs=parameters['DistCoeffs'],
        R=None,
        newCameraMatrix=new_camera_matrix,
        size=image_size,
        m1type=cv2.CV_16SC2
    )
    return map1, map2


def image_preprocessing(show_result=False):
    if re_split:
        split.split()

    # initial undistort map
    map1, map2 = init_undistort_image(split.parameters)

    for i in range(split.parameters['NumPatterns']):
        print("preprocessing image No.{} ...".format(i))
        # open image file
        folder_name = "camera-calibration"
        image_origin = cv2.imread(folder_name + "/{}.jpg".format(i))
        image = cv2.imread(folder_name + "/{}_result.jpg".format(i))

        # undistorting
        undistorted_image = cv2.remap(image, map1, map2, cv2.INTER_LINEAR)
        undistorted_image_origin = cv2.remap(image_origin, map1, map2, cv2.INTER_LINEAR)

        cv2.imwrite(folder_name + "/{}_undistorted.jpg".format(i), undistorted_image_origin)
        cv2.imwrite(folder_name + "/{}_result_undistorted.jpg".format(i), undistorted_image)

        if show_result:
            cv2.namedWindow("input", cv2.WINDOW_NORMAL)
            cv2.imshow("input", image)

            cv2.namedWindow("origin", cv2.WINDOW_NORMAL)
            cv2.imshow("origin", image_origin)

            cv2.namedWindow("undistorted image", cv2.WINDOW_NORMAL)
            cv2.imshow("undistorted image", undistorted_image)

            cv2.waitKey(0)


if __name__ == "__main__":
    image_preprocessing(True)
