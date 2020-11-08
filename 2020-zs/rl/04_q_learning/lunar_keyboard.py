import pygame
successes, failures = pygame.init()
import gym
print("{0} successes and {1} failures".format(successes, failures))


screen = pygame.display.set_mode((200, 200))
clock = pygame.time.Clock()
FPS = 30  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).

rect = pygame.Rect((0, 0), (32, 32))
image = pygame.Surface((32, 32))
image .fill(WHITE)
env = gym.make("LunarLander-v2")
env.reset()

pressed_keys = []
action = 0
i = 0

while True:
    i += 1
    # clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pressed_keys.append(1)
            elif event.key == pygame.K_RIGHT:
                pressed_keys.append(3)
            elif event.key == pygame.K_UP:
                pressed_keys.append(2)

        elif event.type == pygame.KEYUP:
            action = 0
            if event.key == pygame.K_LEFT:
                pressed_keys.remove(1)
            elif event.key == pygame.K_RIGHT:
                pressed_keys.remove(3)
            elif event.key == pygame.K_UP:
                pressed_keys.remove(2)

    if len(pressed_keys) == 0:
        action = 0
    else:
        action = pressed_keys[i % len(pressed_keys)]
    print(action)


    screen.fill(BLACK)
    screen.blit(image, rect)
    pygame.display.update()  # Or pygame.display.flip()


    done = env.step(action)[2]
    if done:
        env.reset()

    env.render()
