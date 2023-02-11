from __future__ import annotations
from enum import Enum
import pygame
from nim import Nim 
from screen import Screen
from button import Button

BOT_MOVE_EVENT = pygame.USEREVENT
BOT_DELAY = 1000

WIDTH, HEIGHT = 900, 720 
BG_COLOR = (255, 255, 0)

BALL_RADIUS = 26
FOCUS_BALL_RADIUS = 34
BALL_SEP = 3 
COL_WIDTH_RATIO = 0.8

LABEL_FONT_SIZE = 34
BALL_FONT_COLOR = (255, 0, 0)
LIMIT_FONT_COLOR = (0, 0, 255)

TITLE_FONT_SIZE = 52
TITLE_SEP = 11.5
PLAYER1_FONT_COLOR = (0, 0, 255)
PLAYER2_FONT_COLOR = (255, 0, 0)

END_TURN_BUTTON_WIDTH_RATIO = 0.25
END_TURN_BUTTON_WIDTH = int(END_TURN_BUTTON_WIDTH_RATIO * WIDTH)
END_TURN_BUTTON_HEIGHT = 50
END_TURN_BUTTON_SEP = 12 
END_TURN_BUTTON_BG_COLOR = (0, 0, 255)
END_TURN_BUTTON_BORDER_RADIUS = 15
END_TURN_BUTTON_ELEVATION = 8
END_TURN_BUTTON_SHDW_COLOR = (0, 0, 0)
END_TURN_BUTTON_FONT_SIZE = 48
END_TURN_BUTTON_ACTIVE_FONT_COLOR = (255, 255, 255)
END_TURN_BUTTON_INACTIVE_FONT_COLOR = (128, 128, 128)

class Turn(Enum): 
    PLAYER1 = 1
    PLAYER2 = 2
    def switch(self) -> Turn: 
        return Turn.PLAYER2 if self is Turn.PLAYER1 else Turn.PLAYER1
    
class MainScreen(Screen): 
    sprite: pygame.Surface
    focus_sprite: pygame.Surface
    label_font: pygame.font.Font
    title_font: pygame.font.Font
    game: Nim
    turn: Turn
    col: int
    amt: int
    limits: list[int]
    end_turn_button: Button
    
    def __init__(self, sprite: pygame.Surface, game: Nim = Nim()): 
        self.sprite = pygame.transform.smoothscale(sprite, (2*BALL_RADIUS, 2*BALL_RADIUS))
        self.focus_sprite = pygame.transform.smoothscale(sprite, (2*FOCUS_BALL_RADIUS, 2*FOCUS_BALL_RADIUS))
        self.label_font = pygame.font.SysFont(None, LABEL_FONT_SIZE)
        self.title_font = pygame.font.SysFont(None, TITLE_FONT_SIZE) 
        self.game = game
        self.turn = Turn.PLAYER1
        self.col, self.amt = self.game.next_move()
        self.limits = list([self.game.get_limit(i) for i in range(0, len(self.game.balls))])
        end_turn_button_sx = (WIDTH - END_TURN_BUTTON_WIDTH) // 2
        end_turn_button_sy = (HEIGHT - END_TURN_BUTTON_HEIGHT - 
            END_TURN_BUTTON_SEP - END_TURN_BUTTON_ELEVATION)
        self.end_turn_button = Button(
            (end_turn_button_sx, end_turn_button_sy, END_TURN_BUTTON_WIDTH, END_TURN_BUTTON_HEIGHT), 
            END_TURN_BUTTON_BG_COLOR, active=False, border_radius=END_TURN_BUTTON_BORDER_RADIUS, 
            elevation=END_TURN_BUTTON_ELEVATION, shdw_color=END_TURN_BUTTON_SHDW_COLOR, 
            font=pygame.font.SysFont(None, END_TURN_BUTTON_FONT_SIZE), text='End Turn', 
            font_color=END_TURN_BUTTON_INACTIVE_FONT_COLOR, on_release=self.end_button_on_release)
        
    def reset_turn(self): 
        self.turn = self.turn.switch()
        self.col, self.amt = self.game.next_move()  
        self.limits = list([self.game.get_limit(i) for i in range(0, len(self.game.balls))])
        if self.turn is Turn.PLAYER2: 
            pygame.time.set_timer(BOT_MOVE_EVENT, BOT_DELAY, loops=self.amt)

    def end_button_on_release(self, button: Button): 
        self.reset_turn()
        button.active = False
        button.font_color = END_TURN_BUTTON_INACTIVE_FONT_COLOR

    def get_ball_rect(self, col: int, ball: int) -> pygame.Rect: 
        col_width = (WIDTH * COL_WIDTH_RATIO) / len(self.game.balls)
        col_sep_width = (WIDTH * (1-COL_WIDTH_RATIO)) / (len(self.game.balls)+1)
        x = col * col_width + (col+1) * col_sep_width + (col_width - 2*BALL_RADIUS) / 2
        y = (self.end_turn_button.rect.y - END_TURN_BUTTON_SEP - 
            self.label_font.size(str(self.game.balls[col]))[1] -
            self.label_font.size(str(self.limits[col]))[1] -
            ball * (2*BALL_RADIUS + BALL_SEP))     
        return pygame.Rect(x, y, BALL_RADIUS, BALL_RADIUS) 

    def get_col_pressed(self, pos: tuple[int, int]) -> int: 
        x, y = pos
        col_width = (WIDTH * COL_WIDTH_RATIO) / len(self.game.balls)
        col_sep_width = (WIDTH * (1-COL_WIDTH_RATIO)) / (len(self.game.balls)+1)
        col = int(x / (col_width + col_sep_width)) 
        if col < 0 or col >= len(self.game.balls): 
            return -1
        rect = self.get_ball_rect(col, self.game.balls[col]) 
        center = pygame.Vector2(rect.center) 
        if center.distance_to(pos) > BALL_RADIUS: 
            return -1
        return col if self.limits[col] else -1

    def draw(self, surface: pygame.Surface): 
        surface.fill(BG_COLOR)    
        if self.game.is_finished(): 
            title_text = 'Player 2 Wins' if self.turn is Turn.PLAYER1 else 'Player 1 Wins'
            title_color = PLAYER2_FONT_COLOR if self.turn is Turn.PLAYER1 else PLAYER1_FONT_COLOR  
        else: 
            title_text = 'Player 1 Turn' if self.turn is Turn.PLAYER1 else 'Player 2 Turn'
            title_color = PLAYER1_FONT_COLOR if self.turn is Turn.PLAYER1 else PLAYER2_FONT_COLOR 
        tx = (WIDTH - self.title_font.size(title_text)[0]) / 2
        surface.blit(self.title_font.render(title_text, True, title_color), (tx, TITLE_SEP))
        col_width = (WIDTH * COL_WIDTH_RATIO) / len(self.game.balls)
        col_sep_width = (WIDTH * (1-COL_WIDTH_RATIO)) / (len(self.game.balls)+1)
        for i in range(0, len(self.game.balls)): 
            limit_text = self.label_font.render(str(self.limits[i]), True, LIMIT_FONT_COLOR)
            lx = i * col_width + (i+1) * col_sep_width + (col_width - limit_text.get_width()) / 2
            ly = self.end_turn_button.rect.y - limit_text.get_height() - END_TURN_BUTTON_SEP
            balls_text = self.label_font.render(str(self.game.balls[i]), True, BALL_FONT_COLOR)
            bx = i * col_width + (i+1) * col_sep_width + (col_width - balls_text.get_width()) / 2
            by = ly - balls_text.get_height()
            if self.limits[i]: 
                surface.blit(limit_text, (lx, ly))
            if self.game.balls[i]: 
                surface.blit(balls_text, (bx, by))
            for j in range(1, self.game.balls[i]+1): 
                col = self.get_col_pressed(pygame.mouse.get_pos())
                rect = self.get_ball_rect(i, j)
                shift = FOCUS_BALL_RADIUS - BALL_RADIUS
                focus_rect = pygame.Rect(rect.x-shift, rect.y-shift, 2*FOCUS_BALL_RADIUS, 2*FOCUS_BALL_RADIUS)
                if i == col and j == self.game.balls[i] and self.turn is Turn.PLAYER1: 
                    surface.blit(self.focus_sprite, focus_rect)
                else: 
                    surface.blit(self.sprite, rect)
        self.end_turn_button.draw(surface)
        pygame.display.update()

    def run(self, event: pygame.event.Event | None = None) -> Screen | None:         
        self.end_turn_button.run(event)
        if event: 
            if event.type == pygame.QUIT: 
                return None 
            elif event.type == pygame.MOUSEBUTTONDOWN and self.turn is Turn.PLAYER1: 
                self.col = self.get_col_pressed(pygame.mouse.get_pos())
                if self.col >= 0: 
                    self.game.balls[self.col] -= 1   
                    self.limits[self.col] -= 1
                    for i in range(0, len(self.limits)): 
                        if i != self.col: 
                            self.limits[i] = 0
                    self.end_turn_button.active = True
                    self.end_turn_button.font_color = END_TURN_BUTTON_ACTIVE_FONT_COLOR
            elif event.type == BOT_MOVE_EVENT and self.turn is Turn.PLAYER2: 
                self.game.balls[self.col] -= 1
                self.amt -= 1
                self.limits[self.col] -= 1
                for i in range(0, len(self.limits)): 
                    if i != self.col: 
                        self.limits[i] = 0
                if self.amt <= 0: 
                    self.reset_turn()
        return self
