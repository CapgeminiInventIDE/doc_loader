import numpy as np
from PIL import Image


def apply_exif_orientation(image: Image.Image) -> Image.Image:
    """
    Applies the exif orientation correctly.
    This code exists per the bug:
      https://github.com/python-pillow/Pillow/issues/3973
    with the function `ImageOps.exif_transpose`. The Pillow source raises errors with
    various methods, especially `tobytes`
    Function based on:
      https://github.com/wkentaro/labelme/blob/v4.5.4/labelme/utils/image.py#L59
      https://github.com/python-pillow/Pillow/blob/7.1.2/src/PIL/ImageOps.py#L527
    Args:
        image (Image.Image): a PIL image
    Returns:
        (Image.Image): the PIL image with exif orientation applied, if applicable
    """
    if not hasattr(image, "getexif"):
        return image

    try:
        exif = image.getexif()
    except Exception:  # https://github.com/facebookresearch/detectron2/issues/1885
        exif = None

    if exif is None:
        return image
    # https://www.exiv2.org/tags.html
    _EXIF_ORIENT = 274  # exif 'Orientation' tag

    # raise Exception(f"EXIF {exif}")

    orientation = exif.get(_EXIF_ORIENT)

    method = {
        2: Image.FLIP_LEFT_RIGHT,
        3: Image.ROTATE_180,
        4: Image.FLIP_TOP_BOTTOM,
        5: Image.TRANSPOSE,
        6: Image.ROTATE_270,
        7: Image.TRANSVERSE,
        8: Image.ROTATE_90,
    }.get(orientation)

    if method is not None:
        return image.transpose(method)
    return image


def pil_to_numpy(image: Image.Image) -> np.ndarray:
    """Convert PIL image to numpy array of target format.

    Args:
        image (Image.Image): A PIL image to convert to numpy

    Returns:
        np.ndarray: Image 
    """
    return np.asarray(image.convert("RGB"))
