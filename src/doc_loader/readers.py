import logging
import pathlib
from typing import IO, List, Tuple, Union

import numpy as np
from pdf2image import convert_from_bytes, convert_from_path
from PIL import Image

from .errors import PasswordProtectedPDFException
from .page_counter import pdf_page_count
from .types import OutputType
from .utils import apply_exif_orientation, pil_to_numpy

logger = logging.getLogger()


def read_tiff(
    path: Union[str, IO], output_type: OutputType = OutputType.NP, max_num_pages: int = 1, *args, **kwargs
) -> Tuple[int, Union[List[np.ndarray], List[Image.Image]]]:
    """Reads in an TIFF image and converts it into a list of PIL/numpy images

    Args:
        path (Union[str, IO]): File path or object where the image is stored
        output_type (OutputType, optional): OutputType.NP or OutputType.PIL. Defaults to OutputType.NP.
        max_num_pages (int, optional): Max number of pages to return, if set to negative then will use all pages in the document. Defaults to 1. 

    Raises:
        TypeError: If output_type is not OutputType.NP or OutputType.PIL

    Returns:
        The number of pages in the image, and a list of PIL Images or numpy arrays
    """
    if hasattr(path, "file"):  # Added for starlette.Uploadfile
        path = path.file

    img = Image.open(path)
    if max_num_pages < 0:
        max_num_pages = img.n_frames

    n_frames = max(1, min(max_num_pages, img.n_frames))
    logger.info(f"Loading image as a multi page tiff with {n_frames} pages")
    images = []

    if output_type == OutputType.NP:
        for i in range(n_frames):
            img.seek(i)
            images.append(pil_to_numpy(img.convert("RGB")))
    elif output_type == OutputType.PIL:
        for i in range(n_frames):
            img.seek(i)
            images.append(img.convert("RGB"))
    else:
        raise TypeError(f"output_type must be one of 'np' or 'pil', {output_type}")

    return img.n_frames, images


def read_pdf(
    path: Union[str, IO],
    output_type: OutputType = OutputType.NP,
    max_num_pages: int = 1,
    dpi: int = 300,
    *args,
    **kwargs,
) -> Tuple[int, Union[List[np.ndarray], List[Image.Image]]]:
    """Reads in a PDF and converts it into a list of PIL.Images/np.ndarray, only if given PDF is not password protected

    Args:
        path (Union[str, IO]): File path or object where the image is stored
        output_type (OutputType, optional): OutputType.NP or OutputType.PIL. Defaults to OutputType.NP.
        max_num_pages (int, optional):  Max number of pages to return, if set to negative then will use all pages in the document. Defaults to 1.
        dpi (int, optional): dpi to set when converting PDF to an image. Defaults to 300.

    Raises:
        TypeError: If output_type is not OutputType.NP or OutputType.PIL
        TypeError: If path is not a string or io object
        PasswordProtectedPDFException: If the pdf was password protected

    Returns:
        The number of pages in the image, and a list of PIL Images or numpy arrays
    """
    if hasattr(path, "file"):
        path = path.file

    page_count = pdf_page_count(path)

    if max_num_pages < 0:
        max_num_pages = page_count

    logger.info(f"Loading image as a multi page pdf with {max_num_pages} max pages")

    try:
        if isinstance(path, str) or isinstance(path, pathlib.Path):
            if output_type == OutputType.NP:
                imgs = [
                    pil_to_numpy(im.convert("RGB")) for im in convert_from_path(path, last_page=max_num_pages, dpi=dpi)
                ]
            elif output_type == OutputType.PIL:
                imgs = [im.convert("RGB") for im in convert_from_path(path, last_page=max_num_pages, dpi=dpi)]
            else:
                raise TypeError("output_type must be one of 'np' or 'pil'")

        elif hasattr(path, "read"):
            path.seek(0)
            if output_type == OutputType.NP:
                imgs = [
                    pil_to_numpy(im.convert("RGB"))
                    for im in convert_from_bytes(path.read(), last_page=max_num_pages, dpi=dpi)
                ]
            elif output_type == OutputType.PIL:
                imgs = [im.convert("RGB") for im in convert_from_bytes(path.read(), last_page=max_num_pages, dpi=dpi)]
            else:
                raise TypeError("output_type must be one of 'np' or 'pil'")
        else:
            raise TypeError("path must be string or io object")
    except Exception as e:
        if "Incorrect password" in str(e):
            raise PasswordProtectedPDFException(f"Password protected PDF file path detected, PDF file path = {path}")
        raise

    return page_count, imgs


def read_jpg_png(
    path: Union[str, IO], output_type: OutputType = OutputType.NP, *args, **kwargs
) -> Tuple[int, Union[List[np.ndarray], List[Image.Image]]]:
    """Reads in a JPG or PNG image and converts it into a list of one PIL.Image/np.ndarray

    Args:
        path (Union[str, IO]): File path or object where the image is stored
        output_type (OutputType, optional): OutputType.NP or OutputType.PIL. Defaults to OutputType.NP.

    Raises:
        TypeError: If output_type is not OutputType.NP or OutputType.PIL

    Returns:
        The number of pages in the image, and a list of PIL Images or numpy arrays
    """
    if hasattr(path, "file"):  # Added for starlette.Uploadfile
        path = path.file

    logger.info(f"Loading image as a single jpg/png image")
    if output_type == OutputType.NP:
        return 1, [pil_to_numpy(apply_exif_orientation(Image.open(path).convert("RGB")))]
    elif output_type == OutputType.PIL:
        return 1, [apply_exif_orientation(Image.open(path).convert("RGB"))]
    else:
        raise TypeError("output_type must be one of 'np' or 'pil'")

