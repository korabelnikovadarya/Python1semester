# Используемые библиотеки

import math
from random import choice, randint
import time
import pygame

# Заголовок игрового окна
pygame.display.set_caption("Попади в мишень")

FPS = 30
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
# Размеры окна
WIDTH = 800
HEIGHT = 600
# Функция - знак числа
def sign(x):
    return 1 if x >= 0 else -1
# Класс мячей (шариков), которыми выстреливает пушка
class Ball:
    def __init__(self, screen: pygame.Surface, x=350, y=450):
        # x - начальное положение мяча по горизонтали
        # y - начальное положение мяча по вертикали
        self.screen = screen
        self.x = x  # нач. координата шарика по Ox
        self.y = y  # нач. координата шарика по Oy
        self.r = 10  # радиус шарика
        self.vx = 0  # скорость по Ox
        self.vy = 0  # скорость по Oy
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):

        # Перемещение мяча (шарика)
        # self.vy, self.vx - скорости шарика по оси у и х соответственно
        self.x += self.vx
        self.y -= self.vy
        self.vy -= 3
        if self.y < 0:
            self.vy *= (-1)
            self.vy -= 3
        if self.y > 590:
            self.vy *= (-1)
            self.vy -= 3

    def draw(self):
        # Рисуем шарик
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r)

    def hittest(self, obj):
        # Если произошло попадание в цель, то к броску подготавливается новый шар
        if (obj.r + self.r) >= (((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)) ** 0.5:
            return True

        else:
            return False
class Gun:
    # Класс пушки
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.color = GREEN
        # Координаты пушки
        self.x = WIDTH / 2
        self.y = 390

        self.v = 3
        self.r = 30


    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        # Выстрел мячом происходит при отпускании кнопки мыши
        # Начальные значения компонент скорости мяча vx и vy зависят от положения мыши
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.x = self.x
        new_ball.y = self.y
        new_ball.r += 10
        self.angle = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.angle) * 3
        new_ball.vy = - self.f2_power * math.sin(self.angle) * 3
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10



    def targetting(self, event):
        # Прицеливание. Чем дольше зажимаем правую кнопку мыши, чем быстрее впоследствие будет лететь мяч
        if event.pos[0] - self.x > 0:
            self.angle = math.atan((self.y - event.pos[1]) / (event.pos[0] - self.x))
        elif event.pos[0] - self.x < 0:
            self.angle = math.pi + math.atan((self.y - event.pos[1]) / (event.pos[0] - self.x))
        else:
            if self.y - event.pos[1] >= 0:
                self.angle = math.pi / 2
            else:
                self.angle = - math.pi / 2
        if self.f2_on:
            self.color = RED
        else:
            self.color = BLACK



    def draw(self):

        # Прорисовка тележки, которая прицеливается
        pygame.draw.circle(self.screen, (121, 120, 255), (self.x, self.y + 40), 60, 50) # Верхняя часть тележки
        pygame.draw.circle(self.screen, (159, 186, 255), (self.x, self.y + 40), 35) # Верхняя часть тележки (второй слой)
        pygame.draw.rect(self.screen, (21, 120, 255), (self.x - 70, self.y + 40, 140, 65)) # Нижняя часть тележки (прямоугольник)

        pygame.draw.circle(self.screen, (80, 80, 80), (self.x - 48, self.y + 80), 33) # Колесо левое
        pygame.draw.circle(self.screen, (80, 80, 80), (self.x + 48, self.y + 80), 33) # Колесо правое

        pygame.draw.polygon(self.screen, self.color, [(self.x, self.y), (
        self.x + self.f2_power * math.cos(self.angle), self.y - self.f2_power * math.sin(self.angle)),
                                          (self.x + self.f2_power * math.cos(self.angle) - 8 * math.sin(self.angle),
                                           self.y - self.f2_power * math.sin(self.angle) - 8 * math.cos(
                                               self.angle)),
                                          (self.x - 8 * math.sin(self.angle),
                                           self.y - 8 * math.cos(self.angle)),
                                          (self.x, self.y)])
    def power_up(self):
        # Функция отвечает за увеличение скорости шарика, макс. знак 100
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 2
            self.color = RED
        else:
            self.color = GREY

# Первая мишень
class Target:
    def __init__(self, screen: pygame.Surface, color, points, live):
        self.screen = screen
        self.color = BLACK
        self.points = 0
        self.live = 1
        self.new_target()
        self.x = randint(600, 750)
        self.y = randint(200, 200)
        self.vy = 8

    def move(self):
        #self.vy -= 3
        self.vy = randint(1, 10) * sign(self.vy)
        self.y -= self.vy
        if self.y < 0:
            self.vy *= (-1)
            self.y -= self.vy
        if self.y > 590:
            self.vy *= (-1)
            self.y -= self.vy


    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
    def new_target(self):
        # Инициализация новой цели
        self.x = randint(600, 750)
        self.y = randint(0, 70)
        self.r = randint(15, 30)
        self.live = 1
        self.color = (255, 63, 128)

    def hit(self, points=1):
        # Количество попаданий по первой мишени
        self.points += points

# Вторая мишень
class Target2:
    def __init__(self, screen: pygame.Surface, color, points, live):
        self.screen = screen
        self.color = BLACK
        self.points = 0
        self.live = 1
        self.new_target()
        self.x = randint(10, 70)
        self.y = randint(200, 200)
        self.vy = 8

    def move(self):
        self.vy = randint(1, 10) * sign(self.vy)
        self.y -= self.vy
        if self.y < 0:
            self.vy *= (-1)
            self.y -= self.vy

        # Отскакивание от пола
        if self.y > 590:
            self.vy *= (-1)
            self.y -= self.vy


    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
    def new_target(self):
        self.x = randint(10, 70)
        self.y = randint(40, 160)
        self.r = randint(15, 30)
        self.live = 1
        self.color = (255, 133, 128)

    def hit(self, points=1):
        # Количество попаданий по второй мишени
        self.points += points


pygame.init()
# Рисуем изображение
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen, RED, 1, 1)
target2 = Target2(screen, RED, 1, 1)
finished = False

pygame.font.init()


while not finished:
    screen.fill((135, 255, 216))
    pygame.draw.rect(screen, (0, 179, 44), (0, HEIGHT - 100, WIDTH, 100))
    gun.draw()
    target.draw()
    target.move()
    target2.draw()
    target2.move()
    for b in balls:
        b.draw()

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('bye')
            finished = True
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
            gun.targetting(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
            gun.targetting(event)

    for b in balls:
        b.move()
        if (b.hittest(target) and target.live) or (b.hittest(target2) and target2.live):
            if (b.hittest(target) and target.live):
                target.live = 0
                target.hit()
                target.new_target()
            else:
                target2.live = 0
                target2.hit()
                target2.new_target()


    pygame.display.update()

# Открытие окна screen2, в котором отображается количество попаданий по мишениям (Score)
clock = pygame.time.Clock()
screen2 = pygame.display.set_mode((WIDTH, HEIGHT))
screen2.fill((0, 0, 0))
score = target2.points + target.points
font = pygame.font.SysFont('Comic Sans MS', 100, 4)
# Вывод на экран количества попаданий по мишеням
text = font.render(f'Your score: {str(score)}', True, (150, 100, 160))
place = text.get_rect(center=(400, 280))
screen2.blit(text, place)
pygame.display.update()
while finished:
    pygame.display.update()
    for event in pygame.event.get():

        pygame.display.update()
        if event.type == pygame.QUIT:

            finished = False
gun.power_up()
pygame.quit()
