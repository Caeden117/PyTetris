import pygame
from .screen_loader import Screen
from ..calculations.dims import *


class PauseMenu(Screen):
    def __init__(self, constants, title, menu, event_state, screen):
        self.constants = constants
        self.title = title
        self.menu = menu
        self.event_state = event_state
        self.screen = screen
        self.volume = 5
        self.max_volume = 10
        self.dragging = False

        # Slider dimensions as fractions of container
        self.slider_x_off = 0.25
        self.slider_y_off = 0.55
        self.slider_width_frac = 0.50
        self.slider_height = 6
        self.knob_radius = 12

    def _get_slider_rect(self, coords):
        cx = coords['cont_x']
        cy = coords['cont_y']
        cw = coords['cont_width']
        ch = coords['cont_height']
        x = cx + cw * self.slider_x_off
        y = cy + ch * self.slider_y_off
        w = cw * self.slider_width_frac
        return x, y, w

    def _get_knob_x(self, slider_x, slider_w):
        return slider_x + (self.volume / self.max_volume) * slider_w

    def _handle_slider_input(self, slider_x, slider_y, slider_w):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        knob_x = self._get_knob_x(slider_x, slider_w)
        knob_rect = pygame.Rect(
            knob_x - self.knob_radius,
            slider_y - self.knob_radius,
            self.knob_radius * 2,
            self.knob_radius * 2
        )

        if mouse_pressed:
            if not self.dragging and knob_rect.collidepoint(mouse_pos):
                self.dragging = True
            if self.dragging:
                raw = (mouse_pos[0] - slider_x) / slider_w
                clamped = max(0.0, min(1.0, raw))
                self.volume = round(clamped * self.max_volume)
                pygame.mixer.music.set_volume(self.volume / self.max_volume)
        else:
            self.dragging = False

    def _draw_slider(self, coords, font, color):
        slider_x, slider_y, slider_w = self._get_slider_rect(coords)

        self._handle_slider_input(slider_x, slider_y, slider_w)

        # Track background
        track_rect = pygame.Rect(slider_x, slider_y - self.slider_height // 2,
                                 slider_w, self.slider_height)
        pygame.draw.rect(self.screen, (100, 100, 100), track_rect)

        # Filled portion
        knob_x = self._get_knob_x(slider_x, slider_w)
        filled_rect = pygame.Rect(slider_x, slider_y - self.slider_height // 2,
                                  knob_x - slider_x, self.slider_height)
        pygame.draw.rect(self.screen, color, filled_rect)

        # Knob
        pygame.draw.circle(self.screen, color, (int(knob_x), int(slider_y)),
                           self.knob_radius)

        # Volume number below slider
        vol_text = font.render(str(self.volume), True, color)
        text_x = slider_x + slider_w // 2 - vol_text.get_width() // 2
        text_y = slider_y + self.knob_radius + 10
        self.screen.blit(vol_text, (text_x, text_y))

        # "Volume" label above slider
        label_text = font.render("Volume", True, color)
        label_x = slider_x + slider_w // 2 - label_text.get_width() // 2
        label_y = slider_y - self.knob_radius - label_text.get_height() - 10
        self.screen.blit(label_text, (label_x, label_y))

    def _draw_resume_button(self, coords, font, color):
        box_dims = self.menu['box_dims']
        menu_entry = self.menu['coords']['Resume']
        x, y, width, height = calculate_menu_boxes(menu_entry, coords,
                                                   box_dims['width'],
                                                   box_dims['height'])
        pygame.draw.rect(self.screen, color,
                         (x, y, width, height),
                         width=self.menu['box_line_width'])
        text_surface = font.render("Resume", True, color)
        name_coords = center_elements(x, y, width, height,
                                      text_surface.get_width(),
                                      text_surface.get_height())
        self.screen.blit(text_surface, name_coords)

        rectangles = [{"rect": pygame.Rect(x, y, width, height),
                       "name": "Resume"}]
        self.event_state.set_menu_rectangles(rectangles,
                                             self.event_state.get_event_state())

    def draw_screen(self):
        coords = self.event_state.get_container_coords()
        color = self.menu['font_color']
        font = self.event_state.get_all_fonts()['other_fonts']

        title_coords = self.menu['title_coords']
        self.title.draw_title("PAUSED", title_coords)

        self._draw_resume_button(coords, font, color)
        self._draw_slider(coords, font, color)
