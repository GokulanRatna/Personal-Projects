
import math
import pygame
import random
import time
from game_objects import GameObject, Snake, Food, Predator, PowerUp 

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont(None, 36)

# Main game loop
snake = Snake()
food = Food(150, 150)
predator = Predator(400, 400)
score = 0
highscore = 0
game_over = False
paused = False
speed = 5
power_up = None
power_up_timer = 0
power_up_effect_timer = None

run = True
while run:
    pygame.time.delay(100)

    if power_up_effect_timer and time.time() - power_up_effect_timer >= 5:
        speed = 5
        power_up_effect_timer = None

    if power_up_timer <= 0:
        power_up = PowerUp(random.randint(5, 490), random.randint(5, 490))
        power_up_timer = random.randint(200, 500)
    else:
        power_up_timer -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        paused = not paused
    if keys[pygame.K_q] and (game_over or paused):
        run = False


    if not game_over and not paused:
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -speed
        if keys[pygame.K_RIGHT]:
            dx = speed
        if keys[pygame.K_UP]:
            dy = -speed
        if keys[pygame.K_DOWN]:
            dy = speed

        snake.move(dx, dy)

        if snake.segments[0].rect.colliderect(food.rect):
            food.rect.topleft = (random.randint(5, 490), random.randint(5, 490))
            snake.grow()
            score += 1

        predator.move_towards(snake.segments[0])

        if snake.segments[0].rect.colliderect(predator.rect):
            game_over = True
            if score > highscore:
                highscore = score

        if power_up and snake.segments[0].rect.colliderect(power_up.rect):
            speed = 10
            power_up = None
            power_up_effect_timer = time.time()

        win.fill((0, 0, 0))
        snake.draw(win, True)  # True for drawing eyes and tongue
        food.draw(win)
        predator.draw(win, snake.segments[0])


        if power_up:
            power_up.draw(win)

        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        win.blit(score_text, (10, 10))

    elif game_over:
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        win.blit(game_over_text, (200, 200))
        restart_text = font.render('Press R to Restart', True, (255, 255, 255))
        win.blit(restart_text, (150, 250))
        quit_text = font.render('Press Q to Quit', True, (255, 255, 255))
        win.blit(quit_text, (175, 275))
        highscore_text = font.render(f'Highscore: {highscore}', True, (255, 255, 255))
        win.blit(highscore_text, (175, 300))

        if keys[pygame.K_r]:
            snake = Snake()
            predator.rect.topleft = (400, 400)
            food.rect.topleft = (150, 150)
            score = 0
            game_over = False
    
    elif paused:
        paused_text = font.render('Paused', True, (255, 255, 0))
        win.blit(paused_text, (200, 200))
        resume_text = font.render('Press P to Resume', True, (255, 255, 255))
        win.blit(resume_text, (150, 250))
        quit_text = font.render('Press Q to Quit', True, (255, 255, 255))
        win.blit(quit_text, (175, 275))


    pygame.draw.rect(win, (255, 255, 255), (0, 0, 500, 500), 5)
    pygame.display.update()


pygame.quit()