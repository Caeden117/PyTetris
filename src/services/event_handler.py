import pygame
import sys
from ..calculations.shapes_calculations import adjust_speeds

class EventHandle:
    def __init__(self, event_variables, gui_collisions, constants):
        self.events_mapper = {
            pygame.QUIT: self.quit_handler,
            pygame.KEYDOWN: self.keydown_handler,
            pygame.KEYUP: self.keyup_handler,
            pygame.MOUSEBUTTONDOWN: self.mousedown_handler,
            pygame.MOUSEBUTTONUP: self.mouseup_handler
        }
        self.event_variables = event_variables
        self.gui_collisions = gui_collisions
        self.constants = constants
        self.keys_pressed = {}

    def quit_handler(self, event):
        self.event_variables.set_running(False)
        sys.exit()

    def adjust_movement_speeds(self):
        pass

    def keydown_handler(self, event):
        if (event.key == pygame.K_q):
            self.event_variables.set_running(False)

        elif (event.key == pygame.K_DOWN):
            delay = adjust_speeds(self.event_variables, self.constants)
            self.event_variables.set_movement_delay(delay//6)

        elif(event.key == pygame.K_UP):
            curr_shape = self.event_variables.get_current_shape()
            curr_shape.increment_current_rotation()
        
        elif(event.key == pygame.K_ESCAPE): # Use ESC for pause
            curr_pause = self.event_variables.get_pause()
            self.event_variables.set_pause(not curr_pause)

        # Instant Drop mapped to SPACE    
        elif(event.key == pygame.K_SPACE): # Updating so SPACE instant drops
            # Get the current state
            curr_shape = self.event_variables.get_current_shape()
            grid_cells = self.event_variables.get_grid_matrix()

            # There is an active shape and we are not in a transition state
            if curr_shape and curr_shape != -1:
                curr_shape.instant_drop(grid_cells)
                

        elif(event.key == pygame.K_c):
            self.hold_piece_action()
        
    def hold_piece_action(self):
        """Handle the hold piece mechanic - swap current piece with held piece."""
        if not self.event_variables.get_can_hold():
            return  # Already held this turn
        
        curr_shape = self.event_variables.get_current_shape()
        if curr_shape is None or curr_shape == -1:
            return  # No active piece to hold
        
        held_shape = self.event_variables.get_held_piece()
        grid_rows = self.event_variables.get_grid_matrix()
        
        if held_shape is None:
            # First hold: store current piece, spawn new one from bag
            curr_shape.reset_to_spawn(grid_rows)
            self.event_variables.set_held_piece(curr_shape)
            self.event_variables.set_current_shape(-1)  # Trigger new spawn
        else:
            # Swap: held piece becomes current, current becomes held
            curr_shape.reset_to_spawn(grid_rows)
            held_shape.reset_to_spawn(grid_rows)
            self.event_variables.set_held_piece(curr_shape)
            self.event_variables.set_current_shape(held_shape)
        
        self.event_variables.set_can_hold(False)

    def keyup_handler(self, event):
        if (event.key == pygame.K_DOWN):
            delay = adjust_speeds(self.event_variables, self.constants)
            self.event_variables.set_movement_delay(delay)

        if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            self.keys_pressed.pop(event.key, None)

    def mousedown_handler(self, event):
        self.event_variables.set_is_mouse_pressed(True)
        self.gui_collisions.mouse_down_collisions()
        

    def mouseup_handler(self, event):
        self.event_variables.set_is_mouse_pressed(False)


    def handle_event(self, event):
        type_func = self.events_mapper.get(event.type)
        if type_func:
            type_func(event)

        keys = pygame.key.get_pressed()
        self.event_variables.set_left_pressed(keys[pygame.K_LEFT])
        self.event_variables.set_right_pressed(keys[pygame.K_RIGHT])
