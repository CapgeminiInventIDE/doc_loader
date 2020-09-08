import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doc_loader",
    version="0.1.1",
    author="Capgemini Invent IDE",
    description="Given werkzeug.FileStorage, fastapi.UploadFile or str file path as input it converts any image files(.pdf, .jpg, .png, .tiff) into list of PIL or numpy objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src", exclude=["tests"]),
    install_requires=["Pillow", "pdf2image", "numpy"],
    url="https://github.com/CapgeminiInventIDE/doc_loader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    keywords=["image loading", "document handling", "PIL wrapper"],
    zip_safe=True,
    python_requires=">=3.6",
    extras_require={"pdf_text_extract": ["PyMuPDF"],},
)
