import pygame, sys, random
from pygame.math import Vector2

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music/music.mp3')
pygame.mixer.music.play(-1)

title_font = pygame.font.Font(None, 60)


black = (20, 20, 20)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 213, 40)
blue = (50, 153, 213)

cell_size = 30
cell_number = 25

OFFSET = 75

class Food:
    def __init__(self, snake1_body, snake2_body):
        self.position = self.random_pos(snake1_body, snake2_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect) 

    def random_cell(self):
        x = random.randint(0, cell_number - 1)
        y = random.randint(0, cell_number - 1)
        return Vector2(x, y)
        
    def random_pos(self, snake1_body, snake2_body):
        position = self.random_cell()
        while position in snake1_body or position in snake2_body:
            position = self.random_cell()

        return position
    
    
class Snake:
    def __init__(self, start_pos, direction, color):
        self.body = [start_pos]
        self.direction = direction
        self.add_block = False
        self.color = color
        
    def draw(self):
        for segment in self.body:
            segment_rect = pygame.Rect(OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, self.color, segment_rect, 0, 7)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_block:
            self.add_block = False
        else:
            self.body = self.body[:-1]


class Game:
    def __init__(self):
        self.snake1 = Snake(Vector2(2, 2), Vector2(1, 0), green)
        self.snake2 = Snake(Vector2(cell_number - 3, cell_number - 3), Vector2(-1, 0), blue)
        self.snake1.body = [Vector2(2, 2), Vector2(1, 2), Vector2(0, 2)]
        self.snake2.body = [Vector2(cell_number - 3, cell_number - 3), Vector2(cell_number - 2, cell_number - 3), Vector2(cell_number - 1, cell_number - 3)]
        self.food = Food(self.snake1.body, self.snake2.body)
        self.state = 'STOPPED'
        self.winner = None

    def draw(self):
        self.snake1.draw()
        self.snake2.draw()
        self.food.draw()

    def update(self):
        if self.state == 'RUNNING':
            self.snake1.update()
            self.snake2.update()
            self.check_collision_food()
            self.check_collision_wall()
            self.check_collision_snake()

    def check_collision_food(self):
        if self.food.position == self.snake1.body[0]:
            self.food.position = self.food.random_pos(self.snake1.body, self.snake2.body)
            self.snake1.add_block = True
        if self.food.position == self.snake2.body[0]:
            self.food.position = self.food.random_pos(self.snake1.body, self.snake2.body)
            self.snake2.add_block = True

    def check_collision_wall(self):
        if self.snake1.body[0].x == cell_number or self.snake1.body[0].x == -1 or self.snake1.body[0].y == cell_number or self.snake1.body[0].y == -1:
            self.winner = 'Player 2'
            self.game_over()
        if self.snake2.body[0].x == cell_number or self.snake2.body[0].x == -1 or self.snake2.body[0].y == cell_number or self.snake2.body[0].y == -1:
            self.winner = 'Player 1'
            self.game_over()

    def check_collision_snake(self):
        nohead1 = self.snake1.body[1:]
        nohead2 = self.snake2.body[1:]
        if self.snake1.body[0] in nohead1 or self.snake1.body[0] in nohead2:
            self.winner = 'Player 2'
            self.game_over()
        if self.snake2.body[0] in nohead2 or self.snake2.body[0] in nohead1:
            self.winner = 'Player 1'
            self.game_over()
        if self.snake1.body[0] == self.snake2.body[0]:
            self.winner = 'Draw'
            self.game_over()
    

    def game_over(self):
        self.snake1 = Snake(Vector2(2, 2), Vector2(1, 0), green)
        self.snake2 = Snake(Vector2(cell_number - 3, cell_number - 3), Vector2(-1, 0), blue)
        self.snake1.body = [Vector2(2, 2), Vector2(1, 2), Vector2(0, 2)]
        self.snake2.body = [Vector2(cell_number - 3, cell_number - 3), Vector2(cell_number - 2, cell_number - 3), Vector2(cell_number - 1, cell_number - 3)]
        self.food.position = self.food.random_pos(self.snake1.body, self.snake2.body)
        if self.winner == 'Player 1':
            message_font = pygame.font.Font(None, 40)
            message_surface = message_font.render('Player 1 wins', True, white)
            message_rect = message_surface.get_rect(center=(OFFSET + cell_number * cell_size // 2, OFFSET + cell_number * cell_size // 2))
            screen.blit(message_surface, message_rect)
            pygame.display.update()
            pygame.time.wait(1000)
            self.state = 'STOPPED'
        elif self.winner == 'Player 2':
            message_font = pygame.font.Font(None, 40)
            message_surface = message_font.render('Player 2 wins', True, white)
            message_rect = message_surface.get_rect(center=(OFFSET + cell_number * cell_size // 2, OFFSET + cell_number * cell_size // 2))
            screen.blit(message_surface, message_rect)
            pygame.display.update()
            pygame.time.wait(1000)
            self.state = 'STOPPED'
        elif self.winner == 'Draw':
            message_font = pygame.font.Font(None, 40)
            message_surface = message_font.render('Draw', True, white)
            message_rect = message_surface.get_rect(center=(OFFSET + cell_number * cell_size // 2, OFFSET + cell_number * cell_size // 2))
            screen.blit(message_surface, message_rect)
            pygame.display.update()
            pygame.time.wait(1000)
            self.state = 'STOPPED'


screen = pygame.display.set_mode((2*OFFSET + cell_number * cell_size, 2*OFFSET + cell_number * cell_size))
pygame.display.set_caption('DuelSnakes')

clock = pygame.time.Clock()

game = Game()
food_surface = pygame.image.load('Graphics/food.png').convert_alpha()
food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size))

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

title = True
while title:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            title = False
    screen.fill(black)
    title_surface = pygame.image.load('Graphics/title.png').convert_alpha()
    title_surface = pygame.transform.scale(title_surface, (600, 200))
    title_rect = title_surface.get_rect(center=(OFFSET + cell_number * cell_size // 2, OFFSET + cell_number * cell_size // 2 - 50))
    screen.blit(title_surface, title_rect)
    message_font = pygame.font.Font(None, 30)
    message_surface = message_font.render('Press any key to play', True, white)
    message_rect = message_surface.get_rect(center=(OFFSET + cell_number * cell_size // 2, OFFSET + cell_number * cell_size // 2 + 50))
    screen.blit(message_surface, message_rect)
    pygame.display.update()
    clock.tick(60)

while title == False:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()        
        if event.type == pygame.KEYDOWN:
            if game.state == 'STOPPED':
                game.state = 'RUNNING'
            if event.key == pygame.K_w and game.snake1.direction.y != 1:
                game.snake1.direction = Vector2(0, -1)
            if event.key == pygame.K_s and game.snake1.direction.y != -1:
                game.snake1.direction = Vector2(0, 1)
            if event.key == pygame.K_a and game.snake1.direction.x != 1:
                game.snake1.direction = Vector2(-1, 0)
            if event.key == pygame.K_d and game.snake1.direction.x != -1:
                game.snake1.direction = Vector2(1, 0)
            if event.key == pygame.K_UP and game.snake2.direction.y != 1:
                game.snake2.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake2.direction.y != -1:
                game.snake2.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake2.direction.x != 1:
                game.snake2.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake2.direction.x != -1:
                game.snake2.direction = Vector2(1, 0)
    screen.fill(black)
    pygame.draw.rect(screen, white, pygame.Rect(OFFSET - 5, OFFSET - 5, cell_number * cell_size + 10, cell_number * cell_size + 10), 5)
    game.draw()
    title_surface = pygame.image.load('Graphics/title.png').convert_alpha()
    title_surface = pygame.transform.scale(title_surface, (150, 50))
    screen.blit(title_surface, (OFFSET -5, 20))
    pygame.display.update()
    clock.tick(60)

