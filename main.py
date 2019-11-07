import random
import math
import csv
import json

numb_of_turns = 50
numb_of_sheeps = 15
init_pos_limit = 10
sheep_move_dist = 0.5
wolf_move_dist = 1
sheeps = []
wolf = []


def find_nearest_point():
    distances = []
    for i in range(len(sheeps)):
        if sheeps[i] is not None:
            distances.append(math.sqrt((wolf[0][0] - sheeps[i][0]) ** 2 + (wolf[0][1] - sheeps[i][1]) ** 2))
        else:
            distances.append(None)
    return sheeps[distances.index(min(dis for dis in distances if dis is not None))]


def create_sheeps():
    for i in range(numb_of_sheeps):
        # musi być włącznie
        sheeps.append([random.uniform(-10.0, 10.0), random.uniform(-10.0, 10.0), i + 1])


def create_wolf():
    wolf.append([0.0, 0.0])


def move_sheeps():
    direction = [-1, 1]
    for i in range(len(sheeps)):
        if sheeps[i] is not None:
            sheeps[i][random.randrange(2)] += (direction[random.randrange(2)] * sheep_move_dist)


def move_wolf():
    closest_sheep = find_nearest_point()
    dist_to_closest_sheep = math.sqrt((wolf[0][0] - closest_sheep[0]) ** 2 + (wolf[0][1] - closest_sheep[1]) ** 2)
    if dist_to_closest_sheep < wolf_move_dist:
        print("Sheep {} has been eaten!".format(closest_sheep[2]))
        sheeps[sheeps.index(closest_sheep)] = None
        global numb_of_sheeps
        numb_of_sheeps -= 1
    else:
        wolf[0][0] = wolf[0][0] - ((wolf_move_dist * (wolf[0][0] - closest_sheep[0])) / dist_to_closest_sheep)
        wolf[0][1] = wolf[0][1] - ((wolf_move_dist * (wolf[0][1] - closest_sheep[1])) / dist_to_closest_sheep)


def show_sheeps():
    for i in range(numb_of_sheeps):
        print(sheeps[i])


if __name__ == '__main__':
    create_sheeps()
    create_wolf()
    alive_file = open('alive.csv', 'w+')
    pos_file = open('pos.json', 'w+')
    alive_writer = csv.writer(alive_file, delimiter=',')
    pos_file.write('[')

    for i in range(numb_of_turns):
        move_sheeps()
        move_wolf()
        print("Turn number: {}".format(i + 1))
        print("Number of sheeps: {}".format(numb_of_sheeps))
        print("Current wolf position: x={:.3f} y={:.3f}".format(wolf[0][0], wolf[0][1]))
        alive_writer.writerow([i + 1, numb_of_sheeps])
        if numb_of_sheeps == 0:
            break

        sheeps_json = []
        for j in range(len(sheeps)):
            if sheeps[j] is not None:
                sheeps_json.append([sheeps[j][0], sheeps[j][1]])
            else:
                sheeps_json.append(None)

        round_dict = {
            'round_no': i + 1,
            'wolf_pos': wolf[0],
            'sheep_pos': sheeps_json}

        json.dump(round_dict, pos_file)
        if i != numb_of_turns-1:
            pos_file.write(',\n')
    pos_file.write(']')
    pos_file.close()
    alive_file.close()



