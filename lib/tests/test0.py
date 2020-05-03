try:
    from libmorphing.morphing import ImageMorph
except ImportError:
    from lib.libmorphing.morphing import ImageMorph

from pathlib import Path
import shutil


def test_1():
    output_dir = './tests/outputs/test_1/'
    output_dir_path = Path(output_dir)
    if output_dir_path.exists() and output_dir_path.is_dir():
        shutil.rmtree(output_dir_path)

    source_img_path = str(Path('./tests/images/andrew.jpg').resolve())
    target_img_path = str(Path('./tests/images/cat.jpg').resolve())
    source_points = [[167.0, 227.0], [287.0, 227.0], [86.0, 213.0], [368.0, 222.0], [182.0, 372.0], [271.0, 372.0],
                     [233.0, 306.0], [240.0, 8.0], [227.0, 458.0]]
    target_points = [[162.0, 209.0], [305.0, 209.0], [28.0, 15.0], [450.0, 18.0], [198.0, 346.0], [270.0, 345.0],
                     [238.0, 293.0], [233.0, 59.0], [237.0, 382.0]]
    ImageMorph(source_img_path, None, target_img_path, source_points, None, target_points, output_dir, gif_duration=3,
               gif_fps=10)
