# image with metadata needed for yolo training
# all coordinates are normalized with 0,0 being the top left corner and 1,1 being the bottom right corner
# class_index is the index of the class in the yolo config file
# tracker_x, tracker_y, tracker_width, tracker_height are the bounding box of the tracker
# xxx_led_x, xxx_led_y are coordinates of the led in frame coordinates
# xxx_led_visible is a flag indicating if the led is visible an/orlabeled:
# 0 - not visible
# 1 - visible but not labeled
# 2 - visible and labeled

sensor_msgs/Image image

int32 class_index
float64 tracker_x
float64 tracker_y

float64 tracker_width
float64 tracker_height

float64 red_led_x
float64 red_led_y
float64 red_led_visible

float64 green_led_x
float64 green_led_y
float64 green_led_visible

float64 blue_led_x
float64 blue_led_y
float64 blue_led_visible
