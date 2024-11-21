import pygame
from scipy.spatial import cKDTree
import random
import time
import math

SEA_LEVEL = 4
STARTING_COMPLEXITY = 550
ITERATIONS = 10000
resolution = 1
SMOOTH_ITERATIONS = 1
screen = pygame.display.set_mode((400, 400))
points = []
clock = pygame.time.Clock()
startTime = time.time()

def getClosestPoints(points, reference_point):
    reference_point_3d = (reference_point[0], reference_point[1], 0)

    tree = cKDTree(points)


    _, closest_indices = tree.query(reference_point_3d, k=3)
    closest_indices = closest_indices[1:]

    return tuple(closest_indices)
def renderPoints(points):
    # Points in the form of (x, y, height)
    for point in points:
        #if len(point) != 3:
           # break
        if point[2] <= SEA_LEVEL:
            color = ((255 / (SEA_LEVEL * 2) * point[2]), (255 / (SEA_LEVEL * 2) * point[2]), 255)
        else:
            color = [int(255 / 13 * point[2]), 255, int(255 / 13 * point[2])]

       # print(height)
        pygame.draw.circle(screen, color, [point[0], point[1]], resolution)

for i in range(0, STARTING_COMPLEXITY):
    points.append((random.randrange(0, screen.get_width()), random.randrange(0, screen.get_height()), random.randrange(0, 11)))

def createPoint():
    newPoint = ([random.randrange(0, screen.get_width()), random.randrange(0, screen.get_height())])
    closestPoints = getClosestPoints(points, newPoint)
    height = (points[closestPoints[0]][2] + points[closestPoints[1]][2]) / 2
    #print(closestPoints)
    #print(height)
    newPoint.append(int(height))
    points.append(tuple(newPoint))

for i in range(ITERATIONS + 1):
    print(i)
    createPoint()

def read_file_to_tuples(file_path):
    tuples_list = []
    with open(file_path, 'r') as file:
        for line in file:
            # Remove leading/trailing whitespace and split by commas
            values = line.strip().split(',')
            # Convert values to integers and create a tuple
            values_tuple = tuple(map(int, values))
            # Append the tuple to the list
            tuples_list.append(values_tuple)
    return tuples_list





endTime = time.time()
running = True
while running:
    screen.fill([0, 0, 0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_EQUALS]:
        if SEA_LEVEL < 10:
            SEA_LEVEL += 1
    if keys[pygame.K_MINUS]:
        if SEA_LEVEL > 1:
            SEA_LEVEL -= 1
    if keys[pygame.K_UP]:
        resolution += 1
    if keys[pygame.K_DOWN]:
        resolution -= 1
    #print(SEA_LEVEL)


    renderPoints(points)
    pygame.display.flip()




f = open("saved1.txt", "w")

print(endTime - startTime)