import pygame
import random
import math
import time

screenWidth = 256 * 3
screenHeight = 144 * 3
screen = pygame.display.set_mode([screenWidth, screenHeight])

clock = pygame.time.Clock()

resolution = 1
seaLevel = 125
pointsPerChunk = 10
pointChance = 3 # 1 in X chance for a initial point in a chunk, 1=certain 100 = 1/100 chance
chunkSize = 10 # Ideally a common factor of screen width & screen height, 40 is 64x36 chunks
iterations = screenWidth*screenHeight


# Generate blank chunk
startTime = time.time()



def resetChunkMap():
    global chunkMap
    chunkMap = []
    for chunkX in range(0, int(screenWidth / chunkSize)):
        chunkMap.append([])
        for chunkY in range(0, int(screenHeight / chunkSize)):
            chunkMap[chunkX].append([])
            for x in range(chunkSize + 1):
                chunkMap[chunkX][chunkY].append([])
                for y in range(chunkSize + 1):
                    chunkMap[chunkX][chunkY][x].append(-1)
    return chunkMap
# Creates a chunkmap that allows reference of a specific spot via chunkMap[chunkX][chunkY][x][y]

def generateComplexityPoints(pointsPerChunk):
    global chunkMap
    for chunkX in range(len(chunkMap)):
        for chunkY in range(len(chunkMap[chunkX])):
            for point in range(pointsPerChunk):
                if random.randrange(pointChance) == 1:
                    chunkMap[chunkX][chunkY][random.randrange(chunkSize + 1)][random.randrange(chunkSize + 1)] = random.randrange(0, 256)


def generatePoint(coords):
    global chunkMap
    cX, cY, pX, pY = coords
    closest_points = [-1, -1]
    min_distance = float('inf')

    for dx in [1, -1, 0]:
        for dy in [1, -1, 0]:
            if len(chunkMap) > dx + cX > 0 and len(chunkMap[0]) > dy + cY > 0:
                chunk = chunkMap[cX + dx][cY + dy]
                for x2 in range(len(chunk)):
                    if dx == -1:
                        distanceX = (chunkSize - x2 + pX + 1)
                    elif dx == 1:
                        distanceX = (chunkSize - pX + x2 + 1)
                    else:
                        distanceX = x2 - pX
                    for y2 in range(len(chunk[0])):
                        if chunk[x2][y2] != -1:
                            if dy == -1:
                                distanceY = (chunkSize - y2 + pY + 1)
                            elif dy == 1:
                                distanceY = (chunkSize - pY + y2 + 1)
                            else:
                                distanceY = y2 - pY
                            distance = math.sqrt(distanceX**2 + distanceY**2) + random.uniform(-1.00, 1.00)
                            if distance <= min_distance:
                                min_distance = distance
                                closest_points[1] = closest_points[0]
                                closest_points[0] = chunk[x2][y2]
    chunkMap[cX][cY][pX][pY] = int((closest_points[0] + closest_points[1]) / 2)



chunkMap = resetChunkMap()

generateComplexityPoints(pointsPerChunk)
all_coords = [(cx, cy, px, py) for cx in range(len(chunkMap)) for cy in range(len(chunkMap[0])) for px in range(chunkSize) for py in range(chunkSize)]
random.shuffle(all_coords)



print('started')






pygame.image.save(screen, f"Blurred/W{screenWidth}H{screenHeight}C{chunkSize}.png")
endTime = time.time()
print(f'Total time: {endTime - startTime}')
i = 0
blurring = False
running = True
finished = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if not blurring:
        try:
            generatePoint(all_coords[i])
        except IndexError:
            screenCopy = screen
            blurring = True
            i = 0

    if not blurring:

        cx, cy, px, py = all_coords[i]
        absX = cx * chunkSize + px
        absY = cy * chunkSize + py
        height = chunkMap[cx][cy][px][py]
        color = [height, height, height]
        screen.set_at([absX, absY], color)
    else:
        try:
            cx, cy, px, py = all_coords[i]
        except IndexError:
            finished = True
            pass
        x = cx * chunkSize + px
        y = cy * chunkSize + py
        neighbouringPixelTotal = 0
        neighbouringPixels = 0
        for y1 in [-1, 0, 1]:
            for x1 in [-1, 0, 1]:
                try:
                    neighbouringPixelTotal += screenCopy.get_at([x + x1, y + y1])[0]
                    neighbouringPixels += 1
                except IndexError:
                    pass
        heightAvg = int(neighbouringPixelTotal / neighbouringPixels)

        if heightAvg >= 128:
            color = [heightAvg, heightAvg, 0]
        else:
            color = [0, 0, heightAvg]

        screen.set_at([x, y], color)
    if not finished:
        i += 1
    clock.tick()

    pygame.display.flip()

print('done')
pygame.image.save(screen, f"Unblurred/W{screenWidth}H{screenHeight}C{chunkSize}.png")
smoothedNoise = pygame.Surface([screenWidth, screenHeight])