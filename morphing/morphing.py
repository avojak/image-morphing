#!/usr/bin/env python3

import logging
import numpy as np
import matplotlib.pyplot as plt

from cv2 import cv2
from scipy.spatial import Delaunay


class ImageMorph:

    def __init__(self, source_img_path: str, target_img_path: str, source_points: list, target_points: list) -> None:
        """
        Create an animated GIF which morphs the source image into the target image.

        Args:
          - source_img_path: The path to the source image.
          - target_img_path: The path to the target image.
          - source_points: The list of points selected in the source image which
            correspond to points in the target image.
          - target_points: The list of points selected in the target image which
            correspond to points in the source image.
        """
        self.source_img = cv2.imread(source_img_path)
        self.target_img = cv2.imread(target_img_path)

        assert len(source_points) == len(target_points)
        self.source_points = source_points.copy()
        self.target_points = target_points.copy()

        assert self.source_img.shape == self.target_img.shape

        self.H, self.W, self.C = self.source_img.shape

        # Add the points at the corners of the images
        self.source_points.extend([[0, 0], [0, self.W - 1], [self.H - 1, 0], [self.H - 1, self.W - 1]])
        self.target_points.extend([[0, 0], [0, self.W - 1], [self.H - 1, 0], [self.H - 1, self.W - 1]])

        self._morph()

    def _morph(self):
        self._create_mapping_img()
        triangulation = Delaunay(self.source_points)

    def _create_mapping_img(self):
        # Display the connected points to verify
        mapping_img = np.zeros(shape=(2 * self.H, 2 * self.W, self.C), dtype='uint16')
        for h in range(0, self.H):
            for w in range(0, self.W):
                for c in range(0, self.C):
                    mapping_img[h][w][c] = self.source_img[h][w][c]
                    mapping_img[h + self.H][w + self.W][c] = self.target_img[h][w][c]

        fig = plt.figure()
        plt.axis('off')
        plt.imshow(cv2.cvtColor(mapping_img, cv2.COLOR_BGR2RGB))

        for p in range(0, len(self.source_points)):
            x1 = self.source_points[p][0]
            y1 = self.source_points[p][1]
            x2 = self.target_points[p][0] + self.W
            y2 = self.target_points[p][1] + self.H
            plt.plot([x1, x2], [y1, y2], marker='+')

        fig_path = './images/outputs/mapping.png'
        plt.savefig(fig_path, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, metadata=None)
