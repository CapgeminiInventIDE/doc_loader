import os

import pytest
from fastapi import UploadFile
from werkzeug.datastructures import FileStorage

from src.doc_loader.page_counter import *
from .utils import TEST_DATA_DIR

PDF_CASES = [
    (TEST_DATA_DIR / "is-doc-has-text.pdf", 10),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 10),
    (TEST_DATA_DIR / "not-doc-no-text.pdf", 1),
]


@pytest.mark.parametrize("path", [("/usr/bin/pdfinfo")])
def test_pdfinfo_install(path):
    assert os.path.exists(path)


@pytest.mark.parametrize("path,expected_page_count", PDF_CASES)
def test_pdf_page_count_file_path(path, expected_page_count):
    page_count = pdf_page_count(path)
    assert page_count == expected_page_count


@pytest.mark.parametrize("path,expected_page_count", PDF_CASES)
def test_pdf_page_count_file_upload(path, expected_page_count):
    with open(path, "rb") as fp:
        upload_file = UploadFile(path, fp)
        page_count = pdf_page_count(upload_file)
    assert page_count == expected_page_count


@pytest.mark.parametrize("path,expected_page_count", PDF_CASES)
def test_pdf_page_count_file_storage(path, expected_page_count):
    with open(path, "rb") as fp:
        file_storage = FileStorage(fp, filename=path)
        page_count = pdf_page_count(file_storage)
    assert page_count == expected_page_count


@pytest.mark.parametrize("path,expected_page_count", PDF_CASES)
def test_pdf_page_count_file_upload_pdfinfo_filestorage(path, expected_page_count):
    with open(path, "rb") as fp:
        upload_file = UploadFile(path, fp)
        info = pdfinfo_filestorage(upload_file)
    assert "Pages" in info.keys()
    page_count = int(info["Pages"])
    assert page_count == expected_page_count


@pytest.mark.parametrize("path,expected_page_count", PDF_CASES)
def test_pdf_page_count_file_storage_pdfinfo_filestorage(path, expected_page_count):
    with open(path, "rb") as fp:
        file_storage = FileStorage(fp, filename=path)
        info = pdfinfo_filestorage(file_storage)
    assert "Pages" in info.keys()
    page_count = int(info["Pages"])
    assert page_count == expected_page_count


@pytest.mark.parametrize("path,expected_page_count", PDF_CASES)
def test_pdf_page_count_file_path_pdfinfo(path, expected_page_count):
    info = pdfinfo(path)
    assert "Pages" in info.keys()
    page_count = int(info["Pages"])
    assert page_count == expected_page_count
