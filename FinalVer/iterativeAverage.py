# MIT License
#
# Copyright (c) 2024 Toby Felton McMahon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import math
import random
import pygame


def combineNoise(baseNoise, addedNoise, addedWeight):
    baseWidth = baseNoise.get_width()
    baseHeight = baseNoise.get_height()

    newNoise = pygame.Surface([baseWidth, baseHeight])

    for y in range(baseHeight):
        for x in range(baseWidth):
            basePixelValue = baseNoise.get_at([x, y])[0]
            addedPixelValue = addedNoise.get_at([x, y])[0]
            heightDif = basePixelValue - addedPixelValue
            newHeight = basePixelValue + int(heightDif * addedWeight)
            newHeight = min(255, max(0, newHeight))
            newNoise.set_at([x, y], (newHeight, newHeight, newHeight))

    return newNoise


def ipaNoise(dimensions, chunkSize, pointsPerChunk, pointChance):

    chunkMap = resetChunkMap(dimensions, chunkSize)
    generateComplexityPoints(pointsPerChunk, chunkMap, chunkSize, pointChance)

    all_coords = [(cx, cy, px, py) for cx in range(len(chunkMap)) for cy in range(len(chunkMap[0])) for px in
                  range(chunkSize) for py in range(chunkSize)]
    random.shuffle(all_coords)

    i = 0
    for coords in all_coords:
        i += 1
        generatePoint(coords, chunkMap, all_coords, chunkSize)

    noise = renderMap(chunkMap, dimensions, chunkSize)

    smoothedNoise = pygame.Surface(dimensions)
    for y in range(dimensions[1]):
        for x in range(dimensions[0]):
            neighbouringPixelTotal = 0
            neighbouringPixels = 0
            for y1 in [-1, 0, 1]:
                for x1 in [-1, 0, 1]:
                    try:
                        neighbouringPixelTotal += noise.get_at([x + x1, y + y1])[0]
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
    noise = smoothedNoise
    return noise


def renderMap(chunkMap, dimensions, chunkSize):
    i = 0
    noise = pygame.Surface(dimensions)
    for chunkPointIndexX in range(len(chunkMap)):
        for chunkPointIndexY in range(len(chunkMap[chunkPointIndexX])):
            for pX in range(len(chunkMap[chunkPointIndexX][chunkPointIndexY])):
                for pY in range(len(chunkMap[chunkPointIndexX][chunkPointIndexY][pX])):
                    if chunkMap[chunkPointIndexX][chunkPointIndexY][pX][pY] != -1:

                        height = chunkMap[chunkPointIndexX][chunkPointIndexY][pX][pY]



                        color = [height, height, height]
                        xCoord = ((chunkPointIndexX) * chunkSize) + pX
                        yCoord = ((chunkPointIndexY) * chunkSize) + pY
                        i += 1
                        noise.set_at([xCoord, yCoord], color)
    return noise


def resetChunkMap(dimensions, chunkSize):
    global chunkMap
    chunkMap = []
    for chunkX in range(0, int(dimensions[0] / chunkSize)):
        chunkMap.append([])
        for chunkY in range(0, int(dimensions[1] / chunkSize)):
            chunkMap[chunkX].append([])
            for x in range(chunkSize + 1):
                chunkMap[chunkX][chunkY].append([])
                for y in range(chunkSize + 1):
                    chunkMap[chunkX][chunkY][x].append(-1)
    return chunkMap


def generateComplexityPoints(pointsPerChunk, chunkMap, chunkSize, pointChance):

    for chunkX in range(len(chunkMap)):
        for chunkY in range(len(chunkMap[chunkX])):
            for point in range(pointsPerChunk):
                if random.randrange(pointChance) == 1:
                    chunkMap[chunkX][chunkY][random.randrange(chunkSize + 1)][random.randrange(chunkSize + 1)] = random.randrange(0, 256)


def generatePoint(coords, chunkMap, allCoords, chunkSize):
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
       allCoords.append(coords)
    else:
        chunkMap[cX][cY][pX][pY] = int((closest_points[0] + closest_points[1]) / 2)


    