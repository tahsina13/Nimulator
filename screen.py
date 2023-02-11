from __future__ import annotations
from abc import ABC, abstractmethod
import pygame

class Screen(ABC): 
    @abstractmethod
    def draw(self, surface: pygame.Surface): 
        pass
    @abstractmethod
    def run(self, event: pygame.event.Event | None = None) -> Screen | None: 
        pass