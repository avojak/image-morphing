#!/usr/bin/env python3

try:
    import libmorphing.io as io
    import libmorphing.util as util
except ImportError:
    import lib.libmorphing.io as io
    import lib.libmorphing.util as util

import logging
import numpy as np
import os

from cv2 import cv2
from multiprocessing import Pool
from scipy.spatial import Delaunay


class ImageMorph:

    def __init__(self, source_img_path: str, target_img_path: str, source_points: list, target_points: list,
                 output_dir: str) -> None:
        """
        Create an animated GIF which morphs the source image into the target image.

        Args:
          - source_img_path: The path to the source image.
          - target_img_path: The path to the target image.
          - source_points: The list of points selected in the source image which
            correspond to points in the target image.
          - target_points: The list of points selected in the target image which
            correspond to points in the source image.
          - output_dir: The location where result images will be placed.
        """
        self.source_img = cv2.imread(source_img_path)
        self.target_img = cv2.imread(target_img_path)

        assert len(source_points) == len(target_points)
        self.source_points = source_points.copy()
        self.target_points = target_points.copy()

        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        assert self.source_img.shape == self.target_img.shape

        H, W, C = self.source_img.shape

        # Add the points at the corners of the images
        self.source_points.extend([[0, 0], [0, W - 1], [H - 1, 0], [H - 1, W - 1]])
        self.target_points.extend([[0, 0], [0, W - 1], [H - 1, 0], [H - 1, W - 1]])

        # Define the configuration
        self.pool_size = os.cpu_count()
        self.gif_duration = 3  # in seconds
        self.gif_fps = 10
        logging.info('Process pool size: {}'.format(self.pool_size))
        logging.info('GIF duration: {}'.format(self.gif_duration))
        logging.info('GIF FPS: {}'.format(self.gif_fps))
        logging.info('Source image: {} ({}x{})'.format(source_img_path, W, H))
        logging.info('Target image: {} ({}x{})'.format(target_img_path, W, H))

        self._morph()

    def _morph(self):
        """
        Performs the morphing.
        """
        logging.debug('Writing mapping image...')
        io.write_mapping_img(self.source_img, self.target_img, self.source_points, self.target_points,
                             os.path.join(self.output_dir, 'mapping.png'))
        logging.debug('Creating Delaunay triangulation...')
        triangulation = Delaunay(self.source_points)
        # From this point on, the points must be a NumPy array
        self.source_points = np.array(self.source_points)
        self.target_points = np.array(self.target_points)
        logging.debug('Writing triangulation images...')
        io.write_triangulation_img(triangulation, self.source_img, self.source_points,
                                   os.path.join(self.output_dir, 'source_triangulation.png'))
        io.write_triangulation_img(triangulation, self.target_img, self.target_points,
                                   os.path.join(self.output_dir, 'target_triangulation.png'))

        H, W, C = self.source_img.shape

        num_frames = self.gif_duration * self.gif_fps

        # TODO: Make pool size configurable?
        with Pool(processes=self.pool_size) as pool:
            results = []
            for frame_num in range(0, num_frames):
                t = frame_num / num_frames
                res = pool.apply_async(self._process_func, (triangulation, t, frame_num, (H, W, C), 'test'))
                results.append(res)

            for res in results:
                res.get(timeout=None)

            frame_dir = os.path.join(self.output_dir, 'frames')
            filename = os.path.join(self.output_dir, 'morphing.gif')
            logging.debug('Creating GIF...')
            io.write_gif(frame_dir, filename)

    def _compute_frame(self, triangulation, t, shape):
        """
        Computes a frame of the image morph.

        Args:
          - triangulation: The scipy.spatial.Delaunay triangulation.
          - t: The time value in the range [0,1]
          - shape: The shape of the frame which should match the shape of
            the original source and target images.

        Returns:
          - The frame of the morphing at time t.
        """
        frame = np.zeros(shape=shape, dtype='uint8')

        # The number of triangles is determined by the simplices attribute
        num_triangles = len(triangulation.simplices)
        average_triangles = np.zeros(shape=(num_triangles, 3, 2), dtype=np.float32)

        for triangle_index in range(0, num_triangles):
            simplices = triangulation.simplices[triangle_index]
            for v in range(0, 3):
                simplex = triangulation.simplices[triangle_index][v]
                P = self.source_points[simplex]
                Q = self.target_points[simplex]
                average_triangles[triangle_index][v] = P + t * (Q - P)

            # Compute the affine projection to the source and target triangles
            source_triangle = np.float32([
                self.source_points[simplices[0]],
                self.source_points[simplices[1]],
                self.source_points[simplices[2]]
            ])
            target_triangle = np.float32([
                self.target_points[simplices[0]],
                self.target_points[simplices[1]],
                self.target_points[simplices[2]]
            ])
            average_triangle = np.float32(average_triangles[triangle_index])
            source_transform = cv2.getAffineTransform(average_triangle, source_triangle)
            target_transform = cv2.getAffineTransform(average_triangle, target_triangle)

            average_triangulation = Delaunay(average_triangle)

            # For each point in the average triangle, find the corresponding points
            # in the source and target triangle, and find the weighted average.
            average_points = util.get_points_in_triangulation(average_triangle, average_triangulation)
            for point in average_points:
                source_point = np.transpose(np.dot(source_transform, np.transpose(np.array([point[0], point[1], 1]))))
                target_point = np.transpose(np.dot(target_transform, np.transpose(np.array([point[0], point[1], 1]))))

                # Perform a weighted average per-channel
                for c in range(0, shape[2]):
                    source_val = self.source_img[int(source_point[1]), int(source_point[0]), c]
                    target_val = self.target_img[int(target_point[1]), int(target_point[0]), c]
                    frame[point[1], point[0], c] = round((1 - t) * source_val + t * target_val)
        return frame

    def _process_func(self, triangulation, t, frame_num, shape, group_name):
        frame = self._compute_frame(triangulation, t, shape)
        io.write_frame(frame, frame_num, os.path.join(self.output_dir, 'frames'))
        logging.debug('Created frame {}'.format(str(frame_num)))
