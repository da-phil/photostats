# Photography Statistics

Python library to extract statistics from JPG EXIF tags and show it as a histogram both on the commandline as well as matplotlib histogram plots.

Credit goes to Jason Millwards
[photography-statistics](https://github.com/JasonMillward/photography-statistics)
for providing a good foundation and inspiration for this script.

The script works for the following EXIF tags:
* FocalLength
* ISOSpeedRatings
* ExposureTime
* LensModel

It has been tested on my entire image folder which contains approx. 125 000 pictures.


### Installation

Requirements

* python 3
* matplotlib
* exifread


### Usage

```photostats.py [--exif-tags tag1 [tag2 tag3 ...]] [--dir <dir>] ```

### Results

```
$ python stats.py --exif-tags FNumber FocalLength ExposureTime ISOSpeedRatings --dir ./images/

Found 134 images for statistics.
=============
== FNumber ==
=============
  11/5         (   20 counts): ++++++++++++++++++++
  14/5         (    2 counts): ++
  16/5         (    2 counts): ++
  31/10        (    1 counts): +
  4            (    1 counts): +
  7/2          (    1 counts): +
  8            (  100 counts): ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  9/2          (    6 counts): ++++++

=================
== FocalLength ==
=================
  101          (    1 counts): +
  108          (    1 counts): +
  12           (   48 counts): ++++++++++++++++++++++++++++++++++++++++++++++++
  147          (    2 counts): ++
  15           (    3 counts): +++
  17           (    4 counts): ++++
  18           (    2 counts): ++
  19           (    7 counts): +++++++
  200          (   17 counts): +++++++++++++++++
  21           (    7 counts): +++++++
  23           (    2 counts): ++
  24           (    2 counts): ++
  25           (    1 counts): +
  30           (    1 counts): +
  36           (    1 counts): +
  40           (   10 counts): ++++++++++
  47/10        (    2 counts): ++
  473/100      (   18 counts): ++++++++++++++++++
  50           (    1 counts): +
  83           (    1 counts): +
  92           (    2 counts): ++

==================
== ExposureTime ==
==================
  1/10         (    3 counts): +++
  1/100        (    7 counts): +++++++
  1/1000       (    3 counts): +++
  1/125        (    7 counts): +++++++
  1/1250       (    2 counts): ++
  1/13         (    1 counts): +
  1/15         (    1 counts): +
  1/160        (    4 counts): ++++
  1/2          (    3 counts): +++
  1/20         (    1 counts): +
  1/200        (    2 counts): ++
  1/2000       (    3 counts): +++
  1/240        (    1 counts): +
  1/25         (    3 counts): +++
  1/250        (    6 counts): ++++++
  1/3          (    3 counts): +++
  1/30         (    7 counts): +++++++
  1/320        (    9 counts): +++++++++
  1/4          (    3 counts): +++
  1/40         (    5 counts): +++++
  1/400        (   17 counts): +++++++++++++++++
  1/5          (    1 counts): +
  1/50         (    3 counts): +++
  1/500        (    7 counts): +++++++
  1/6          (    2 counts): ++
  1/60         (    7 counts): +++++++
  1/640        (    5 counts): +++++
  1/8          (    1 counts): +
  1/80         (    6 counts): ++++++
  1/800        (    2 counts): ++
  5/8          (    7 counts): +++++++
  781/500000   (    1 counts): +

=====================
== ISOSpeedRatings ==
=====================
  100          (   20 counts): ++++++++++++++++++++
  200          (  113 counts): +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

```
