import pygame
import random

pygame.init()

display_w = 500  #увеличь вдвое
display_h = 500  #увеличь вдвое

win = pygame.display.set_mode((display_w, display_h))

tank_size = 68  #увеличь вдвое
tank_img_0 = pygame.image.load("tank_0.png")
tank_img_0 = pygame.transform.scale(tank_img_0, (tank_size, tank_size))
tank_img_rotate_0 = tank_img_0
tank_0 = tank_img_0.get_rect(center=(tank_size / 2, tank_size / 2))
direction_0 = 'up'
tank_img_1 = pygame.image.load("tank_1.png")
tank_img_1 = pygame.transform.scale(tank_img_1, (tank_size, tank_size))
tank_img_rotate_1 = tank_img_1
tank_1 = tank_img_1.get_rect(center=(tank_size / 2, tank_size / 2))
direction_1 = 'up'
shells_0 = []
shells_1 = []

walls1 = [
    pygame.Rect(50, 50, 50, 175),
    pygame.Rect(50, 275, 50, 175),
    pygame.Rect(225, 50, 50, 175),
    pygame.Rect(225, 275, 50, 175),
    pygame.Rect(400, 50, 50, 175),
    pygame.Rect(400, 275, 50, 175)
]  #увеличь вдвое все цифры
walls2 = [
    pygame.Rect(50, 50, 275, 50),
    pygame.Rect(225, 225, 50, 50),
    pygame.Rect(175, 400, 275, 50)
]  #увеличь вдвое все цифры

a = random.randint(0, 1)
tank_speed = 2  #увеличь вдвое
shell_speed = tank_speed + 2
clock = pygame.time.Clock()
FPS = 60
shell_size = 5  #увеличь вдвое
if a == 0:
    walls = walls1
else:
    walls = walls2

def draw_shells(shells):
    for shell in shells:
        pygame.draw.rect(win, (255, 237, 0), shell[0])
        if shell[1] == 'left':
            shell[0].x -= shell_speed
        elif shell[1] == 'right':
            shell[0].x += shell_speed
        elif shell[1] == 'up':
            shell[0].y -= shell_speed
        elif shell[1] == 'down':
            shell[0].y += shell_speed
        if shell[0].x < 0 or shell[0].x > display_w or shell[0].y < 0 or shell[0].y > display_h or shell[0].collidelist(walls)\
                != -1:
            shells.remove(shell)


def draw_tank(tank, tank_img, tank_img_rotate, direction, keys, k_left,
              k_right, k_up, k_down):
    tank_copy_left = tank.copy()
    tank_copy_left.x -= tank_speed
    tank_copy_right = tank.copy()
    tank_copy_right.x += tank_speed
    tank_copy_up = tank.copy()
    tank_copy_up.y -= tank_speed
    tank_copy_down = tank.copy()
    tank_copy_down.y += tank_speed

    if keys[k_left] and tank.x > 0 and tank_copy_left.collidelist(walls) == -1:
        tank.x -= tank_speed
        tank_img_rotate = pygame.transform.rotate(tank_img, 90)
        direction = 'left'
    elif keys[
            k_right] and tank.right < display_w and tank_copy_right.collidelist(
                walls) == -1:
        tank.x += tank_speed
        tank_img_rotate = pygame.transform.rotate(tank_img, -90)
        direction = 'right'
    elif keys[k_up] and tank.y > 0 and tank_copy_up.collidelist(walls) == -1:
        tank.y -= tank_speed
        tank_img_rotate = tank_img
        direction = 'up'
    elif keys[
            k_down] and tank.bottom < display_h and tank_copy_down.collidelist(
                walls) == -1:
        tank.y += tank_speed
        tank_img_rotate = pygame.transform.rotate(tank_img, 180)
        direction = 'down'

    win.blit(tank_img_rotate, tank)
    return tank, tank_img_rotate, direction


def new_shell(direction, tank):
    if direction == 'left':
        return pygame.Rect(tank.left - shell_size,
                           tank.centery - (shell_size // 2), shell_size,
                           shell_size), direction
    elif direction == 'right':
        return pygame.Rect(tank.right, tank.centery - (shell_size // 2),
                           shell_size, shell_size), direction
    elif direction == 'up':
        return pygame.Rect(tank.centerx - (shell_size // 2), tank.top,
                           shell_size, shell_size), direction
    elif direction == 'down':
        return pygame.Rect(tank.centerx - (shell_size // 2), tank.bottom,
                           shell_size, shell_size), direction

def shells_objects(shells):
  objects = []
  for shell in shells:
    objects.append(shell[0])
  return objects

def main():
    global tank_0, tank_img_rotate_0, direction_0, tank_1, tank_img_rotate_1, direction_1, shells_0, shells_1
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(shells_0) < 4:
                    shells_0.append(new_shell(direction_0, tank_0))

                if event.key == pygame.K_g and len(shells_1) < 4:
                    shells_1.append(new_shell(direction_1, tank_1))

        keys = pygame.key.get_pressed()
        win.fill((43, 23, 17))

        tank_0, tank_img_rotate_0, direction_0 = draw_tank(
            tank_0, tank_img_0, tank_img_rotate_0, direction_0, keys,
            pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

        tank_1, tank_img_rotate_1, direction_1 = draw_tank(
            tank_1, tank_img_1, tank_img_rotate_1, direction_1, keys,
            pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
      
        draw_shells(shells_0)
        draw_shells(shells_1)

        if tank_0.collidelist(shells_objects(shells_1)) != -1:
            print('Зеленый проиграл')
            break

        if tank_1.collidelist(shells_objects(shells_0)) != -1:
            print('Синий проиграл')
            break
      
        for wall in walls:
            pygame.draw.rect(win, (255, 255, 255), wall)

        clock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()
