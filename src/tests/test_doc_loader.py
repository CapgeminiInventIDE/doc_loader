import pytest

from werkzeug.datastructures import FileStorage
from fastapi import UploadFile

from src.doc_loader.doc_loader import *
from src.doc_loader.errors import DocumentLoaderException, PasswordProtectedPDFException
from src.doc_loader.types import OutputType

from .utils import TEST_DATA_DIR

TIFF_CASES = [
    (TEST_DATA_DIR / "not-doc-no-text.tif", 1, 1, OutputType.NP, 1),
    (TEST_DATA_DIR / "not-doc-no-text.tiff", 1, 1, OutputType.NP, 1),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 1, 1, OutputType.NP, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 5, 5, OutputType.NP, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 50, 10, OutputType.NP, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", -1, 10, OutputType.NP, 10),
    #
    (TEST_DATA_DIR / "not-doc-no-text.tif", 1, 1, OutputType.NUMPY, 1),
    (TEST_DATA_DIR / "not-doc-no-text.tiff", 1, 1, OutputType.NUMPY, 1),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 1, 1, OutputType.NUMPY, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 5, 5, OutputType.NUMPY, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 50, 10, OutputType.NUMPY, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", -1, 10, OutputType.NUMPY, 10),
    #
    (TEST_DATA_DIR / "not-doc-no-text.tif", 1, 1, OutputType.PIL, 1),
    (TEST_DATA_DIR / "not-doc-no-text.tiff", 1, 1, OutputType.PIL, 1),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 1, 1, OutputType.PIL, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 5, 5, OutputType.PIL, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 50, 10, OutputType.PIL, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", -1, 10, OutputType.PIL, 10),
    #
    (TEST_DATA_DIR / "not-doc-no-text.tif", 1, 1, OutputType.PILLOW, 1),
    (TEST_DATA_DIR / "not-doc-no-text.tiff", 1, 1, OutputType.PILLOW, 1),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 1, 1, OutputType.PILLOW, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 5, 5, OutputType.PILLOW, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", 50, 10, OutputType.PILLOW, 10),
    (TEST_DATA_DIR / "is-doc-has-text.tiff", -1, 10, OutputType.PILLOW, 10),
]

JPG_CASES = [
    (TEST_DATA_DIR / "is-doc-has-text.jpg", 1, 1, OutputType.NP, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 1, 1, OutputType.NP, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpg", 1, 1, OutputType.NP, 1),
    #
    (TEST_DATA_DIR / "is-doc-has-text.jpg", 1, 1, OutputType.NUMPY, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 1, 1, OutputType.NUMPY, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpg", 1, 1, OutputType.NUMPY, 1),
    #
    (TEST_DATA_DIR / "is-doc-has-text.jpg", 1, 1, OutputType.PIL, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 1, 1, OutputType.PIL, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpg", 1, 1, OutputType.PIL, 1),
    #
    (TEST_DATA_DIR / "is-doc-has-text.jpg", 1, 1, OutputType.PILLOW, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 1, 1, OutputType.PILLOW, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpg", 1, 1, OutputType.PILLOW, 1),
    #
    (TEST_DATA_DIR / "is-doc-has-text.jpg", -1, 1, OutputType.NP, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 50, 1, OutputType.NP, 1),
    #
    (TEST_DATA_DIR / "is-doc-has-text.jpg", -1, 1, OutputType.PIL, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 50, 1, OutputType.PIL, 1),
]

PNG_CASES = [
    (TEST_DATA_DIR / "is-doc-has-text.jpg", 1, 1, OutputType.NP, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 1, 1, OutputType.NP, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpg", 1, 1, OutputType.NP, 1),
    #
    (TEST_DATA_DIR / "is-doc-has-text.jpg", 1, 1, OutputType.NUMPY, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 1, 1, OutputType.NUMPY, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpg", 1, 1, OutputType.NUMPY, 1),
    #
    (TEST_DATA_DIR / "is-doc-has-text.jpg", 1, 1, OutputType.PIL, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 1, 1, OutputType.PIL, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpg", 1, 1, OutputType.PIL, 1),
    #
    (TEST_DATA_DIR / "is-doc-has-text.jpg", 1, 1, OutputType.PILLOW, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 1, 1, OutputType.PILLOW, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpg", 1, 1, OutputType.PILLOW, 1),
    #
    (TEST_DATA_DIR / "is-doc-has-text.jpg", -1, 1, OutputType.NP, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 50, 1, OutputType.NP, 1),
    #
    (TEST_DATA_DIR / "is-doc-has-text.jpg", -1, 1, OutputType.PIL, 1),
    (TEST_DATA_DIR / "not-doc-has-text.jpeg", 50, 1, OutputType.PIL, 1),
]

PDF_CASES = [
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 1, 1, OutputType.NP, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", -1, 10, OutputType.NP, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 5, 5, OutputType.NP, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 99, 10, OutputType.NP, 10),
    #
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 1, 1, OutputType.NP, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", -1, 10, OutputType.NP, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 5, 5, OutputType.NP, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 99, 10, OutputType.NP, 10),
    #
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 1, 1, OutputType.NP, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", -1, 1, OutputType.NP, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 5, 1, OutputType.NP, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 99, 1, OutputType.NP, 1),
    ##
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 1, 1, OutputType.NUMPY, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", -1, 10, OutputType.NUMPY, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 5, 5, OutputType.NUMPY, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 99, 10, OutputType.NUMPY, 10),
    #
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 1, 1, OutputType.NUMPY, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", -1, 10, OutputType.NUMPY, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 5, 5, OutputType.NUMPY, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 99, 10, OutputType.NUMPY, 10),
    #
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 1, 1, OutputType.NUMPY, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", -1, 1, OutputType.NUMPY, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 5, 1, OutputType.NUMPY, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 99, 1, OutputType.NUMPY, 1),
    ##
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 1, 1, OutputType.PIL, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", -1, 10, OutputType.PIL, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 5, 5, OutputType.PIL, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 99, 10, OutputType.PIL, 10),
    #
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 1, 1, OutputType.PIL, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", -1, 10, OutputType.PIL, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 5, 5, OutputType.PIL, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 99, 10, OutputType.PIL, 10),
    #
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 1, 1, OutputType.PIL, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", -1, 1, OutputType.PIL, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 5, 1, OutputType.PIL, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 99, 1, OutputType.PIL, 1),
    ##
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 1, 1, OutputType.PILLOW, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", -1, 10, OutputType.PILLOW, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 5, 5, OutputType.PILLOW, 10),
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 99, 10, OutputType.PILLOW, 10),
    #
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 1, 1, OutputType.PILLOW, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", -1, 10, OutputType.PILLOW, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 5, 5, OutputType.PILLOW, 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 99, 10, OutputType.PILLOW, 10),
    #
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 1, 1, OutputType.PILLOW, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", -1, 1, OutputType.PILLOW, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 5, 1, OutputType.PILLOW, 1),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 99, 1, OutputType.PILLOW, 1),
]

ALL_CASES = TIFF_CASES + JPG_CASES + PNG_CASES + PDF_CASES


@pytest.mark.parametrize(
    "path,max_num_pages,expected_pages,output_type,expected_page_count", ALL_CASES,
)
def test_docloader_file_upload(path, max_num_pages, expected_pages, output_type, expected_page_count):
    with open(path, "rb") as fp:
        upload_file = UploadFile(path, fp)
        page_count, imgs = DocumentLoader.load(upload_file, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize(
    "path,max_num_pages,expected_pages,output_type,expected_page_count", ALL_CASES,
)
def test_docloader_file_storage(path, max_num_pages, expected_pages, output_type, expected_page_count):
    with open(path, "rb") as fp:
        file_storage = FileStorage(fp, filename=path)
        page_count, imgs = DocumentLoader.load(file_storage, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize(
    "path,max_num_pages,expected_pages,output_type,expected_page_count", ALL_CASES,
)
def test_docloader_file_path(path, max_num_pages, expected_pages, output_type, expected_page_count):
    page_count, imgs = DocumentLoader.load(path, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize(
    "path,expectation",
    [
        (TEST_DATA_DIR / "corrupt.jpg", pytest.raises(DocumentLoaderException)),
        (TEST_DATA_DIR / "corrupt.pdf", pytest.raises(DocumentLoaderException)),
        (TEST_DATA_DIR / "corrupt.png", pytest.raises(DocumentLoaderException)),
        (TEST_DATA_DIR / "corrupt.tiff", pytest.raises(DocumentLoaderException)),
    ],
)
def test_docloader_corrupt_error(path, expectation):
    with expectation:
        page_count, imgs = DocumentLoader.load(path, max_num_pages=-1, output_type=OutputType.PILLOW)


@pytest.mark.parametrize("path,expectation", [(TEST_DATA_DIR / "demo.txt", pytest.raises(DocumentLoaderException))])
def test_docloader_filepath_error(path, expectation):
    with expectation:
        page_count, imgs = DocumentLoader.load(path, max_num_pages=-1, output_type=OutputType.PILLOW)


@pytest.mark.parametrize(
    "path,expectation", [(TEST_DATA_DIR / "not-doc-no-text-locked.pdf", pytest.raises(PasswordProtectedPDFException))]
)
def test_docloader_locked_error(path, expectation):
    with expectation:
        page_count, imgs = DocumentLoader.load(path, max_num_pages=-1, output_type=OutputType.PILLOW)
