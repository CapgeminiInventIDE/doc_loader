import importlib
from typing import Callable

import numpy as np
from PIL import Image


def apply_exif_orientation(image: Image.Image) -> Image.Image:
    """Applies the exif orientation correctly.
    
    Args:
        image (Image.Image): a PIL image
    Returns:
        The PIL image with exif orientation applied, if applicable

    ```
    This code exists per the bug:
      https://github.com/python-pillow/Pillow/issues/3973
    with the function `ImageOps.exif_transpose`. The Pillow source raises errors with
    various methods, especially `tobytes`
    Function based on:
      https://github.com/wkentaro/labelme/blob/v4.5.4/labelme/utils/image.py#L59
      https://github.com/python-pillow/Pillow/blob/7.1.2/src/PIL/ImageOps.py#L527
    ```
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
        The PIL image converted to a numpy array
    """
    return np.asarray(image.convert("RGB"))


def optional_import(module: str, name: str = None, package: str = None) -> Callable:
    """Allows us to make an optional import

    Args:
        module (str): Name of the module we want to load eg yaml
        name (str, optional): name of the function you want to load. Defaults to None.
        package (str, optional): Name of the package incase it is different from the module name. Defaults to None.

    Example:
        ```python
        from yaml import safe_load as load
        # would be
        load = optional_import('yaml', 'safe_load', package='pyyaml')
        ```
    Raises:
        ValueError: If there was an import error for the module that was trying to be loaded

    Returns:
        Either a function to raise the exception or the function from the module
    """
    try:
        module = importlib.import_module(module)
        return module if name is None else getattr(module, name)
    except ImportError as e:
        if package is None:
            package = module
        msg = f"install the '{package}' package to make use of this feature"
        import_error = e

        def _failed_import(*args, **kwargs):
            raise ValueError(msg) from import_error

        return _failed_import
