import pygame
from pygame.locals import *
import time
import random

SIZE = 40  # block.jpg에서 dimension이 40이니까, initial position이 40
BACKGROUND_COLOR = (171, 168, 168)

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3  # 40 dimension의 배수일걸
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):  # 화면 크기에서 40으로 나눈거 사이로 그리고 SIZE로 곱해준다
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE


class Snake:
    def __init__(self, parent_screen, length):  # Game의 surface를 parent_screen으로
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length  # 빈 배열과 size length를 곱한다
        self.y = [SIZE] * length
        self.direction = 'down'
        self.length = length

    def increase_length(self):
        # 길이를 늘리면서, x, y 배열에 무언가 추가해줘야한다
        self.length += 1
        self.x.append(1)
        self.y.append(1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):  # x,y is now array

        # 1번 블록 자리에 2번블록이, 2번자리에 3번째 블록이
        for i in range(self.length - 1, 0, -1):  # -1 means step size, reverse loop이다
            self.x[i] = self.x[i - 1]  # current x position will be your previous block position
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE  # SIZE로 놔서 pixel를 40으로 유지해준다
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):  # To move the block, write the function
        # 하나의 x,y가 아닌 여러 x,y를 위해 for loop
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))  # 이 이미지를 surface에 어떤 위치에 그려라
        pygame.display.flip()  # 여기있는 코드를 스크린에 작동시킨다


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Snake and Apple Game")
        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))  # self를 붙이면 class member 밑에 run에서도 쓰게
        self.surface.fill((171, 168, 168))  # Background Screen

        # Game이 snake을 갖고있으니 snake is inside Game class
        self.snake = Snake(self.surface, 1)  # Snake의 길이
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True  # True라는 뜻은 collision이 있다는것

        return False  # Collision이 없다

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0)) #이 사진은 (0,0)에서 all the way

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3") # 받아온 파라미터의 변수가 여기에 저장
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()  # 이걸 안넣어주면 화면이 초기화될것
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()  # snake가 apple에 닿으면 apple 위치가 바뀌어라

        # snake colliding with itself
        for i in range(3, self.snake.length):  # for loop 3에서 시작하는 이유는, 1번째 블록이 2,3번째 블록과 충돌이 불가능함으로
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                # 뱀이 자기 자신을 물었으니 game is over, 예외처리를 하여 처리
                raise "Game over"

    def show_game_over(self):
        self.render_background()
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        # Surface에 저장하기 위해서는 blit function is needed
        self.surface.blit(score, (800, 100))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        # Event Loop을 만들어야 한다.
        running = True
        pause = False

        while running:
            for event in pygame.event.get():  # give all the keyboard mouse and events
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    elif event.key == K_ESCAPE:
                        running = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_DOWN:
                            self.snake.move_down()
                        elif event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)


if __name__ == '__main__':
    game = Game()
    game.run()  # Game이 snake을 갖고있으니 snake is inside Game class
