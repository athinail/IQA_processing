import json
import argparse
import funcy

from os import listdir
from os.path import isfile, join

def save_coco(file, info, licenses, images, annotations, categories):
    with open(file, 'wt', encoding='UTF-8') as coco:
        json.dump({ 'info': info, 'licenses': licenses, 'images': images, 
            'annotations': annotations, 'categories': categories}, coco, indent=2, sort_keys=True)

def filter_annotations(annotations, images):
    image_ids = funcy.lmap(lambda i: i['id'], images)
    return funcy.lfilter(lambda a: a['image_id'] in image_ids, annotations)


def filter_images(images, annotations):
    annotation_ids = funcy.lmap(lambda i: i['image_id'], annotations)
    return funcy.lfilter(lambda a: a['id'] in annotation_ids, images)

# This script makes a list of image names that are found in image_dir,
# then scans the infile json for annotations matching to those images,
# then outputs a new json which a "valid" subset of infile.

# image_dir = 'raw/'
# infile = 'merged_all_fixed_resize_cropped.json'
# outfile = 'outfile.json'

parser = argparse.ArgumentParser(description='Creates a subset of json file annotations that match images file in a directory.')
parser.add_argument('infile', type=str, help='Path to the input COCO annotations file.')
parser.add_argument('outfile', type=str, help='Where to store the subset of COCO annotations')
parser.add_argument('image_dir', type=str, help='Where to check for images')
args = parser.parse_args()

def main(args):

	image_file_list = [f for f in listdir(args.image_dir) if isfile(join(args.image_dir, f))]

	cocofile = open(args.infile, 'rt', encoding='UTF-8')

	# set up metadata arguments for coco
	coco = json.load(cocofile)
	info = None
	licences = None
	images = coco['images']
	annotations = coco['annotations']
	categories = coco['categories']

	print('reference to images found in infile:\t', len(images))

	images_with_annotations = funcy.lmap(lambda a: a['image_id'], annotations)
	images = funcy.lremove(lambda i: i['id'] not in images_with_annotations, images)
	print('subset of infile with annotations:\t', len(images))

	images_in_dir = funcy.lremove(lambda i: i['file_name'] not in image_file_list, images)
	print('subset of infile with images in dir:\t', len(images_in_dir))

	annotations_in_dir = filter_annotations(annotations, images_in_dir)
	print('selecting', len(annotations_in_dir), 'from', len(annotations), 'annotations')

	save_coco(args.outfile, info, licences, images_in_dir, annotations_in_dir, categories)
	print('saved subset as', args.outfile)

if __name__ == "__main__":
	main(args)
