import json
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
import cv2
from pycocotools.coco import COCO
from PIL import Image
import matplotlib.patches as patches
import os
import sys

def bbox_visualize(json_path, img_dir, img_filename):
    """
    visualize the bbox stated in the input json file around an object
    on the input image
    
    Args:
    -----
    json_path: str
        the path to the json file where the bbox coordinates are mentioned. The json needs to be in COCO style
    img_dir: str
        the path to the directory that contains the image of interest
    img_filename: str
        filename of the image of interest 
    """
    with open(json_path, "r") as f:
        annotations = json.load(f)
    images = annotations["images"]
    img_index = next((index for index, image in enumerate(images) if image["file_name"] == img_filename), None)
    ann = annotations["annotations"]
    ann_index = next((ann_index for ann_index, annotation in enumerate(ann) if
                      annotation["image_id"] == annotations["images"][img_index]["id"]), None)

    image_name = annotations['images'][img_index]["file_name"]
    image = cv2.imread(os.path.join(img_dir, img_filename))

    box = annotations["annotations"][ann_index]["bbox"]
    cv2.rectangle(image, (box[0], box[1]), ((box[0] + box[2]), (box[1] + box[3])), (0, 255, 0), 2)

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # as opencv loads in BGR format by default, we want to show it in RGB.
    plt.show()
