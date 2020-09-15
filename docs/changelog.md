# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [v0.1.2](https://github.com/CapgeminiInventIDE/doc_loader/releases/tag/v0.1.2) - 2020-09-08

* Add error handling to password protected searchable pdf's

## [v0.1.1](https://github.com/CapgeminiInventIDE/doc_loader/releases/tag/v0.1.1) - 2020-09-08

* Apply patch to Pillow dependency from 7.0.0 to 7.2.0

## [v0.1.0](https://github.com/CapgeminiInventIDE/doc_loader/releases/tag/v0.1.0) - 2020-09-08

Initial commit of code, includes:

* Loading from fastapi.UploadFile
* Loading from werkzeug.FileStorage
* Loading from local file using str or pathlib.Path
* Output as List[PIL.Image] or List[np.ndarray]
* Applys EXIF orientation to jpg/png if it can
* Handles TIFF, JPG, PNG, PDF files
* Handles password protected PDF's with exceptions
* Able to choose dpi of pdf to image rendering
* 674 unit tests with high coverage
* 100% Docstring coverage
