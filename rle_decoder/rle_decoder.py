from dataclasses import dataclass
from typing import List, Dict, Any

import numpy as np
import numpy.typing as npt
import cv2
from pycocotools import mask as cocomask  # type: ignore


@dataclass
class RLE:
    size: List[int]
    counts: List[int] | str

    def _contour(self, remove_small_objects:bool=False, min_area:int=200, merge_contours=False) -> npt.ArrayLike:
        mask_decoded = self.decode()
        contours, hierarchy = cv2.findContours(
            mask_decoded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        # Sort contours by area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        if remove_small_objects:
            contours = [c for c in contours if cv2.contourArea(c) > min_area]
        if merge_contours:
            contour = np.concatenate(contours)
        else:
            contour = contours[0]
        return contour.reshape(-1, 2)

    @property
    def contour(self) -> npt.ArrayLike:
        return self._contour().tolist()

    @property
    def binary_mask(self) -> npt.NDArray[np.uint8]:
        return self.decode()

    @property
    def area(self) -> float:
        return int(cv2.contourArea(self._contour()))

    @property
    def perimeter(self) -> float:
        return int(cv2.arcLength(self._contour(), True))

    @property
    def compactness(self) -> float:
        return round(self.perimeter ** 2 / self.area, 3)

    def _centroid(self) -> np.ndarray:
        cnt = self._contour()
        M = cv2.moments(cnt)
        centroid = np.array(
            [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])]
        )
        return centroid

    @property
    def centroid(self) -> np.ndarray:
        return self._centroid().tolist()

    # More moments https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
    @property
    def moments(self) -> Dict[str, float]:
        cnt = self._contour()
        M = cv2.moments(cnt)
        return M

    @property
    def rle(self) -> Dict[str, Any]:
        return dict(size=self.size, counts=self.counts)

    @property
    def bbox(self) -> List:
        return cocomask.toBbox(self.rle).ravel().astype(int).tolist()

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RLE":
        return cls(size=d["size"], counts=d["counts"])

    # Add two RLE objects
    def __add__(self, other):
        return RLE(**cocomask.merge([self.rle, other.rle]))

    def to_dict(self) -> Dict[str, Any]:
        return self.rle

    def decode(self) -> np.ndarray:
        d = {"size": self.size, "counts": self.counts}
        return cocomask.decode(d)

    def rle_uncompressed(self) -> Dict[str, Any]:
        # https://www.kaggle.com/code/stainsby/fast-tested-rle/notebook
        pixels = self.binary_mask.flatten()
        pixels = np.concatenate([[0], pixels, [0]])
        runs = np.where(pixels[1:] != pixels[:-1])[0] + 1
        runs[1::2] -= runs[::2]
        return {"size": self.size, "counts": runs.tolist()}


if __name__ == "__main__":
    counts = "_lm26^b09I4L4M2M3N2O1N2N2O1N101N101O0O100000O1O100N2K6L3M3N2N2O2N1O3L5L3N2M`bb5"
    size = [600, 500]
    rle = RLE(size=size, counts=counts)
    print(rle.decode())
    print(rle.rle_uncompressed())
    print(rle.bbox)
    print(rle.centroid)
    print(rle.contour)
    print(rle.binary_mask)
