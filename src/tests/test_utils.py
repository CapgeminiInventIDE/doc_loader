import os

import numpy as np
import pytest
from PIL import Image
from src.doc_loader.errors import *
from src.doc_loader.utils import pil_to_numpy, apply_exif_orientation

from .utils import TEST_DATA_DIR


@pytest.mark.parametrize("path", [(TEST_DATA_DIR / "is-doc-has-text.jpg")])
def test_pil_to_np(path):
    img = Image.open(path)
    assert isinstance(pil_to_numpy(img), np.ndarray)


@pytest.mark.parametrize(
    "img_with_exif_path,correct_img", [(TEST_DATA_DIR / "tmp.png", TEST_DATA_DIR / "tmp_corrected.png")]
)
def test_apply_exif_orientation(img_with_exif_path, correct_img):
    img = Image.open(img_with_exif_path)
    corrected = apply_exif_orientation(img)
    comparison = pil_to_numpy(corrected) == pil_to_numpy(Image.open(correct_img))
    assert comparison.all()
