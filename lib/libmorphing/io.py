import glob
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

from cv2 import cv2
from scipy.spatial import Voronoi
from subprocess import Popen, PIPE

# Allows headless plotting
matplotlib.use("Agg")


def write_mapping_img(source_img, target_img, source_points, target_points, filename):
    assert source_img.shape == target_img.shape
    H, W, C = source_img.shape

    # Display the connected points to verify
    mapping_img = np.zeros(shape=(2 * H, 2 * W, C), dtype='uint16')
    for h in range(0, H):
        for w in range(0, W):
            for c in range(0, C):
                mapping_img[h][w][c] = source_img[h][w][c]
                mapping_img[h + H][w + W][c] = target_img[h][w][c]

    fig = plt.figure()
    plt.axis('off')
    plt.imshow(cv2.cvtColor(mapping_img, cv2.COLOR_BGR2RGB))

    for p in range(0, len(source_points)):
        x1 = source_points[p][0]
        y1 = source_points[p][1]
        x2 = target_points[p][0] + W
        y2 = target_points[p][1] + H
        plt.plot([x1, x2], [y1, y2], marker='+')

    plt.savefig(filename, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                format=None, transparent=False, bbox_inches='tight', pad_inches=0, metadata=None)


def write_triangulation_img(triangulation, img, points, filename):
    fig = plt.figure()
    v = Voronoi(points)
    plt.axis('off')
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.triplot(points[:, 0], points[:, 1], triangulation.simplices.copy(), c='#FF0000')
    plt.plot(points[:, 0], points[:, 1], 'r+')

    plt.savefig(filename, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                format=None, transparent=False, bbox_inches='tight', pad_inches=0, metadata=None)


def write_frame(frame, frame_number, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, 'frame_{}.png'.format(str(frame_number)))
    cv2.imwrite(filename, frame)


def write_gif(frame_dir, filename, fps):
    """
    Creates an animated GIF from the frame files using ImageMagick.
    """
    frames = glob.glob('{}/*.png'.format(frame_dir))
    list.sort(frames, key=lambda x: int(x.split('_')[-1].split('.png')[0]))
    with open('{}/frame_list.txt'.format(frame_dir), 'w') as f:
        for frame in frames:
            f.write('{}\n'.format(frame))
    process = Popen(['convert', '-delay', str(int(100/fps)), '@{}/frame_list.txt'.format(frame_dir), filename],
                    stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(stderr.decode('utf-8'))
