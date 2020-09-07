import logging
import os
import pathlib
import subprocess
import tempfile
from typing import IO, Dict, Union

from .errors import PasswordProtectedPDFException, PDFInfoException, PDFInfoFileNotFoundException

logger = logging.getLogger()


def pdf_page_count(file: Union[str, IO]) -> int:
    """Gets the page count for a pdf using pdf info

    Args:
        file (Union[str, IO]): File path or io object where the document is stored

    Raises:
        TypeError: If file is not str, pathlib.Path or io object with `read` method

    Returns:
        The page count inside the pdf
    """
    if hasattr(file, "file"):
        file = file.file

    if isinstance(file, str) or isinstance(file, pathlib.Path):
        count = pdfinfo(str(file)).get("Pages", None)
    elif hasattr(file, "read"):
        logger.info(f"Determining page count for file")
        count = pdfinfo_filestorage(file).get("Pages", None)
    else:
        raise TypeError(f"file must be a str or io object: {file}")
    if count:
        logger.info(f"Detected {count} pages in file")
        return int(count)
    logger.info(f"Failed to determine number of pages in file")
    return count


def pdfinfo_filestorage(file_storage: IO) -> Dict[str, str]:
    """Wraps the functionality of pdfinfo to be used on fastapi.UploadFile and werkzeug.FileStorage objects

    Args:
        file_storage (IO): IO buffer PDF file to extract info from

    Returns:
        The metainfo in a dictionary
    """
    if hasattr(file_storage, "file"):
        file_storage = file_storage.file

    fh, temp_filename = tempfile.mkstemp()
    try:
        with open(temp_filename, "wb") as f:
            file_storage.seek(0)
            f.write(file_storage.read())
            file_storage.seek(0)
            f.flush()
            try:
                return pdfinfo(f.name)
            except Exception as e:
                raise
    finally:
        os.close(fh)
        os.remove(temp_filename)


def pdfinfo(path: str) -> Dict[str, str]:
    """
    Wraps command line utility pdfinfo to extract the PDF meta information using poppler-utils

    This function parses the text output that looks like this:
    ```
        Title:          PUBLIC MEETING AGENDA
        Author:         Customer Support
        Creator:        Microsoft Word 2010
        Producer:       Microsoft Word 2010
        CreationDate:   Thu Dec 20 14:44:56 2012
        ModDate:        Thu Dec 20 14:44:56 2012
        Tagged:         yes
        Pages:          2
        Encrypted:      no
        Page size:      612 x 792 pts (letter)
        File size:      104739 bytes
        Optimized:      no
        PDF version:    1.5
    ```
    Args:
        path (str): Path to file
    
    Raises:
        PDFInfoException: If pdfinfo cannot be found in the path
        PDFInfoFileNotFoundException: If the file to be processed could not be found by pdfinfo
        PasswordProtectedPDFException: If the pdf file was password protected
    
    Returns:
        The metainfo in a dictionary.
    """

    cmd = "/usr/bin/pdfinfo"
    if not os.path.exists(cmd):
        raise PDFInfoException(f"System command not found: {cmd}")

    if not os.path.exists(path):
        raise PDFInfoFileNotFoundException(f"Provided input file not found: {path}")

    def _extract(row):
        """Extracts the right hand value from a : delimited row"""
        return row.split(":", 1)[1].strip().rstrip("'")

    output = {}

    labels = [
        "Title",
        "Author",
        "Creator",
        "Producer",
        "CreationDate",
        "ModDate",
        "Tagged",
        "Pages",
        "Encrypted",
        "Page size",
        "File size",
        "Optimized",
        "PDF version",
    ]
    try:
        cmd_output = subprocess.check_output([cmd, path], stderr=subprocess.STDOUT)
        for line in map(str, cmd_output.splitlines()):
            for label in labels:
                if label in line:
                    output[label] = _extract(line)

        return output
    except subprocess.CalledProcessError as e:
        if "Incorrect password" in e.output.decode("utf-8"):
            raise PasswordProtectedPDFException(f"PDF file is password protected: {e.output.decode('utf-8')}")
        raise
    except:
        raise
