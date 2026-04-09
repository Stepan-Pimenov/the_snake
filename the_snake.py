from random import choice, randint

import pygame

'''
Здесь были внесены небольшие изменения
с целью убоать пустой хвост отстающий от тела.
'''
# Константы для размеров поля и сетки:
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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    '''
    Родительский класс с общими методами для дочерних
    (стартовая позиция и покраска).
    '''
    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        pass

    def draw_object(self, position, color):
        '''как закрасить пиксель??? (Нашел в прекоде).'''
        head_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)


class Snake(GameObject):
    '''
    Класс описывающий непосредственно змейку
    (унаследован от Gameobjects).
    '''
    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        '''Метод для получения координат головы змеи.'''
        return self.positions[0]

    def update_direction(self):
        '''Метод отвечающий за обновление движения змейки'''
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        '''
        Метод сброса игрового поля в исходное состояние
        при поражении.
        '''
        self.length = 1
        self.positions = [self.position] 
        self.last = None
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.direction = choice((UP, RIGHT, DOWN, LEFT))

    def move(self):
        '''
        Метод отвечающий за обновление состояния змейки,
        а именно за добавление головы
        '''
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        self.positions.insert(0, new_position)  # Добавляем голову

        # Удаляем хвост, только если длина списка превышает длину змейки
        if len(self.positions) > self.length:
            self.last = self.positions.pop()  # Сохраняем удалённую позицию


class Apple(GameObject):
    '''
    Класс описывающий "Яблоко",
    его цвет и позицию на поле. Унаследован от Gameobjects.
    '''
    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        '''
        Было подправленно после того,
        как яблоко появилось за игровым полем (это было забавно).
        '''
        width = GRID_SIZE * randint(0, GRID_WIDTH - 1)
        height = GRID_SIZE * randint(0, GRID_HEIGHT - 1)
        self.position = width, height

    def draw(self):
        '''
        Метод отвечающий за покраску яблока
        '''
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    '''
    Функция взята из прекода,
    отвечает за управление змейкой с помощью нажатий клавиш
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def stop_game(snake):
    '''
    Данная функция отвечает за то, чтобы игры не шла по круга
    в случае столкновения с телом.
    '''
    if snake.get_head_position() in snake.positions[1:]:
        game_over = True
        while game_over:
            screen.fill(BOARD_BACKGROUND_COLOR)  # Очищаем экран
            font = pygame.font.Font(None, 36)
            text = font.render(
                "Game Over! Press Space to continue", True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        snake.reset()  # Сброс состояния змейки
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit


def main():
    '''Основная функция отвечающая за вход в программу'''
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очищаем экран

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        stop_game(snake)  # Вызов функции, чтобы игра не шла по кругу

        # Проверка поедания яблока
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
            snake.length += 1  # Увеличиваем длину после поедания яблока

        # Отрисовываем ВСЕ части змейки — голову, тело и хвост
        for position in snake.positions:
            snake.draw_object(position, snake.body_color)

        # Отрисовываем яблоко
        apple.draw_object(apple.position, apple.body_color)
        pygame.display.update()


if __name__ == '__main__':
    main()
'''Приятной игры!'''