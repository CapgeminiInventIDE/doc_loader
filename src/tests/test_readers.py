from contextlib import ExitStack as does_not_raise

import numpy as np
import pytest
from fastapi import UploadFile
from werkzeug.datastructures import FileStorage
from PIL import Image

from src.doc_loader.errors import PasswordProtectedPDFException
from src.doc_loader.readers import *
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


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", TIFF_CASES)
def test_read_tiff_file_storage(path, max_num_pages, expected_pages, output_type, expected_page_count):
    with open(path, "rb") as fp:
        upload_file = UploadFile(path, fp)
        page_count, imgs = read_tiff(upload_file, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", TIFF_CASES)
def test_read_tiff_file_upload(path, max_num_pages, expected_pages, output_type, expected_page_count):
    with open(path, "rb") as fp:
        file_storage = FileStorage(fp, filename=path)
        page_count, imgs = read_tiff(file_storage, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", TIFF_CASES)
def test_read_tiff_file_path(path, max_num_pages, expected_pages, output_type, expected_page_count):
    page_count, imgs = read_tiff(path, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", JPG_CASES)
def test_read_jpg_file_storage(path, max_num_pages, expected_pages, output_type, expected_page_count):
    with open(path, "rb") as fp:
        upload_file = UploadFile(path, fp)
        page_count, imgs = read_jpg_png(upload_file, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", JPG_CASES)
def test_read_jpg_file_upload(path, max_num_pages, expected_pages, output_type, expected_page_count):
    with open(path, "rb") as fp:
        file_storage = FileStorage(fp, filename=path)
        page_count, imgs = read_jpg_png(file_storage, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", JPG_CASES)
def test_read_jpg_file_path(path, max_num_pages, expected_pages, output_type, expected_page_count):
    page_count, imgs = read_jpg_png(path, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", PNG_CASES)
def test_read_png_file_storage(path, max_num_pages, expected_pages, output_type, expected_page_count):
    with open(path, "rb") as fp:
        upload_file = UploadFile(path, fp)
        page_count, imgs = read_jpg_png(upload_file, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", PNG_CASES)
def test_read_png_file_upload(path, max_num_pages, expected_pages, output_type, expected_page_count):
    with open(path, "rb") as fp:
        file_storage = FileStorage(fp, filename=path)
        page_count, imgs = read_jpg_png(file_storage, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", PNG_CASES)
def test_read_png_file_path(path, max_num_pages, expected_pages, output_type, expected_page_count):
    page_count, imgs = read_jpg_png(path, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", PDF_CASES)
def test_read_pdf_file_storage(path, max_num_pages, expected_pages, output_type, expected_page_count):
    with open(path, "rb") as fp:
        upload_file = UploadFile(path, fp)
        page_count, imgs = read_pdf(upload_file, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", PDF_CASES)
def test_read_pdf_file_upload(path, max_num_pages, expected_pages, output_type, expected_page_count):
    with open(path, "rb") as fp:
        file_storage = FileStorage(fp, filename=path)
        page_count, imgs = read_pdf(file_storage, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize("path,max_num_pages,expected_pages,output_type,expected_page_count", PDF_CASES)
def test_read_pdf_file_path(path, max_num_pages, expected_pages, output_type, expected_page_count):
    page_count, imgs = read_pdf(path, max_num_pages=max_num_pages, output_type=output_type)
    assert len(imgs) == expected_pages
    assert page_count == expected_page_count
    if output_type == OutputType.NP or output_type == OutputType.NUMPY:
        assert all([isinstance(im, np.ndarray) for im in imgs])
    elif output_type == OutputType.PIL or output_type == OutputType.PILLOW:
        assert all([isinstance(im, Image.Image) for im in imgs])


@pytest.mark.parametrize(
    "path,expectation",
    [
        (TEST_DATA_DIR / "not-doc-no-text.pdf", does_not_raise()),
        (TEST_DATA_DIR / "not-doc-no-text-locked.pdf", pytest.raises(PasswordProtectedPDFException)),
    ],
)
def test_read_pdf_file_storage_locked(path, expectation):
    with expectation, open(path, "rb") as fp:
        file_storage = FileStorage(fp, filename=path)
        page_count, imgs = read_pdf(file_storage, max_num_pages=-1, output_type=OutputType.PILLOW)


@pytest.mark.parametrize(
    "path,expectation",
    [
        (TEST_DATA_DIR / "not-doc-no-text.pdf", does_not_raise()),
        (TEST_DATA_DIR / "not-doc-no-text-locked.pdf", pytest.raises(PasswordProtectedPDFException)),
    ],
)
def test_read_pdf_file_upload_locked(path, expectation):
    with expectation, open(path, "rb") as fp:
        upload_file = UploadFile(path, fp)
        page_count, imgs = read_pdf(upload_file, max_num_pages=-1, output_type=OutputType.PILLOW)


@pytest.mark.parametrize(
    "path,expectation",
    [
        (TEST_DATA_DIR / "not-doc-no-text.pdf", does_not_raise()),
        (TEST_DATA_DIR / "not-doc-no-text-locked.pdf", pytest.raises(PasswordProtectedPDFException)),
    ],
)
def test_read_pdf_file_path_locked(path, expectation):
    with expectation:
        page_count, imgs = read_pdf(path, max_num_pages=-1, output_type=OutputType.PILLOW)
