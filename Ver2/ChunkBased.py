import pygame
import random
import math
import time

screenWidth = 100
screenHeight = 100
screen = pygame.display.set_mode([screenWidth, screenHeight])

clock = pygame.time.Clock()

resolution = 1
seaLevel = 125
pointsPerChunk = 2
pointChance = 5 # 1 in X chance for a initial point in a chunk, 1=certain 100 = 1/100 chance
chunkSize = 5 # Ideally a common factor of screen width & screen height, 40 is 64x36 chunks
iterations = screenWidth*screenHeight


# Generate blank chunk
startTime = time.time()

def renderMap(map):
    i = 0
    for chunkPointIndexX in range(len(chunkMap)):
        for chunkPointIndexY in range(len(chunkMap[chunkPointIndexX])):
            for pX in range(len(chunkMap[chunkPointIndexX][chunkPointIndexY])):
                for pY in range(len(chunkMap[chunkPointIndexX][chunkPointIndexY][pX])):
                    if chunkMap[chunkPointIndexX][chunkPointIndexY][pX][pY] != -1:

                        height = chunkMap[chunkPointIndexX][chunkPointIndexY][pX][pY]



                        color = [height, height, height]
                        xCoord = ((chunkPointIndexX) * chunkSize) + pX
                        yCoord = ((chunkPointIndexY) * chunkSize) + pY
                        #print(color)
                        i += 1
                        #print(i)
                        pygame.draw.circle(screen, color, [xCoord, yCoord], resolution)

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
    if -1 in closest_points:
       all_coords.append(coords)
    else:
        chunkMap[cX][cY][pX][pY] = int((closest_points[0] + closest_points[1]) / 2)



chunkMap = resetChunkMap()
print(f"expectedX chunks: {screenWidth / chunkSize}, actual: {len(chunkMap)}")
print(f"expectedX chunks: {screenHeight / chunkSize}, actual: {len(chunkMap[0])}")
generateComplexityPoints(pointsPerChunk)
all_coords = [(cx, cy, px, py) for cx in range(len(chunkMap)) for cy in range(len(chunkMap[0])) for px in range(chunkSize) for py in range(chunkSize)]
random.shuffle(all_coords)

i = 0
for coords in all_coords:
    i += 1
    print(i)
    generatePoint(coords)

print('started')
renderMap(chunkMap)
print('done')
pygame.image.save(screen, f"Unblurred/W{screenWidth}H{screenHeight}C{chunkSize}.png")
smoothedNoise = pygame.Surface([screenWidth, screenHeight])
for y in range(screenHeight):
    for x in range(screenWidth):
        neighbouringPixelTotal = 0
        neighbouringPixels = 0
        for y1 in [-1, 0, 1]:
            for x1 in [-1, 0, 1]:
                try:
                    neighbouringPixelTotal += screen.get_at([x + x1, y + y1])[0]
                    neighbouringPixels += 1
                except IndexError:
                    pass
        heightAvg = int(neighbouringPixelTotal / neighbouringPixels)

        # if heightAvg >= 128:
        #     color = [heightAvg, heightAvg, 0]
        # else:
        #     color = [0, 0, heightAvg]

        color = [heightAvg, heightAvg, heightAvg]

        smoothedNoise.set_at([x, y], color)
screen.blit(smoothedNoise, [0, 0])



pygame.image.save(screen, f"Blurred/W{screenWidth}H{screenHeight}C{chunkSize}.png")
endTime = time.time()
print(f'Total time: {endTime - startTime}')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #print("ello")
    clock.tick()

    pygame.display.flip()
for chunkX in chunkMap:
    for chunkY in chunkX:
        for x in chunkY:
            print(x)
        print('\n')