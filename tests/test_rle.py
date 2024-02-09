# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring, redefined-outer-name
import pytest

from rle_decoder.rle_decoder import RLE

@pytest.fixture
def input_encoded() -> dict:
    d = {
        "counts": "_lm26^b09I4L4M2M3N2O1N2N2O1N101N101O0O100000O1O100N2K6L3M3N2N2O2N1O3L5L3N2M`bb5",
        "size": [600, 500],
    }
    return d

def test_rle_bbox_len(input_encoded: dict):
    rle = RLE(size=input_encoded["size"], counts=input_encoded["counts"])
    assert len(rle.bbox)==4

def test_rle_bbox_types(input_encoded: dict):
    rle = RLE(size=input_encoded["size"], counts=input_encoded["counts"])
    assert all(isinstance(x, int) for x in rle.bbox)

def test_contour_not_empty(input_encoded: dict):
    rle = RLE(size=input_encoded["size"], counts=input_encoded["counts"])
    assert len(rle.contour) > 0

def test_contour_shape(input_encoded: dict):
    rle = RLE(size=input_encoded["size"], counts=input_encoded["counts"])
    assert rle.contour.shape[1] == 2

def test_invalid_counts():
    with pytest.raises(ValueError):
        RLE(size=[600, 500], counts="-").decode()

def test_invalid_size():
    with pytest.raises(TypeError):
        RLE(size=[600, 'hi'], counts="").decode()

def test_invalid_size_len():
    with pytest.raises(IndexError):
        RLE(size=[600], counts="").decode()

def test_invalid_size_type():
    with pytest.raises(TypeError):
        RLE(size=600, counts="").decode()

def test_invalid_counts_type():
    with pytest.raises(TypeError):
        RLE(size=[600, 500], counts=1).decode()
