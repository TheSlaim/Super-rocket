# Example file showing a circle moving on screen
import pygame
from random import uniform, randint, choice
from time import sleep

# pygame setup
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

background = pygame.image.load("ref/cosmos.jpg")
player_img = pygame.image.load("ref/rocket.png")
enemy_img = [pygame.image.load(f"ref/enemy_{i}.png") for i in range(1, 4)]
bullet = pygame.Surface((5,10))
bullet.fill((255, 0, 0))

pygame.mixer.music.load("ref/music.mp3")
pygame.mixer.music.play(-1)

bullet_list = []
bullet_speed = 5

score = 0
missed = 0

num_enemies = 3
enemies_list = []
for _ in range(num_enemies):
    enemies_list.append([randint(0, WIDTH - 50), randint(-100, -40), uniform(0.3, 0.5), choice(enemy_img)])

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_list.append([player_pos.x + 20, player_pos.y])

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(background, (0, 0))
    # screen.blit(enemy_img, (0, 0))
    screen.blit(player_img, (player_pos.x, player_pos.y))

    score_text = font.render(f'Знищено {score}/10', True, (255, 255, 255))
    missed_text = font.render(f'Пропущено {missed}/3', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(missed_text, (10, 50))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    for enemy in enemies_list:
        enemy[1] += enemy[2]
        if enemy[1] >HEIGHT:
            missed += 1
            enemy[0] = randint(0, WIDTH - 50)
            enemy[1] = randint(-100, -40)
            enemy[2] = uniform(0.3, 0.5)
            enemy[3] = choice(enemy_img)

    new_bullet = []
    for bull in bullet_list:
        bull[1] -= bullet_speed
        if bull[1] > 0:
            new_bullet.append(bull)
    bullet_list = new_bullet

    for enemy in enemies_list:
        if player_pos.x < enemy[0] + 50 and player_pos.x + 50 > enemy[0] and player_pos.y < enemy[1] and player_pos.y + 50 > enemy[1]:
            print('Зіткнення з ворогом')
            end_game_text = font.render('Зіткнення з ворогом', True, (255, 255, 255))
            screen.blit(end_game_text, (350, 300))
            pygame.display.update()
            sleep(5)
            running = False


    for bull in bullet_list:
        for enemy in enemies_list:
            if enemy[0] < bull[0] < enemy[0] + 50 and enemy[1] < bull[1] < enemy[1] + 50:
                score += 1
                enemies_list.remove(enemy)
                bullet_list.remove(bull)
                enemies_list.append([randint(0, WIDTH - 50), randint(-100, -40), uniform(0.3, 0.5), choice(enemy_img)])




    if score >= 10:
        finish_text = font.render('It is Victory', True, (255, 255, 255))
        screen.blit(finish_text, (350, 300))
        pygame.display.update()
        sleep(5)
        print("Перемога")

        running = False
    if missed >= 3:
        TheEnd_text = font.render('It is End', True, (255, 255, 255))
        screen.blit(TheEnd_text, (350, 300))
        pygame.display.update()
        sleep(5)
        print("Програш")
        running = False

    for enemy in enemies_list:
        screen.blit(enemy[3], (enemy[0], enemy[1]))

    for bull in bullet_list:
        screen.blit(bullet, (bull[0], bull[1]))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()