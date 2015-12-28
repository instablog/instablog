import os
from PIL import Image



def make_thumbnail(path, width, height):
    filepath, ext = os.path.splitext(path)
    output_path = '{}_thumb{}'.format(filepath, ext)

    if os.path.exists(output_path):
        return output_path

    im = Image.open(path)
    im.thumbnail((width, height, ), Image.ANTIALIAS)
    im.save(output_path)
    im.close()
    return output_path
