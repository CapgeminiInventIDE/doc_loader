import os
from contextlib import ExitStack as does_not_raise

import pytest
from fastapi import UploadFile
from werkzeug.datastructures import FileStorage

try:
    should_test_extract_text_pdf = False
    import fitz

    should_test_extract_text_pdf = True
except:
    pass

from src.doc_loader.utils import optional_import
from src.doc_loader.pdf_extract import extract_text_pdf
from .utils import TEST_DATA_DIR
from src.doc_loader.errors import NoTextToExtractError, PasswordProtectedPDFException

PDF_CG_CASES = [
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 10, -1,),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 10, 5,),
    (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", 10, 1,),
]


@pytest.mark.parametrize("path", [(TEST_DATA_DIR / "is-doc-has-text.pdf")])
def test_fitz_open_install(path):
    fitz_open = optional_import("fitz", name="open", package="PyMuPDF")
    if should_test_extract_text_pdf:
        with does_not_raise():
            fitz_open(path)
    else:
        with pytest.raises(ValueError):
            fitz_open(path)


if should_test_extract_text_pdf:

    @pytest.mark.parametrize("path", [("/usr/bin/mupdf")])
    def test_mupdf_install(path):
        assert os.path.exists(path)

    cg_text = [
        "PrintNode Multi \nPage Test Start\n1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "PrintNode \nMultipage Test End\n10",
    ]

    PDF_CG_CASES_ERRORS = [
        (TEST_DATA_DIR / "is-doc-has-text.pdf", pytest.raises(NoTextToExtractError)),
        (TEST_DATA_DIR / "not-doc-no-text-locked.pdf", pytest.raises(PasswordProtectedPDFException)),
        (TEST_DATA_DIR / "is-doc-has-cgtext.pdf", does_not_raise()),
    ]

    @pytest.mark.parametrize(
        "path,expectation", PDF_CG_CASES_ERRORS,
    )
    def test_extract_text_pdf_file_path_error(path, expectation):
        with expectation:
            extract_text_pdf(path, max_num_pages=-1)

    @pytest.mark.parametrize(
        "path,expectation", PDF_CG_CASES_ERRORS,
    )
    def test_extract_text_pdf_file_storage_error(path, expectation):
        with expectation, open(path, "rb") as fp:
            file_storage = FileStorage(fp, filename=path)
            extract_text_pdf(file_storage, max_num_pages=-1)

    @pytest.mark.parametrize(
        "path,expectation", PDF_CG_CASES_ERRORS,
    )
    def test_extract_text_pdf_file_upload_error(path, expectation):
        with expectation, open(path, "rb") as fp:
            upload_file = UploadFile(path, fp)
            extract_text_pdf(upload_file, max_num_pages=-1)

    @pytest.mark.parametrize(
        "path,expected_page_count,max_num_pages", PDF_CG_CASES,
    )
    def test_extract_text_pdf_file_path(path, expected_page_count, max_num_pages):
        if (len(cg_text) < max_num_pages) or (max_num_pages < 0):
            max_index = len(cg_text) + 1
        else:
            max_index = max_num_pages
        page_count, extracted_text = extract_text_pdf(path, max_num_pages=max_num_pages)
        print(extracted_text)
        print(cg_text[:max_index])
        assert page_count == expected_page_count
        assert extracted_text == cg_text[:max_index]

    @pytest.mark.parametrize(
        "path,expected_page_count,max_num_pages", PDF_CG_CASES,
    )
    def test_extract_text_pdf_file_storage(path, expected_page_count, max_num_pages):
        if (len(cg_text) < max_num_pages) or (max_num_pages < 0):
            max_index = len(cg_text) + 1
        else:
            max_index = max_num_pages
        with open(path, "rb") as fp:
            file_storage = FileStorage(fp, filename=path)
            page_count, extracted_text = extract_text_pdf(file_storage, max_num_pages=max_num_pages)
        print(extracted_text)
        print(cg_text[:max_index])
        assert page_count == expected_page_count
        assert extracted_text == cg_text[:max_index]

    @pytest.mark.parametrize(
        "path,expected_page_count,max_num_pages", PDF_CG_CASES,
    )
    def test_extract_text_pdf_file_upload(path, expected_page_count, max_num_pages):
        if (len(cg_text) < max_num_pages) or (max_num_pages < 0):
            max_index = len(cg_text) + 1
        else:
            max_index = max_num_pages
        with open(path, "rb") as fp:
            upload_file = UploadFile(path, fp)
            page_count, extracted_text = extract_text_pdf(upload_file, max_num_pages=max_num_pages)
        print(extracted_text)
        print(cg_text[:max_index])
        assert page_count == expected_page_count
        assert extracted_text == cg_text[:max_index]

