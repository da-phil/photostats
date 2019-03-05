#!/usr/bin/env python3
"""
Showing statistics about photos by evaluating EXIF tags.
Based on program by Jason Millward

Usage:
    photostats.py [--exif-tags=[tag1, tag2, ...]] [--dir=<dir>]

"""

import sys
import os
import exifread
import unicodedata
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import argparse


photo_dir_default = "."
exif_tags_default = ["FocalLength", "ISOSpeedRatings", "ExposureTime", "LensModel"]
image_file_extensions = ["jpg", "jpeg", "png"]




def findimages(dirname):
    result = []
    dirname = dirname.encode('utf-8', 'surrogateescape').decode('utf-8')
    if not os.path.isdir(dirname):
        print("Folder '{}'' doesn't exist!".format(dirname))
        return []

    # recursively find files within dirname
    for root, dirs, files in os.walk(dirname):
        path = root.split(os.sep)
        for file in files:
            try:
                file = file.encode('utf-8', 'surrogateescape').decode('utf-8')
                file_extension = os.path.splitext(file)[1].replace(".", "").lower()
                if file_extension in image_file_extensions:
                    full_filename = "/".join(path)+os.sep+file
                    if os.path.isfile(full_filename):
                        result.append(full_filename)
            except Exception as e:
                print("Problem with file '{}'".format(file))
                print("Exception: ", str(e))
                continue

    return result


def returnattribute(image, attribute):
    try:
        f = open(image, "rb")
    except Exception as e:
        print("Problem with file '{}': {}".format(image, str(e)))
        return none

    exif_attribute = "EXIF {:s}".format(attribute)
    try:
        tags = exifread.process_file(f, details=False)
        #print("tags[exif_attribute]: ", tags[exif_attribute], ", type: ", type(tags[exif_attribute]))
        result = str(tags[exif_attribute])
    except KeyError:
        #print("Couldn't find attribute '{}' in {}".format(exif_attribute, image))
        result = None
    except Exception as e:
        print("Problem with attribute '{}': {}".format(exif_attribute, str(e)))
        result = None
    return result


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def autolabel(rects, ax):
    for rect in rects:
        x = rect.get_x() + rect.get_width()/2.
        y = rect.get_height()
        ax.annotate("{}".format(y), (x,y), xytext=(0,5),
                    textcoords="offset points", ha='center', va='bottom')

def parseresults(imageresults):
    max_width = 200
    attributes = list(imageresults.keys())
    for attr in attributes:
        results = imageresults[attr]
        sorted_results = dict(sorted(results.items()))
        keys   = list(sorted_results.keys())
        values = list(sorted_results.values())
        key_min, key_max = keys[0], keys[-1]
        value_max = max(values)

        attr_str = "== {} ==".format(attr)
        print("=" * len(attr_str))
        print(attr_str)
        print("=" * len(attr_str))
        for k in keys:
            count = "+" * results[k] # (results[k] // value_max) * max_width
            print("  {:12s} ({:5d} counts): {}".format(k, results[k], count))
        print("")


        # have a linear axis with all gathered EXIF values 
        tick_positions = [int(i) for i in range(len(keys))]
        bins = tick_positions
        if attr == "ISOSpeedRatings":
            allowed_ticks = np.array([25, 50, 64, 80, 100, 125, 160,  200, 250, 320, 400, 500, 640,
                                      800, 1000, 1250, 1600, 2000, 2500, 3200, 4000, 5000, 6400])
            # filter histogram according to allowed tick values
            filtered_results = {}
            for k, v in sorted_results.items():
                if int(k) in allowed_ticks:
                    filtered_results[int(k)] = sorted_results[k]

            filtered_results_ordered = dict(sorted(filtered_results.items()))
            print(filtered_results_ordered)
            tick_names = list(filtered_results_ordered.keys())
            tick_positions = [int(i) for i in range(len(tick_names))]
            bins = tick_positions
            hist  = list(filtered_results.values())
            # have logarithmic scale on x/y axis?
            #plt.gca().set_yscale("log")
        elif attr in  ["FocalLength", "ExposureTime"]:
            str_float_mapping = {k: eval(k) for k, v in results.items()}
            sorted_float = dict(sorted(str_float_mapping.items(), key=lambda x: x[1]))
            sorted_str = {k: results[k] for k, v in sorted_float.items()}
            tick_names = sorted_str.keys()
            hist = sorted_str.values()
        #elif attr in ["FocalLength", "FNumber", "ExposureTime", "LensModel"]:
        else:
            tick_names = keys
            hist = values

        plot_results(bins, hist, tick_positions, tick_names, attr, save=True)

    plt.show()

def plot_results(bins, hist, tick_positions, tick_names, attribute, save=False):
    axis_label_props_dict = {'fontsize': 15, 'fontweight': 'bold'}
    title_props_dict = {'fontsize': 18, 'fontweight': 'bold'}
    
    plt.figure()
    plt.title("{} statistics".format(attribute), **title_props_dict)
    plt.ylabel("photo count", **axis_label_props_dict)
    plt.xlabel(attribute, **axis_label_props_dict)    

    rects = plt.bar(bins, hist, align="center")
    autolabel(rects, plt.gca())
    plt.grid(alpha=0.2)

    # don't show minor ticks on x axis
    plt.gca().tick_params(axis="x", which="minor", bottom=False)
    plt.xticks(tick_positions, tick_names, rotation=70)
    plt.tight_layout();
    if save:
        plt.savefig("./{}.png".format(attribute))
    #plt.show()


def statistics(args):
    imageresults = {}
    directory = args.dir
    attributes = args.exif_tags
    print(attributes)
    images = findimages(directory)
    image_count = len(images)
    print("Found {} images for statistics.".format(image_count))
    for f in images:
        if not image_count % 1000:
            print("{} images left for processing".format(image_count))

        for attr in attributes:
            val = returnattribute(os.path.join(directory, f), attr)
            if val is not None:
                if attr in imageresults:
                    if val in imageresults[attr]:
                        imageresults[attr][val] += 1
                    else:
                        imageresults[attr][val] = 1
                else:
                    imageresults[attr] = {val: 1}

        image_count -= 1

    parseresults(imageresults)




if __name__ == '__main__':
    print("\nPython " + sys.version)
    parser = argparse.ArgumentParser(description="Photostatistics based on EXIF tags")
    parser.add_argument("-d", "--dir", help="Photo directory to browse, default: {}".format(photo_dir_default),
                        type=str, metavar="", default=photo_dir_default)
    parser.add_argument("-e", "--exif-tags", help="EXIF tags to consider, default: {}".format(exif_tags_default),
                        type=str, metavar="", nargs="+", default=exif_tags_default)
    args = parser.parse_args()

    # convert default path and relative paths to absolute paths
    if not args.dir.startswith("/"):
        args.dir = os.getcwd() + os.sep + args.dir
    
    statistics(args)