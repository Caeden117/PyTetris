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
    

    def append_queue(self, grid_row=None):
        # If the seven bag is empty, refill it immediately
        if len(self.seven) == 0:
            self.load_seven(grid_row)

        # If queue is empty, grab the first 3
        if len(self.queue) == 0:
            # Make sure we have at least 3 in seven (we should after load_seven)
            num_to_take = min(len(self.seven), 3)
            for _ in range(num_to_take):
                self.queue.append(self.seven.pop(0))
            return

        # Move one from bag to queue
        if len(self.seven) > 0:
            self.queue.append(self.seven.pop(0))


    def get_queue_element(self, grid_row=None):
        # If queue is somehow empty, fill it
        if len(self.queue) == 0:
            self.append_queue(grid_row)
        
        # Get the next piece
        element = self.queue.pop(0)
        
        # Refill the queue so there's always a Next Up preview
        self.append_queue(grid_row)
        
        return element

