# usage
The python script select_json_instances can be used to filter instances in an _input_ coco .json file based on available images in an _image directory_ and stores this subset as an _output_ coco .json file. Example usage:

    $ python select_jscon_instances.py input.json output.json path_to_images_dir/

Then, coco .json files can be merged using the utility pyodi. From `https://gradiant.github.io/pyodi/install/` we install this utility using:

    $ pip install pyodi

Then we use this utility to merge two coco .jsons as follows:

    $ pyodi coco merge first.json second.json output.json

# results
This process was applied using `instances_train_trashcan.json` and `instances_val_trashcan.json` from the original trashcan dataset, and `merged_all_fixed_resize_cropped.json` from the Seaclear webdrive environment.

For the IQA dataset this resulted in the coco .json file `IQA_Dataset_original_dimensions.json`, with annotations for 1199 images (one selected Trashcan training image has no annotations). 

# further processing
This output .json file can be further processed to have the dimensions and coordinates of the annotations match the file size as found in the directory.
In addition, the annotations from different sources in this .json do not necessarily match well with each other. Other .json processing utilities can be used to downpool the annotated classes by merging them.

# dimension updated
Using the python script `check_resize_annotations.py` I looped over all the annotations from `IQA_Dataset_original_dimensions.json` and updated the width, height, bbox, and segmentation fields with correct width and height scaling to make sure the coordinate system in the coco .jscon file matches with the dimensions of the files as present in the image directory. This output json is also uploaded as `IQA_Dataset_matched_dimensions.json`. Example usage:

    $ python check_resize_annotations.py input.json output.json path_to_images_dir/ [--debug]
    > 0 annotations had correct dimensions and 3537 annotations were changed
    > saved updated file as output.json

# classes
By combining these images from different datasets, there exists overlap in the `coco['categories']` in the combined coco json. Therefore, as a final step, we use Antun's script to downpool the 57 categories, merging those that are similar and/or identical.

    rov
    plant
    animal_fish
    animal_starfish
    animal_shells
    animal_crab
    animal_eel
    animal_etc
    trash_clothing
    trash_pipe
    trash_bottle
    trash_bag
    trash_snack_wrapper
    trash_can
    trash_cup
    trash_container
    trash_unknown_instance
    trash_branch
    trash_wreckage
    trash_tarp
    trash_rope
    trash_net
    can_metal
    tarp_plastic
    container_plastic
    bottle_plastic
    tube_cement
    container_middle_size_metal
    animal_sponge
    bottle_glass
    wreckage_metal
    unknown_instance
    pipe_plastic
    net_plastic
    rope_fiber
    animal_urchin
    cup_plastic
    brick_clay
    bag_plastic
    sanitaries_plastic
    clothing_fiber
    cup_ceramic
    boot_rubber
    tire_rubber
    jar_glass
    rov_cable
    rov_tortuga
    branch_wood
    furniture_wood
    snack_wrapper_plastic
    lid_plastic
    cardboard_paper
    rope_plastic
    cable_metal
    snack_wrapper_paper
    rov_vehicle_leg
    rov_bluerov

specifically for the yolo pretrained network, we're looking for the categories: `animal`,`plant`,`rov`,`trash`. Double checking that the categories in the output json file exactly match the entries and ordering of the yolo implementation, we now have `IQA_four_classes.json`. This file should, after conversion, be compatible with the yolo implementation.
