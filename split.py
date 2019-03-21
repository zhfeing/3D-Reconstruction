import cv2
import numpy as np
import init_parameters


parameters = init_parameters.init_parameter()

H_min = 30
H_max = 101
S_min = 45
S_max = 255
V_min = 45
V_max = 255


def update_graph(args):
    H_min = cv2.getTrackbarPos("H_min", toolbar_window_name)
    H_max = cv2.getTrackbarPos("H_max", toolbar_window_name)
    S_max = cv2.getTrackbarPos("S_max", toolbar_window_name)
    S_min = cv2.getTrackbarPos("S_min", toolbar_window_name)
    V_max = cv2.getTrackbarPos("V_max", toolbar_window_name)
    V_min = cv2.getTrackbarPos("V_min", toolbar_window_name)

    hsv = cv2.cvtColor(callback_image, cv2.COLOR_BGR2HSV)

    lower = np.array([H_min, S_min, V_min])
    upper = np.array([H_max, S_max, V_max])
    mask = cv2.inRange(hsv, lower, upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    res = cv2.bitwise_and(image, image, mask=mask)

    cv2.imshow(result_window_name, res)
    cv2.imshow(toolbar_window_name, mask)
    cv2.imwrite(result_file_name, mask)


def split():
    folder_name = "camera-calibration"
    for i in range(parameters['NumPatterns']):
        print("processing image No.{} ...".format(i))
        image = cv2.imread(folder_name + "/{}.jpg".format(i))
        result_file_name = folder_name + "/{}_result.jpg".format(i)

        if image is None:
            print("no such a picture")
        else:
            image = cv2.blur(image, (11, 11))
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            lower = np.array([H_min, S_min, V_min])
            upper = np.array([H_max, S_max, V_max])
            mask = cv2.inRange(hsv, lower, upper)

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            cv2.imwrite(result_file_name, mask)


if __name__ == "__main__":
    folder_name = "camera-calibration"
    result_window_name = "cup"
    toolbar_window_name = "toolbar"

    for i in range(parameters['NumPatterns']):

        image = cv2.imread(folder_name + "/{}.jpg".format(i))
        result_file_name = folder_name + "/{}_result.jpg".format(i)

        if image is None:
            print("no such a picture")
        else:
            input_image_name = "image"

            cv2.namedWindow(input_image_name, cv2.WINDOW_NORMAL)
            cv2.namedWindow(result_window_name, cv2.WINDOW_NORMAL)
            cv2.namedWindow(toolbar_window_name, cv2.WINDOW_NORMAL)

            cv2.imshow(input_image_name, image)
            callback_image = cv2.blur(image, (11, 11))

            cv2.createTrackbar("H_min", toolbar_window_name, H_min, 255, update_graph)
            cv2.createTrackbar("H_max", toolbar_window_name, H_max, 255, update_graph)
            cv2.createTrackbar("S_min", toolbar_window_name, S_min, 255, update_graph)
            cv2.createTrackbar("S_max", toolbar_window_name, S_max, 255, update_graph)
            cv2.createTrackbar("V_min", toolbar_window_name, V_min, 255, update_graph)
            cv2.createTrackbar("V_max", toolbar_window_name, V_max, 255, update_graph)
            update_graph(0)

            cv2.waitKey(1)
