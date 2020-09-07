import logging
import os
import pathlib
from typing import IO, List, Union

import numpy as np
from PIL import Image

from .errors import DocumentLoaderException, PasswordProtectedPDFException
from .readers import read_jpg_png, read_pdf, read_tiff
from .types import OutputType

logger = logging.getLogger()


class DocumentLoader(object):

    valid_extentions = {
        ".png": read_jpg_png,
        ".jpg": read_jpg_png,
        ".jpeg": read_jpg_png,
        ".pdf": read_pdf,
        ".tiff": read_tiff,
        ".tif": read_tiff,
    }

    @staticmethod
    def load(
        file: Union[str, IO], output_type: OutputType = OutputType.NP, max_num_pages: int = 1, dpi: int = 300
    ) -> Union[List[Image.Image], List[np.ndarray]]:
        """Loads in a document with a valid extension from filestorage, uploadfile or from disk

        Args:
            file (Union[str, IO]): File path or io object where the document is stored
            output_type (OutputType, optional): OutputType.NP or OutputType.PIL. Defaults to OutputType.NP.
            max_num_pages (int, optional): Max number of pages to return, if set to negative then will use all pages in the document. Defaults to 1.
            dpi (int, optional): dpi to set when converting PDF to an image. Defaults to 300.

        Raises:
            TypeError: If the given file is not a str, pathlib.Path or file-like object with a read method
            DocumentLoaderException: If the extension is not in the list of valid extensions
            DocumentLoaderException: If there was a problem loading - corrupt file
            PasswordProtectedPDFException: If the file was password protected

        Returns:
            A list of PIL Images or numpy arrays
        """
        logger.info("Loading file sent in the request")

        if isinstance(file, str) or isinstance(file, pathlib.Path):  # Covers filepath
            ext = os.path.splitext(file)[1].lower()
        elif hasattr(file, "filename"):  # Covers werkzeug.FileStorage and starlette.UploadFile
            ext = os.path.splitext(file.filename)[1].lower()
        else:
            raise TypeError("file must be a str or io object")

        logger.info(f"Detected extension as {ext}, checking if there is a loader function for that extension")
        loader = DocumentLoader.valid_extentions.get(ext)
        if not loader:
            raise DocumentLoaderException("Invalid extension type, cannot load this type of file")

        try:
            return loader(file, output_type=output_type, max_num_pages=max_num_pages, dpi=dpi)
        except PasswordProtectedPDFException:
            raise
        except FileNotFoundError:
            raise
        except Exception as e:
            raise DocumentLoaderException(f"Corrupt file, failed to load: full error, {e}")
