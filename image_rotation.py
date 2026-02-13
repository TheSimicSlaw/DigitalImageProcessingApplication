from dip_imports import *
import math

def rotate(image, angle, type):
  angle = float(angle)
  print("rotating")
  inv_trans_mat = array([[math.cos(angle), math.sin(angle)], 
                         [-math.sin(angle), math.cos(angle)]])
  img_size = image.shape
  transf_corners = [array([0, 0], dtype=int) for _ in range(4)]
  transf_corners[1] = (inv_trans_mat @ array([0, img_size[1]])).astype(int)
  transf_corners[2] = (inv_trans_mat @ array([img_size[0], img_size[1]])).astype(int)
  transf_corners[3] = (inv_trans_mat @ array([img_size[0], 0])).astype(int)

  new_corners = [array([0, 0], dtype=int) for _ in range(2)]
  new_corners[0] = [
    int(min([tc[0] for tc in transf_corners])),
    int(min([tc[1] for tc in transf_corners]))
  ]
  new_corners[1] = [
    int(max([tc[0] for tc in transf_corners])),
    int(max([tc[1] for tc in transf_corners]))
  ]
  new_img_size = [0,0]
  new_img_size[0] = new_corners[1][0]-new_corners[0][0]
  new_img_size[1] = new_corners[1][1]-new_corners[0][1]

  origin = [-new_corners[0][1], -new_corners[0][0]]
  
  rotated_image = zeros(new_img_size, uint8)

  if type == "nearest_neighbor":
    for i in range(0, new_img_size[0]):
      for j in range(0, new_img_size[1]):
        i_prime, j_prime = int(i - origin[0]), int(j - origin[1])
        location = inv_trans_mat @ array([i_prime, j_prime])
        nearest_x, nearest_y = int(round(location[0], 0)), int(round(location[1], 0))
        if(nearest_x>=0 and nearest_y>=0 and nearest_x<img_size[0] and nearest_y<img_size[1]):
          rotated_image[i, j] = image[nearest_x, nearest_y]
  elif type == "bilinear":
    for i in range(0, new_img_size[0]):
      for j in range(0, new_img_size[1]):
        i_prime, j_prime = int(i - origin[0]), int(j - origin[1])
        location = inv_trans_mat @ array([i_prime, j_prime])
        if(math.floor(location[0])>=0 and math.floor(location[1])>=0 and math.ceil(location[0])<img_size[0] and math.ceil(location[1])<img_size[1]):
          rotated_image[i, j] = uint8(round(bilinear_interpolation(math.floor(location[0]), math.ceil(location[0]), math.floor(location[1]), math.ceil(location[1]), location[0], location[1], 
                                                              image[math.floor(location[0])][math.floor(location[1])], image[math.ceil(location[0])][math.floor(location[1])], 
                                                              image[math.floor(location[0])][math.ceil(location[1])], image[math.ceil(location[0])][math.ceil(location[1])]), 0))

  return rotated_image

def linear_interpolation(Pt1, Pt2, location_x, int1, int2): # used for bilinear interpolation
    if Pt1 == Pt2:
      return int1

    slope = (int2 - int1) / (Pt2 - Pt1)
    interpolated_value = int1 + slope * (location_x - Pt1)
    return interpolated_value

def bilinear_interpolation(Pt1_x, Pt2_x, Pt1_y, Pt2_y, location_x, location_y, int1, int2, int3, int4):
  interpolation_1 = linear_interpolation(Pt1_x, Pt2_x, float(location_x), float(int1), float(int2))
  interpolation_2 = linear_interpolation(Pt1_x, Pt2_x, float(location_x), float(int3), float(int4))
  interpolation_3 = linear_interpolation(Pt1_y, Pt2_y, float(location_y), float(interpolation_1), float(interpolation_2))
  return interpolation_3
  
