# image-morphing

[![Build Status](https://travis-ci.com/avojak/image-morphing.svg?token=7woVhJy8YaHrvHwYkFnY&branch=master)](https://travis-ci.com/avojak/image-morphing)

Implementation of image morphing with a web front-end. Images are uploaded, 
and the user selects corresponding points in the two images.

![Input Home Page](examples/inputs.png)

![Results Page](examples/outputs.png)

This was created for the CS 445 Spring 2020 Final Project at the University of Illinois at Urbana-Champaign.
There are plenty of things that could be better but it works, and again this was for a school project!

## Building

```bash
$ pip install -r requirements.txt
$ make all
```

Note that imagemagick is also required.

## Running

A Docker image is produced and can be run with the following command:

```bash
$ docker run -it -p 8080:8080 avojak/image-morphing:{version}
```

The UI will be available at [http://localhost:8080/morph](http://localhost:8080/morph).

## Example Results

![Sample Morph](examples/morph.gif)

## Test Server

To run locally without needing to build the Docker image:

```bash
$ export FLASK_APP=webmorphing; flask run 
```

The UI will be available at [http://localhost:5000/morph](http://localhost:5000/morph).

## Technologies Used

* [OpenCV](https://pypi.org/project/opencv-python/) - Image IO, computing affine transformations
* [Scipy](https://pypi.org/project/scipy/) - Computing Delaunay triangulations
* [Matplotlib](https://pypi.org/project/matplotlib/) - Creating plots
* [Flask](https://pypi.org/project/Flask/) - Web server
* [Bootstrap](https://getbootstrap.com) - Making a half-decent looking UI
* [Docker](https://www.docker.com) - Portable distribution

## Attribution

Cat photo used in the example GIF by [Matthew Kerslake](https://unsplash.com/@mattkerslake?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/cat?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).