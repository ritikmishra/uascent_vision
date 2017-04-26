import cv2
import numpy as np


def get_ranges(image, threshold=800):
    """
    :param image: The image to grab the ranges of 
    :param threshold: The minimum sum of a column for it to be considered having an object in it.
    :return: The ranges in which there are objects.
    """
    intervals = []

    for x, col in enumerate(image.T):
        inteval = [0, 0]
        if np.sum(col) >= threshold:
            # if we have stuff
            if x > 0:
                # if we are not at the beginning
                if np.sum(image.T[x-1]) < threshold:
                    # if the column before us does not have stuff
                    # add us as the beginning of the range
                    inteval[0] = x
            else:
                # add us as the start of the range if we are the beginning
                inteval[0] = x

            if x < image.shape[1]:
                # if we are not the end
                if np.sum(image.T[x + 1]) < threshold:
                    # if the column after us does not have stuff
                    # add us to the end
                    inteval[1] = x
            else:
                # add us as the end of the range if we are the end
                inteval[1] = x

        intervals.append(inteval)

    return intervals


def track_range(image):
    """
    :param image: The image to track the ranges of.
    :return: The offset of the thinnest range, so you may use it for 2013 autonomous mode.
    """
    intervals = get_ranges(image)

    filtered_images = []
    filtered_images_dimensions = []
    for interval in intervals:
        blank = np.zeros(image.shape)
        for x, col in image.T:
            if interval[0] <= x <= interval[1]:
                blank[x] = image.T[x]

        filtered_images.append(blank.T)
    for image in filtered_images:
        filtered_images_dimensions.append(objdimensions(image))

    # look for the thinnest one, height-wise
    min_height = None
    min_height_index = 0
    for x, (width, height) in enumerate(filtered_images_dimensions):
        if height < min_height or min_height == 0:
            min_height = height
            min_height_index = x

    filtered_image = filtered_images[min_height_index]
    return [middle(filtered_image), filtered_image]

def middle(img):
    # add up all the values in each column, put into 1d numpy array
    avg = 0
    graph = np.zeros(img.shape[1])
    for y, column in enumerate(img.T):
        graph[y] = np.sum(column) / np.sum(img)

    # weighted average of values in numpy array. Value: x val; Weight: sum
    for x, val in enumerate(graph):
        avg += x * val

    avg = avg - (img.shape[1] / 2)
    return avg


def objdimensions(img):
    """
    :param img: The image to find the dimensions of 
    :return: The dimensions of the image in [width, height] format
    """
    avg_width = avg_calc(width_calc(img))
    avg_height = avg_calc(width_calc(np.rot90(img)))

    return [avg_width, avg_height]


def avg_calc(widths):
    """
    :param widths: A list of widths 
    :return: The average width of the object
    """
    try:
        avg = 0
        for width in widths:
            avg = avg + width
        return avg/len(widths)
    except:
        return 0


def width_calc(img):
    """
    :param img: The image to find the widths of
    :return: A list of the width of the object in each row
    """
    boundaries = gen_boundary(img)
    widths = []
    for (l_boundary, r_boundary) in boundaries:
        widths.append(r_boundary - l_boundary)
    return widths


def gen_boundary(img):
    """
    :param img The image to find the boundaries of
    :return The leftmost and rightmost white pixel in each row.
    """
    boundaries = []
    for rownum, row in enumerate(img):
        if np.sum(row) != 0:
            counter = []
            for col, pixel in enumerate(img[rownum]):
                if pixel > 100:
                    counter.append(col)
            if len(counter) > 2:
                boundaries.append((counter[0], counter[-1]))
    return boundaries



