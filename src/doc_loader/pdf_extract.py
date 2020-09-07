import io
import logging
import pathlib
from typing import IO, Union, List, Callable, Tuple

from .errors import NoTextToExtractError
from .page_counter import pdf_page_count
from .utils import optional_import

# Will lazily import the function open if available, if not will return a function that will raise an ImportException
fitz_open = optional_import("fitz", name="open", package="PyMuPDF")

logger = logging.getLogger()


def extract_text_pdf(
    path: Union[str, IO], max_num_pages: int = 1, postprocess_page: Callable = lambda x: x.strip(), *args, **kwargs
) -> Tuple[int, List[str]]:
    """Extracts the text in every page within a readable PDF file

    Args:
        path (Union[str, IO]): File path or io object where the document is stored
        max_num_pages (int, optional): Max number of pages to return, if set to negative then will use all pages in the document. Defaults to 1.
        postprocess_page (Callable, optional): Function to pass to postprocess the text on each page. Defaults to lambda x:x.strip().

    Raises:
        TypeError: If the given file is not a str, pathlib.Path or file-like object with a read method
        NoTextToExtractError: If the function failed to extract any text (eg pdf with all images)

    Returns:
        Number of pages in the, list of text in each page
    """

    if hasattr(path, "file"):
        path = path.file

    page_count = pdf_page_count(path)

    if max_num_pages < 0:
        max_num_pages = page_count

    logger.info(f"Passing file through MuPDF as a multi page pdf with {max_num_pages} max pages")

    # Converting file into BytesIO
    memf = io.BytesIO()
    if hasattr(path, "read"):
        memf.write(path.read())
        memf.seek(0)
        document = fitz_open(stream=memf, filetype="pdf")
    elif isinstance(path, str) or isinstance(path, pathlib.Path):
        document = fitz_open(str(path), filetype="pdf")
    else:
        raise TypeError("path must be string or io object")

    # Reading file and extracting text
    text = []
    for i, page in enumerate(document):
        if i + 1 > max_num_pages:
            break
        t = postprocess_page(page.getText("text"))
        text.append(t)

    full_text_len = len("".join(text))

    if full_text_len > 0:
        return page_count, text
    raise NoTextToExtractError(f"File has length {full_text_len}", 1008)
