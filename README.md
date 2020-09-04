<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Invent_Logo_2COL_RGB.png"><br>
</div>

-----------

# doc_loader

[![PyPI Latest Release](https://img.shields.io/pypi/v/doc_loader.svg)](https://pypi.org/project/doc_loader/)
[![License](https://img.shields.io/pypi/l/doc_loader.svg)](https://github.com/CapgeminiInventIDE/doc_loader/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What is it

doc_loader is a utility package for loading multiple types of documents in the form of images, it can be used to load images into `Pillow` or `numpy` formats and can load from in memory buffers as well as from file paths

## Main Features

* General purpose document loader which accepts .png, .jpg, .jpeg, .pdf, .tiff, .tif formats and outputs list of either PIL (PILLOW) objects or list of numpy arrays
* Handles Password Protected PDFS
* Applies Exif Orientation to .jpg and .png images if present
* Input: `fastapi.UploadFile`, `werkeug.FileStrorage` object or `str` (file path)
* Output: List of images as PIL objects or numpy array

## Where to get it

The source code is currently hosted on GitHub at: https://github.com/CapgeminiInventIDE/doc_loader

Binary installers for the latest released version are available at the [Python package index](https://pypi.org/project/doc_loader/)

```bash
pip install doc_loader
```

## Dependencies

* [Pillow](https://pypi.org/project/Pillow/)
* [numpy](https://pypi.org/project/numpy/)
* [pdf2image](https://pypi.org/project/pdf2image/)

## License

* [BSD 3](/LICENSE)

## Usage

* pip install doc_loader
* In your code where you need to you will be using doc_loader you can refer to below script as reference:

```python
from doc_loader import DocumentLoader, OutputType
from werkzeug.datastructures import FileStorage
from fastapi import UploadFile

path = "demo.jpg"

# Open file using path
document = DocumentLoader.load(path, max_num_pages = 2, output_type=OutputType.NUMPY)
print(document)

# Open file using UploadFile
with open(path, "rb") as fp:
    upload_file = UploadFile(path, fp)
    document = DocumentLoader.load(upload_file, max_num_pages = 2, output_type=OutputType.NUMPY)
print(document)

# Open file using FileStorage
with open(path, "rb") as fp:
    file_storage = FileStorage(fp, filename=path)
    document = DocumentLoader.load(file_storage, max_num_pages = 2, output_type=OutputType.NUMPY)
print(document)
```

## Contributing to doc_loader

To contribute to doc_loader, follow these steps:

1. Fork the repository
2. Create a branch in your own fork: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request back to our fork.

## Contact

If you want to contact use you can reach us at andy.challis@capgemini.com or jeremiah.mannings@capgemini.com
