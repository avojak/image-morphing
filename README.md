# image-morphing

Implementation of image morphing with a web front-end. Images are uploaded, 
and the user selects corresponding points in the two images.

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

The UI will be available at [localhost:8080/morph](localhost:8080/morph).

## Example Results

![Sample Morph](examples/morph.gif)

## Test Server

To run locally without needing to build the Docker image:

```bash
$ export FLASK_APP=webmorphing; flask run 
```

## Attribution

Cat photo used in the example GIF by [Matthew Kerslake](https://unsplash.com/@mattkerslake?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/cat?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).