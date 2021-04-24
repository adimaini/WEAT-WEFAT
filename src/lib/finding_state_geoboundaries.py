import geopy
import numpy as np
import geopy.distance

class Geoboundaries:

    def __init__(self, left_bottom, right_top):
        self.left_bottom = left_bottom
        self.right_top = right_top
        self.max_distance = self.calculate_distance(self.left_bottom, self.right_top)
        self.twitter_bound = 25
        self.bounding_box_coords = []
    
    def get_vertical_points(self, start_point=None):
        'iterate a diagonal up and to the right. Returns the point of the top-right point.'
        if start_point is None: 
            start_point = self.left_bottom

        vertical_point = geopy.distance.distance(miles=self.twitter_bound).destination(start_point, bearing=0)
        # new_point = geopy.distance.distance(miles=self.twitter_bound).destination(vertical_point, bearing=45)
        # self.add_coordinates_to_bounding_box(start_point, new_point)
        while vertical_point[0] < self.right_top[0]: 
            self.get_right_points(vertical_point)
            self.get_vertical_points(new_point)
    
    def get_right_points(self, vertical_point):
        


        
    
    def add_coordinates_to_bounding_box(self, left_coord, right_coord):
        # reverse the coordinates for twitter which is in (long, lat) form and join them together 
        left_point = ' '.join(map(str, [*left_coord][:2][::-1]))
        right_point = ' '.join(map(str, [*tuple(right_coord)][:2][::-1]))
        self.bounding_box_coords.append(left_point + ' ' + right_point)


    def calculate_distance(self, left_coord, right_coord):
        return geopy.distance.geodesic(left_coord, right_coord)

    def meets_twitter_boundary_limits(self, left_coord, right_coord):
        if self.calculate_distance(left_coord, right_coord) <= self.twitter_bound:
            return True

    def main(self):
        self.iterate_diaganol_up()
        print(len(self.bounding_box_coords))
        print(self.bounding_box_coords)


if __name__ == '__main__':
    # coordinates need to be (lat, long) form 
    Geoboundaries((38.777895, -77.300710), (40.405451, -75.061367)).main()

    

    
        