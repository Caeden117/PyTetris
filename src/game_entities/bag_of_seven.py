from .shape import Shape
from ..services import read_files
from ..calculations.dims import *
import random

class BagOfSeven:
    def __init__(self, 
                 constants, 
                 event_state,
                 screen,
                 shapes,
                 container_coords):
        self.constants = constants
        self.shape_rotations = shapes
        self.queue = []
        self.seven = []
        self.event_state = event_state
        self.screen = screen
        self.container_coords = container_coords

    def load_seven(self, grid_row):
        # SRS (Standard Rotation System) Color Mao
        srs_colors = {
            'I_SHAPE' : (0, 255, 255), # Cyan
            'O_SHAPE' : (255, 255, 0), # Yellow                                           
            'T_SHAPE' : (128, 0, 128), # Purple
            'S_SHAPE' : (0, 255, 0),  # Green
            'Z_SHAPE' : (255, 0, 0), # Red
            'J_SHAPE' : (0, 0, 255), # Blue
            'L_SHAPE' : (255, 165, 0) # Orange                                    
        }

        for k, v in self.shape_rotations.items():
            if k == "BLACK":
                continue

            # Instead of Random Colors. Use the map to get the correct color, default to grey if not found
            print(f"Debug: The key is '{k}'")
            shape_color = srs_colors.get(k, (128, 128, 128))

            block_size = self.constants['BLOCK_SIZE']
            random_pos = calculate_shape_pos(grid_row, k)
            blit_coords = [random_pos[0], random_pos[1]]
            shape_obj = Shape(self.constants,
                              self.event_state,
                              self.screen,
                              self.shape_rotations,
                              k,
                              shape_color, # Use mapped color here
                              blit_coords,
                              random_pos[2]
                              )
            self.seven.append(shape_obj)
        self.seven  = random.sample(self.seven, len(self.seven))
    
    def append_queue(self):
        if len(self.queue) == 0:
            for x in range(0, 3):
                self.queue.append(self.seven[x])
            del self.seven[0: 3]
            return
        self.queue.append(self.seven[0])
        del self.seven[0]

    def get_queue_element(self):
        element = self.queue[0]
        del self.queue[0]
        self.append_queue()
        return element