from random import choice, randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Родительский класс с общими методами для дочерних."""

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Метод общей отрисовки."""


class Snake(GameObject):
    """Дочерний класс описывающий змейку."""
    
    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT

    def get_head_position(self):
        """Метод для получения координат головы змеи."""
        return self.positions[0]

    def update_direction(self):
        """Метод отвечающий за обновление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Метод сброса игрового поля в исходное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.next_direction = None
        self.direction = choice((UP, RIGHT, DOWN, LEFT))

    def move(self):
        """Метод отвечающий за обновление состояния змейки."""
        head_x, head_y = self.get_head_position()
        step_x, step_y = self.direction
        new_head = ((head_x + step_x * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + step_y * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw_object(self, position, color):
        """Закрашивает ячейку с заданной позицией и цветом."""
        head_rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions:
            self.draw_object(position, self.body_color)

        if self.last:
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR,
                         pg.Rect(self.last, (GRID_SIZE, GRID_SIZE)))


class Apple(GameObject):
    """Дочерний класс описывающий 'Яблоко'."""
    
    def __init__(self, occupied_positions=(), body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """
        Метод отвечающий за новую позицию для яблока.

        Учитывает позиции змейки и дополнительные занятые позиции.
        """
        while True:
            self.position = (
                GRID_SIZE * randint(0, GRID_WIDTH - 1),
                GRID_SIZE * randint(0, GRID_HEIGHT - 1)
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовка яблока."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """
    Функция взята из прекода.

    Отвечает за управление змейкой с помощью нажатий клавиш.
    Исправлен вариант с выходом через ESC.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Функция отвечающая за вход в программу."""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.length += 1
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
