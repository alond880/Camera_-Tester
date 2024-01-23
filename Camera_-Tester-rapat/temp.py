from PIL import Image, ImageDraw


dead_value = (1, 1, 1)


def load_image(image_path, x, y):
    im = Image.open(image_path)  # Can be many different formats.
    pix = im.load()
    im.show()

    return im, pix


def scan_image(image, pix):
    global dead_value
    dead_pixels = []
    width, height = image.size
    section0 = [10, 10]  # center area
    section1 = [50, 50]  # middle area
    section2 = [100, 100]  # large area (frame and edges)

    # scan entire image
    for i in range(0, width):
        for j in range(0, height):
            if pix[i, j] == dead_value:
                dead_pixels.append([i, j])
                print([i, j])


if __name__ == '__main__':
    img, pix = load_image("C:/Users/Rapat/PycharmProjects/elbit_GUI/image.jpg", 0, 0)
    scan_image(img, pix)
