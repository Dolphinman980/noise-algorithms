import pygame
import iterativeAverage
import time
dimensions = [100, 100]

screen = pygame.display.set_mode(dimensions)
clock = pygame.time.Clock()
BG_COLOR = [100, 210, 30]

noises = []

startTime = time.time()
noise = iterativeAverage.ipaNoise(dimensions, 10, 2, 20)
pygame.image.save(noise, "../GreyscaleLarge.png")

noise2 = iterativeAverage.ipaNoise(dimensions, 5, 2, 10)
pygame.image.save(noise2, "../GreyscaleSmall.png")

noise = iterativeAverage.combineNoise(noise, noise2, 0.5)
heights = []
endTime = time.time()

print(f"total time: {(endTime - startTime)}")

biomeTemplate = iterativeAverage.ipaNoise(dimensions, 5, 1, 30)
pygame.image.save(biomeTemplate, "../biomeTemplate.png")

pygame.image.save(noise, "../Greyscale.png")

for i in range(256):
    heights.append(0)

for y in range(noise.get_height()):
    for x in range(noise.get_width()):
        biome = biomeTemplate.get_at([x, y])[0]
        height = noise.get_at([x, y])[0]
        if height <= 120:
            color = [0, 0, height]

        elif biome <= 64:
            color = [height * 0.2, height * 0.65, 0]
        elif biome <= 128:
            color = [height * 0.1, height, height * 0.2]
        elif biome <= 192:
            color = [height * 0, height * 0.95, height * 0.3]
        else:
            color = [height * 0.2, height * 0.99, 0]

        noise.set_at([x, y], color)

#noise = pygame.transform.scale_by(noise, 4)
noises.append(noise)


noiseBG = pygame.Surface([400, 1000], pygame.SRCALPHA)
noiseBG.blit(noise, [0, 0])
pygame.image.save(noiseBG, "../TransparentNoise2.png")


i = 0
for height in heights:
    print(f"{i} count: {height}")
    i += 1
running = True
while running:
    clock.tick(60)
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    #screen.blit(noise, [0, 0])
    i = 0
    for noise in noises:
        screen.blit(noise, [100 * i, 0])
        i += 1

    pygame.display.flip()
