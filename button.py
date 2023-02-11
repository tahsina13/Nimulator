from __future__ import annotations
from typing import Callable
import pygame
from screen import Screen

Color = pygame.Color | tuple[int, int, int] | str

class Button(Screen): 
    rect: pygame.Rect
    bg_color: Color
    active: bool
    width: int
    border_radius: int
    elevation: int
    shdw_color: Color
    bg_img: pygame.Surface | None
    font: pygame.font.Font | None
    text: str
    font_color: Color
    on_default: Callable[[Button], None]
    on_hover: Callable[[Button], None]    
    on_click: Callable[[Button], None]
    on_release: Callable[[Button], None]
    
    def __init__(self, rect: pygame.Rect | tuple[int, int, int, int], bg_color: Color, *, active: bool = True, 
    width: int = 0, border_radius: int = 0, elevation: int = 0, shdw_color: Color | None = None, 
    bg_img: pygame.Surface | None = None, font: pygame.font.Font | None = None, text: str = '', font_color: Color = (0, 0, 0),
    on_default: Callable[[Button], None] = lambda _: None, on_hover: Callable[[Button], None] = lambda _: None, 
    on_click: Callable[[Button], None] = lambda _: None, on_release: Callable[[Button], None] = lambda _: None):
        self.set_rect(rect)
        self.bg_color = bg_color
        self.active = active
        self.width = width
        self.border_radius = border_radius
        self.elevation = elevation
        self.shdw_color = shdw_color if shdw_color else bg_color
        self.set_bg_img(bg_img)
        self.font = font
        self.text = text
        self.font_color = font_color
        self.on_default = on_default
        self.on_hover = on_hover
        self.on_click = on_click
        self.on_release = on_release

    def set_rect(self, rect: pygame.Rect | tuple[int, int, int, int]): 
        self.rect = pygame.Rect(rect)
        if hasattr(self, 'bg_img') and self.bg_img: 
            self.bg_img = pygame.transform.smoothscale(self.bg_img, self.rect.size)
    
    def set_bg_img(self, bg_img: pygame.Surface | None): 
        self.bg_img = (pygame.transform.smoothscale(bg_img, self.rect.size) 
            if bg_img else None)

    def is_hover(self) -> bool: 
        return self.active and self.rect.collidepoint(pygame.mouse.get_pos())

    def is_click(self) -> bool: 
        return self.is_hover() and pygame.mouse.get_pressed()[0]

    def draw(self, surface: pygame.Surface): 
        rect = self.rect.copy()
        shdw_rect = self.rect.copy()
        if self.is_click(): 
            rect.y = rect.y + self.elevation
        else: 
            shdw_rect.height = shdw_rect.height + self.elevation
        shdw_rect.midtop = rect.midtop
        pygame.draw.rect(surface, self.shdw_color, shdw_rect,
            self.width, self.border_radius)
        pygame.draw.rect(surface, self.bg_color, rect, 
            self.width, self.border_radius)
        if self.bg_img: 
            bg_img_rect = self.bg_img.get_rect(center=rect.center)
            surface.blit(self.bg_img, bg_img_rect)
        if self.font: 
            text_surf = self.font.render(self.text, True, self.font_color) 
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)
    
    def run(self, event: pygame.event.Event | None = None) -> Screen | None: 
        if self.active: 
            if event and event.type == pygame.MOUSEBUTTONDOWN and self.is_hover(): 
                self.on_click(self)
            elif event and event.type == pygame.MOUSEBUTTONUP and self.is_hover(): 
                self.on_release(self)
            elif self.is_hover():
                self.on_hover(self)
            else: 
                self.on_default(self)
        return self