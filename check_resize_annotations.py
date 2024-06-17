import json
import argparse
import funcy

from os import listdir
from os.path import isfile, join


import cv2
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

def get_annotations(annotations, image_id):
	return funcy.lfilter(lambda a: a['image_id'] == image_id, annotations)

def get_image(images, image_id):
	return funcy.lfilter(lambda a: a['id'] == image_id, images)[0]

# image_dir = 'raw/'
# infile = 'merged_all_fixed_resize_cropped.json'
# outfile = 'outfile.json'

parser = argparse.ArgumentParser(description='Checks the annotations and dimensions of the annotations and matches it to the image file dimensions')
parser.add_argument('infile', type=str, help='Path to the input COCO annotations file.')
parser.add_argument('outfile', type=str, help='Where to store the rescaled COCO annotations')
parser.add_argument('image_dir', type=str, help='Where to check for images')
parser.add_argument("--debug", help="verbose output", nargs='?', type=int, const=1)
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

	images_with_annotations = funcy.lmap(lambda a: a['image_id'], annotations)
	images = funcy.lremove(lambda i: i['id'] not in images_with_annotations, images)
	if args.debug: 
		print('reference to images found in infile:\t', len(images))
		print('subset of infile with annotations:\t', len(images))

	images_in_dir = funcy.lremove(lambda i: i['file_name'] not in image_file_list, images)
	if args.debug: 
		print('subset of infile with images in dir:\t', len(images_in_dir))

	if len(images_in_dir) != len(images):
		print('not every image listed in infile.json is found in the image directory... stopping')
		quit()

	# print(annotations[0]) # to check whether changing by reference worked

	correct_cnt = 0
	change_cnt = 0

	for cur_anno in annotations: #this is passed as reference

		cur_img = get_image(images,cur_anno['image_id'])
		img = cv2.imread(args.image_dir+cur_img['file_name'])

		wscale = img.shape[1] / cur_img['width']
		hscale = img.shape[0] / cur_img['height'] 

		if args.debug: print('\nfile name:',cur_img['file_name'])

		if wscale != 1 or hscale != 1:

			change_cnt += 1

			if args.debug: 
				print('file dimensions: width', img.shape[1], ', height', img.shape[0])
				print('annotation dims: width', cur_img['width'],', height', cur_img['height'])

			# image ::
			#	file name
			#	id
			#	width
			#	height

			# annotation ::
			#	area
			#	bbox [x_min,y_min,width,height]
			#	category_id
			#	id
			#	image_id
			#	is_crowd
			#	segmentation

			# multiply the numbers at even indices with height scale, and even indices with width scale.
			cur_anno['bbox'] = [round(x * hscale) if i%2 else round(x * wscale) for i,x in enumerate(cur_anno['bbox'])]
			cur_anno['segmentation'] = [round(x * hscale) if i%2 else round(x * wscale) for i,x in enumerate(cur_anno['segmentation'][0])]
			cur_anno['area'] = cur_anno['area'] * hscale * wscale

		else:

			correct_cnt += 1
			if args.debug: 
				print('annotation matches file dimensions')

	# we can't change the image dims in the first loop, because then the check condition would not trigger for a 2nd or 3rd+ annotation on that same image.
	for cur_img in images:

		img = cv2.imread(args.image_dir+cur_img['file_name'])

		wscale = img.shape[1] / cur_img['width']
		hscale = img.shape[0] / cur_img['height'] 

		# this also gets changed by reference
		cur_img['width'] = int(img.shape[1])
		cur_img['height'] = int(img.shape[0])

	# check_image = get_image(images,annotations[0]['image_id'])		
	# print('changed dims: width', check_image['width'],', height', check_image['height'])
	# print(annotations[0]) # to check whether changing by reference worked

	# annotations_in_dir = filter_annotations(annotations, images_in_dir)
	# print('selecting', len(annotations_in_dir), 'from', len(annotations), 'annotations')
	print(correct_cnt, 'annotations had correct dimensions and', change_cnt, 'annotations were changed')
	save_coco(args.outfile, info, licences, images, annotations, categories)
	print('saved updated file as', args.outfile)

if __name__ == "__main__":
	main(args)
