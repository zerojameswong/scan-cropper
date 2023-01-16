# scan-cropper
## What it does
This is a simple solution to remove white borders in scans of physical images. There can be much more complete solutions for more general cases but this was sufficient for my use case at the time and quick to implement
## Limitations
* The physical image must be relatively straight in the scan such that the edges of the physical image are parallel to the edges of the scan. This minimises the possibility of white triangles being present after cropping
* White physical images present a difficulty for differentiating the bounadries of the physical image and the white borders around it. Tweaking the threshold value can help with this to some extent
## How to use
Call the `crop_and_save` function with the source directory, destination directory for processed images, cropping function and threshold
```python
crop_and_save(source_path, destination_path, cropping_function, threshold)
```
### Cropping function
Determines which edges of the scan to crop the image from
Gets passed orientation, shape and the source file so you can define which directions in a custom function. For example, if you know that the the white borders will always be on the left if portrait or on the bottom if landscape you can define such a funcrtion for more fine grained control

The most general function is defined below and simply includes all of the possible edges
```python
def crop_from_general(orientation, shape, src):
    return [Edge.TOP, Edge.BOTTOM, Edge.LEFT, Edge.RIGHT]
```
### Threshold
The threshold is used to determine exactly where to crop by comparing the color of each row or column of the image, 255 being the most white and 0 being the least
