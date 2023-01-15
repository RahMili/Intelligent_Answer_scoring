import os
import cv2
import numpy as np



save_path = "\data\saved_crops"


def read_image(image_file_path):
    """
    Wrapper method to read image file using OpenCV
    :param image_file_path:
    :param config: placeholder for passing any config parameters
    :return:
    """

    if os.path.exists(image_file_path):
        return cv2.imread(image_file_path)
    else:
        print("Path {} does not exist".format(image_file_path))


def read_images(image_directory_path, extensions):
    """
    Utility method to read images in a directory using OpenCV
    :param image_directory_path: path to directory containing images
    :param extensions: list of extensions to be selected
    :param config: placeholder for passing  config parameters
    :return:
    """

    if os.path.exists(image_directory_path):

        image_list = []

        for data_file in os.listdir(image_directory_path):
            if data_file.lower().endswith(extensions):
                image_list.append(cv2.imread(os.path.join(image_directory_path, data_file)))

        return image_list
    else:
        print("Path {} does not exist".format(image_directory_path))



def detect_and_crop_contours_old(image):
    """
    detecting and cropping contours from an image
    :param image: image on which contours and crops to be performed
    :return: crops
    """

    gray1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret1, th1 = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # kernel = np.ones((5, 5), 'uint8')
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    par_img = cv2.dilate(th1, kernel, iterations=1)
    (contours, _) = cv2.findContours(par_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    coordinates_list = []
    count = 0
    for cnt in contours:
        crop_coordinates_dict = {}
        x, y, w, h = cv2.boundingRect(cnt)
        cropped_img = image[y:y + h, x:x + w]
        w = (x + w) / (image.shape[1])
        h = (y + h) / (image.shape[0])
        x = x / image.shape[1]
        y = y / image.shape[0]
        coordinates = (x, y, w, h)
        img_save_path = os.path.join(save_path, f'img_{coordinates}_{count}.jpg')
        cv2.imwrite(img_save_path, cropped_img)
        count += 1

        crop_coordinates_dict[coordinates] = cropped_img
        coordinates_list.append(crop_coordinates_dict)
    coordinates_list = sort_crops(coordinates_list)

    return coordinates_list


def crop_contours(image, contour_list, binarize=True, reshape=(1, 50, 50, 1)):

    image_crops = []

    if binarize:
        if reshape[3] != 1:
            raise ValueError("Invalid reshape size - binarized crop should contain only single channel output")

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (thresh, binary_image) = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        for bbox in contour_list:
            (x, y, w, h) = bbox
            cropped_image = binary_image[y:y + h, x:x + w]

            resized_img = cv2.resize(cropped_image, (50, 50))
            cropped_img_resized = resized_img.reshape(1, 50, 50, 1)

            image_crops.append(cropped_img_resized)

        image_crops = np.concatenate(image_crops, axis=0)

    else:
        raise NotImplementedError("Implementation pending cropping with existing color channels")

    return image_crops


def detect_contours(image):
    """
    detecting and cropping contours from an image
    :param image: image on which contours and crops to be performed
    :return: crops
    """

    gray1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret1, th1 = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    par_img = cv2.dilate(th1, kernel, iterations=1)
    (contours, _) = cv2.findContours(par_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_list = [cv2.boundingRect(contour) for contour in contours]
    contour_list = sorted(contour_list, key=lambda bbox: (bbox[1], bbox[0]))

    return contour_list
