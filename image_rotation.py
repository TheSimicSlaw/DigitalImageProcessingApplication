import math

from numpy import array, uint8, zeros

def rotate(image, angle, type):
  print(angle)
  radian_angle = round(float(angle)*math.pi/180.0, 6) # convert to radians
  print(radian_angle)
  print("rotating")
  trans_mat = array([[math.cos(radian_angle), -math.sin(radian_angle)], 
                         [math.sin(radian_angle), math.cos(radian_angle)]]) # rotation matrix, counterclockwise by angle in radians
  inv_trans_mat = array([[math.cos(radian_angle), math.sin(radian_angle)], 
                         [-math.sin(radian_angle), math.cos(radian_angle)]]) # inverse rotation matrix, clockwise by angle in radians
  img_size = image.shape
  print(f"image size: {img_size}")
  transf_corners = [array([0, 0], dtype=int) for _ in range(4)] # top left corner (OG origin)
  transf_corners[1] = (trans_mat @ array([img_size[0], 0])).astype(int) # bottom left corner
  transf_corners[2] = (trans_mat @ array([img_size[0], img_size[1]])).astype(int) # bottom right corner
  transf_corners[3] = (trans_mat @ array([0, img_size[1],])).astype(int) # top right corner
  print(f"transformed corners: {transf_corners}")

  new_corners = [array([0, 0], dtype=int) for _ in range(2)]
  new_corners[0] = [
    int(min([tc[0] for tc in transf_corners])),
    int(min([tc[1] for tc in transf_corners]))
  ]
  new_corners[1] = [
    int(max([tc[0] for tc in transf_corners])),
    int(max([tc[1] for tc in transf_corners]))
  ]
  print(f"new corners: {new_corners}")
  new_img_size = [0,0,3]
  new_img_size[0] = new_corners[1][0]-new_corners[0][0]
  new_img_size[1] = new_corners[1][1]-new_corners[0][1]
  print(f"new image size: {new_img_size}")

  # Shift output pixel coordinates so inverse mapping samples from valid source space.
  origin = [new_corners[0][0], new_corners[0][1]] 
  print(f"origin: {origin}")
  
  rotated_image = zeros(new_img_size, uint8)

  if type == "nearest_neighbor_interpolation" or type == "nearest_neighbor":
    for row in range(0, new_img_size[0]): 
      for col in range(0, new_img_size[1]):
        r_dest, c_dest = int(row + origin[0]), int(col + origin[1])
        location = inv_trans_mat @ array([r_dest, c_dest])
        nearest_row, nearest_col = int(round(location[0], 0)), int(round(location[1], 0))
        if(0 <= nearest_row < img_size[0] and 0 <= nearest_col < img_size[1]):
          rotated_image[row, col] = image[nearest_row, nearest_col] 
        if nearest_col == 0 and nearest_row == 0:
          print(f"origin: ({row}, {col})")

  elif type == "bilinear_interpolation" or type == "bilinear":
    for row in range(0, new_img_size[0]):
      for col in range(0, new_img_size[1]):
        r_dest, c_dest = int(row + origin[0]), int(col + origin[1])
        location = inv_trans_mat @ array([r_dest, c_dest])
        if(math.floor(location[0])>=0 and math.floor(location[1])>=0 and math.ceil(location[0])<img_size[0] and math.ceil(location[1])<img_size[1]):
          rotated_image[row, col] = bilinear_interpolation(math.floor(location[0]), math.ceil(location[0]), math.floor(location[1]), math.ceil(location[1]), location[0], location[1], 
                                                              image[math.floor(location[0])][math.floor(location[1])], image[math.ceil(location[0])][math.floor(location[1])], 
                                                              image[math.floor(location[0])][math.ceil(location[1])], image[math.ceil(location[0])][math.ceil(location[1])])
  else:
    raise ValueError(f"Unsupported rotate interpolation type: {type}")

  return rotated_image

def linear_interpolation(Pt1, Pt2, location_x, pixel1, pixel2): # used for bilinear interpolation
    if Pt1 == Pt2:
      return pixel1

    if pixel1.ndim == 0:
      return linear_interpolation_scalar(Pt1, Pt2, location_x, float(pixel1), float(pixel2))

    pix1 = pixel1.astype(float)
    pix2 = pixel2.astype(float)

    slope = (pix2 - pix1) / (Pt2 - Pt1)
    interpolated_value = pix1 + slope * (location_x - Pt1)
    return interpolated_value

def linear_interpolation_scalar(Pt1, Pt2, location_x, pix1, pix2): # used for bilinear interpolation
    if Pt1 == Pt2:
      return pix1

    slope = (pix2 - pix1) / (Pt2 - Pt1)
    interpolated_value = pix1 + slope * (location_x - Pt1)
    return interpolated_value

def bilinear_interpolation(Pt1_x, Pt2_x, Pt1_y, Pt2_y, location_x, location_y, pixel1, pixel2, pixel3, pixel4):

  interpolation_1 = linear_interpolation(Pt1_x, Pt2_x, float(location_x), pixel1, pixel2)
  interpolation_2 = linear_interpolation(Pt1_x, Pt2_x, float(location_x), pixel3, pixel4)
  interpolation_3 = linear_interpolation(Pt1_y, Pt2_y, float(location_y), interpolation_1, interpolation_2)
  if interpolation_3.ndim == 0:
    return uint8(round(interpolation_3, 0))
  for i in range(interpolation_3.ndim):
    interpolation_3[i] = uint8(round(interpolation_3[i], 0))
  return interpolation_3
  
