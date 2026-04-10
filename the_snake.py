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
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """
    Родительский класс с общими методами для дочерних
    (стартовая позиция и покраска).
    """

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Метод общей отрисовки."""
        pass

    def draw_object(self, position, color):
        """как закрасить пиксель??? (Нашел в прекоде)."""
        head_rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)


class Snake(GameObject):
    """
    Класс описывающий непосредственно змейку
    (унаследован от Gameobjects).
    """

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
        """
        Метод сброса игрового поля в исходное состояние
        при поражении.
        """
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.next_direction = None
        self.direction = choice((UP, RIGHT, DOWN, LEFT))

    def move(self):
        """
        Метод отвечающий за обновление состояния змейки,
        а именно за добавление головы.
        """
        head_x, head_y = self.get_head_position()
        step_x, step_y = self.direction
        self.positions.insert(
            0,
            ((head_x + step_x * GRID_SIZE) % SCREEN_WIDTH,
             (head_y + step_y * GRID_SIZE) % SCREEN_HEIGHT)
        )

        # Удаляем хвост, только если длина списка превышает длину змейки
        if len(self.positions) > self.length:
            self.last = self.positions.pop()  # Сохраняем удалённую позицию
        else:
            self.last = None

    def draw(self):
        for position in self.positions:
            self.draw_object(position, self.body_color)


class Apple(GameObject):
    """
    Класс описывающий "Яблоко",
    его цвет и позицию на поле. Унаследован от Gameobjects.
    """

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position()
        self.initialize_position()

    def initialize_position(self):
        """Метод отвечающий за начальную позицию яблока (без учёта змейки)."""
        self.position = (
            GRID_SIZE * randint(0, GRID_WIDTH - 1),
            GRID_SIZE * randint(0, GRID_HEIGHT - 1)
        )

    def randomize_position(self):
        """
        Метод отвечающий за новую позицию для яблока проверяя,
        что она не совпадает с позицией змейки.
        """
        self.position = (
                GRID_SIZE * randint(0, GRID_WIDTH - 1),
                GRID_SIZE * randint(0, GRID_HEIGHT - 1)
            )

    def draw(self):
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """
    Функция взята из прекода,
    отвечает за управление змейкой с помощью нажатий клавиш.
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
    pg.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очищаем экран

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка столкновения со своим телом
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()  # Сразу сбрасываем состояние змейки без паузы

        # Проверка поедания яблока
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
            snake.length += 1  # Увеличиваем длину после поедания яблока

        # Отрисовываем змейку
        snake.draw()

        # Отрисовываем яблоко
        apple.draw()
        pg.display.update()

if __name__ == '__main__':
    main()