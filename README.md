<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Invent_Logo_2COL_RGB.png" style="width:80%;"><br>
</div>

-----------

# doc_loader

[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://capgeminiinventide.github.io/doc_loader/index.html)
[![Discord](https://img.shields.io/discord/752353026366242846.svg?label=Join%20us%20on%20Discord&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/rQcMtVE)
[![PyPI Latest Release](https://img.shields.io/pypi/v/doc_loader.svg)](https://pypi.org/project/doc_loader/)
[![License](https://img.shields.io/pypi/l/doc_loader.svg)](https://github.com/CapgeminiInventIDE/doc_loader/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What is it

doc_loader is a utility package for loading multiple types of documents in the form of images, it can be used to load images into `Pillow` or `numpy` formats and can load from in memory buffers as well as from file paths

## Main Features

* General purpose document loader which accepts .png, .jpg, .jpeg, .pdf, .tiff, .tif formats and outputs list of either PIL.Image objects or list of numpy arrays
* Handles Password Protected PDF's
* Applies Exif Orientation to .jpg and .png images if present
* Input: `fastapi.UploadFile`, `werkeug.FileStorage` object or `str` (file path)
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
* [pdf2image](https://pypi.org/project/pdf2image/) + popplerutils
* OPTIONAL [PyMuPDF](https://pypi.org/project/PyMuPDF/) + MuPDF

## License

* [Mozilla Public License 2.0](/LICENSE)

## Usage

* pip install doc_loader
* In your code where you need to you will be using doc_loader you can refer to below script as reference:

```python
from doc_loader import DocumentLoader, OutputType
from werkzeug.datastructures import FileStorage
from fastapi import UploadFile

path = "/opt/working/src/tests/data/tmp.png"

# Open file using path
page_count, document = DocumentLoader.load(path, max_num_pages = 2, output_type=OutputType.NUMPY)
print(page_count, document)

# Open file using UploadFile
with open(path, "rb") as fp:
    upload_file = UploadFile(path, fp)
    page_count, document = DocumentLoader.load(upload_file, max_num_pages = 2, output_type=OutputType.NUMPY)

print(page_count, document)

# Open file using FileStorage
with open(path, "rb") as fp:
    file_storage = FileStorage(fp, filename=path)
    page_count, document = DocumentLoader.load(file_storage, max_num_pages = 2, output_type=OutputType.NUMPY)

print(page_count, document)
```

## Optional features

* `extract_text_pdf` - allows you to get text from a searchable pdf if possible, otherwise will raise an error that can be handled, to use this `pip install doc_loader[pdf_text_extract]`

```python
from doc_loader import extract_text_pdf
from werkzeug.datastructures import FileStorage
from fastapi import UploadFile

path = "/opt/working/src/tests/data/is-doc-has-cgtext.pdf"

# Open file using path
page_count, document = extract_text_pdf(path, max_num_pages = 2)
print(page_count, document)

# Open file using UploadFile
with open(path, "rb") as fp:
    upload_file = UploadFile(path, fp)
    page_count, document = extract_text_pdf(upload_file, max_num_pages = 2)

print(page_count, document)

# Open file using FileStorage
with open(path, "rb") as fp:
    file_storage = FileStorage(fp, filename=path)
    page_count, document = extract_text_pdf(file_storage, max_num_pages = 2)

print(page_count, document)
```

## Contributing to doc_loader

To contribute to doc_loader, follow these steps:

1. Fork the repository
2. Create a branch in your own fork: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request back to our fork.

## About Us

### Capgemini Invent combines strategy, technology, data science and creative design to solve the most complex business and technology challenges.

Disruption is not new, but the pace of change is. The fourth industrial revolution is forcing businesses to rethink everything they know.

Leading organizations behave as living entities, constantly adapting to change. With invention at their core, they continuously redesign their business to generate new sources of value. Winning is about fostering inventive thinking to create what comes next.

### Invent. Build. Transform.

This is why we have created Capgemini Invent, Capgemini’s new digital innovation, consulting and transformation global business line. Our multi-disciplinary team helps business leaders find new sources of value. We accelerate the process of turning ideas into prototypes and scalable real-world solutions; leveraging the full business and technology expertise of the Capgemini Group to implement at speed and scale.

The result is a coordinated approach to transformation, enabling businesses to create the products, services, customer experiences, and business models of the future.

## We're Hiring!

Do you want to be part of the team that builds doc_loader and [other great products](https://github.com/CapgeminiInventIDE) at Capgemini Invent? If so, you're in luck! Capgemini Invent is currently hiring Data Scientists who love using data to drive their decisions. Take a look at [our open positions](https://www.capgemini.com/careers/job-search/?search_term=capgemini+invent) and see if you're a fit.
