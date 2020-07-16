import xml.etree.cElementTree as ET
import os
import json
import argparse
import glob
import sys
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default='.', help="Location of Jsons to read")
parser.add_argument("-s", "--supervisely", type=str, help="Location of Supervisely folder")
parser.add_argument("-o", "--output", type=str, default='.', help="Location of XMLs to  write")
parser.add_argument('-p', "--pretend", default=False, action='store_true', help="Pretend to be VOC2012")
parser.add_argument("-r", "--overwrite", default=False, action='store_true',
                    help="Overwrite the output dir if it exists")
args = parser.parse_args()


##
# Create fake VOC2012 file structure
# location: location of the root folder
def create_voc(location):
    # Check if we can overwrite the folder
    if os.path.exists(os.path.join(location, "voc2012_raw")):
        if args.overwrite:
            shutil.rmtree(os.path.join(location, "voc2012_raw"), ignore_errors=True)
        else:
            sys.exit("Folder already exists: {}".format(os.path.join(location, "voc2012_raw")))
    # Create the folders
    os.makedirs(os.path.join(location, "voc2012_raw/VOCdevkit/VOC2012/Annotations"))
    os.makedirs(os.path.join(location, "voc2012_raw/VOCdevkit/VOC2012/JPEGImages"))
    os.makedirs(os.path.join(location, "voc2012_raw/VOCdevkit/VOC2012/ImageSets/Main"))


##
# Writes an XML given prams
# cords: A list of lists containing points - [["name", x, y, x1, y1], ["name2", x, y, x1, y1]]
# width: the width of the image
# height: the height of the image
# depth: color depth of the image. For RGB this should be 3
# filename: file of the xml to write
# folder: folder to write the xml to
# difficult: the difficultly to see the image. This should be set to 0
# truncated: see VOC docs. Should be set to 0
# pose: see VOC docs. Should be set to Unspecified
def write_xml(cords, width, height, depth, filename, folder, difficult, truncated, pose):
    # Make the names right
    if folder[-1] != '/':
        folder_out_name = folder
        folder = folder + '/'
    else:
        folder_out_name = folder[:-1]
    filename = filename[:-5]

    annotation = ET.Element("annotation")

    # folder
    if args.pretend:
        ET.SubElement(annotation, "folder").text = "VOC2012"
    else:
        ET.SubElement(annotation, "folder").text = str(folder_out_name)

    # filename
    ET.SubElement(annotation, "filename").text = str(filename)

    # size block
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)

    # object block
    for point in cords:
        object = ET.SubElement(annotation, "object")
        ET.SubElement(object, "name").text = point[0]
        ET.SubElement(object, "pose").text = pose
        ET.SubElement(object, "truncated").text = str(truncated)
        ET.SubElement(object, "difficult").text = str(difficult)
        bndbox = ET.SubElement(object, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(point[1])
        ET.SubElement(bndbox, "ymin").text = str(point[2])
        ET.SubElement(bndbox, "xmax").text = str(point[3])
        ET.SubElement(bndbox, "ymax").text = str(point[4])
        write_to_main(point[0] + ".txt", filename[:-4] + " -1\n")
    # Write to a file
    print("Writing: {}{}.xml".format(folder, filename[:-4]))
    tree = ET.ElementTree(annotation)
    tree.write(folder + filename[:-4] + ".xml")


##
# Convert Json to XML
# folder_in: folder that contains the json
# file_in: name of json file
# folder_out: folder to write the XML to
def convert_to_xml(folder_in, file_in, folder_out):
    with open(folder_in + file_in) as f:
        data = json.load(f)
        # find the cords
        if data['objects'] is not None:
            # List of points
            cords = []
            # Go over every object
            for i in range(len(data['objects'])):
                # Example point: ["name", x, y, x1, y1]
                point = [data['objects'][i]["classTitle"]]
                j = 0
                # Make a point
                while j < 2:
                    k = 0
                    while k < 2:
                        point.append(data['objects'][i]['points']['exterior'][j][k])
                        k = k + 1
                    j = j + 1
                cords.append(point)
        else:
            print('There was nothing in objects for: ' + file_in)

        # Get width and height
        width = data['size']['width']
        height = data['size']['height']

        # Write it to XML
        write_xml(cords, width, height, 3, file_in, folder_out, 0, 0, "Unspecified")


##
# Converts a whole folder from json into XML
# input: folder containing the jsons
# output: folder to write the XMLs
def convert_files(input, output):
    # Convert all of the jsons
    for file in os.listdir(input):
        convert_to_xml(input, file, output)


##
# Gets the location of the jsons that need to be read
# Return: list of folders to read
def get_location_of_jsons():
    if args.supervisely is not None:
        print(glob.glob(args.supervisely + "/**/ann/"))
        return glob.glob(args.supervisely + "/**/ann/")
    else:
        return [args.input]


##
# Copy images from supervisely to file
# super: location of the root supervisely folder
# dest folder to write images to
def copy_files_from_supervisely(super, dest):
    for src in glob.glob(super + "/**/img/"):
        for file in os.listdir(src):
            shutil.copyfile(os.path.join(src, file), os.path.join(dest, file))


##
# write append to file or make file in ImageSets/Main
# file: the file to write to in Main
# value: the value to append to the file
def write_to_main(file, value):
    writer = open(os.path.join(args.output, "voc2012_raw/VOCdevkit/VOC2012/ImageSets/Main", file), "a")
    writer.write(value)
    writer.close()


##
# Clears dir if flag is set
# location: dir to clear
def clear_dir(location):
    # Check to see if we can overwrite the file
    if os.path.exists(location):
        if args.overwrite:
            shutil.rmtree(location, ignore_errors=True)
        else:
            sys.exit("Folder already exists: {}".format(location))
    os.makedirs(location)


if __name__ == "__main__":
    if args.pretend:
        create_voc(args.output)
        for location in get_location_of_jsons():
            print(location)
            convert_files(location, os.path.join(args.output, "voc2012_raw/VOCdevkit/VOC2012/Annotations/"))
        copy_files_from_supervisely(args.supervisely,
                                    os.path.join(args.output, "voc2012_raw/VOCdevkit/VOC2012/JPEGImages/"))
    else:
        if args.output != ".":
            clear_dir(args.output)
        convert_files(get_location_of_jsons()[0], args.output)
