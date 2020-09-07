## Installation

```bash
pip install doc_loader
```

Optionally you can also install the package with extra features

```bash
pip install doc_loader[pdf_text_extract]
```

This plugin allows you to get text from a searchable pdf

## Core package usage

=== "Files on disk"

    ```python
    from doc_loader import DocumentLoader, OutputType

    path = "/opt/working/src/tests/data/tmp.png"

    # Open file using path
    page_count, document = DocumentLoader.load(path, max_num_pages = 2, output_type=OutputType.NUMPY)
    print(page_count, document)
    ```

=== "Files in memory - fastapi.UploadFile"

    ```python
    from doc_loader import DocumentLoader, OutputType
    from fastapi import UploadFile

    path = "/opt/working/src/tests/data/tmp.png"

    # Open file using UploadFile
    with open(path, "rb") as fp:
        upload_file = UploadFile(path, fp)
        page_count, document = DocumentLoader.load(upload_file, max_num_pages = 2, output_type=OutputType.NUMPY)

    print(page_count, document)
    ```

=== "Files in memory - werkzeug.FileStorage" 

    ```python
    from doc_loader import DocumentLoader, OutputType
    from werkzeug.datastructures import FileStorage

    path = "/opt/working/src/tests/data/tmp.png"

    # Open file using FileStorage
    with open(path, "rb") as fp:
        file_storage = FileStorage(fp, filename=path)
        page_count, document = DocumentLoader.load(file_storage, max_num_pages = 2, output_type=OutputType.NUMPY)

    print(page_count, document)
    ```

## PDF text extraction - Optional

* `extract_text_pdf` - allows you to get text from a searchable pdf if possible, otherwise will raise an error that can be handled, to use this `pip install doc_loader[pdf_text_extract]`

=== "Files on disk"

    ```python
    from doc_loader import extract_text_pdf

    path = "/opt/working/src/tests/data/is-doc-has-cgtext.pdf"

    # Open file using path
    page_count, document = extract_text_pdf(path, max_num_pages = 2)
    print(page_count, document)
    ```

=== "Files in memory - fastapi.UploadFile"

    ```python
    from doc_loader import extract_text_pdf
    from fastapi import UploadFile

    path = "/opt/working/src/tests/data/is-doc-has-cgtext.pdf"

    # Open file using UploadFile
    with open(path, "rb") as fp:
        upload_file = UploadFile(path, fp)
        page_count, document = extract_text_pdf(upload_file, max_num_pages = 2)

    print(page_count, document)
    ```

=== "Files in memory - werkzeug.FileStorage" 

    ```python
    from doc_loader import extract_text_pdf
    from werkzeug.datastructures import FileStorage

    path = "/opt/working/src/tests/data/is-doc-has-cgtext.pdf"

    # Open file using FileStorage
    with open(path, "rb") as fp:
        file_storage = FileStorage(fp, filename=path)
        page_count, document = extract_text_pdf(file_storage, max_num_pages = 2)

    print(page_count, document)
    ```
