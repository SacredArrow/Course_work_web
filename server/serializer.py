from PIL import Image
import numpy as np

def to_string(id):
    def binarize_output(img, coeff=0.25):
        size = len(img)
        for i in range(size):
            for j in range(size):
                if i != j:
                    if img[i][j] > 255 * coeff:
                        img[i][j] = 255
                    else:
                        img[i][j] = 0
        return img

    def get_dot(img):
        size = len(img)
        coords = []
        for i in range(size):
            for j in range(size):
                if img[i][j] == 255 and i != j:
                    coords.append((min(i, j), max(i, j)))
        coords = set(coords)
        dot = ['.' for i in range(size)]
        # print(coords)
        for coord in coords:
            if dot[coord[0]] != "." or dot[coord[1]] != ".":
                continue
            if dot[coord[0]] == '.':
                dot[coord[0]] = '('
            # else:
                # print(coord, dot[coord[0]])
                # return 'err'
            if dot[coord[1]] == '.':
                dot[coord[1]] = ')'
            # else:
            #     return 'err'
        return ''.join(dot)

    img = np.array(Image.open("./pics/" + str(id) + "_pred.png"))
    binarized_image = binarize_output(img)
    size = len(img)
    Image.fromarray(binarized_image).save("pics/" + str(id) + '_binarized.png')
    return get_dot(binarized_image)

if __name__ == '__main__':
    import sys
    print(to_string(sys.argv[1]))
