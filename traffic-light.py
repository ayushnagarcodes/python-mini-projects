import os
import time
from threading import Thread


user_input = None
close_timer = False
second = 0
# format of queue list: [[road_name, is_open, timer], [...], [...]]
queue = []


def check_input(var, message):
    while True:
        try:
            var = int(var)
        except ValueError:
            var = input(f"{message}")
        else:
            return var


def clear_terminal():
    global user_input
    user_input = input()
    os.system('cls' if os.name == 'nt' else 'clear')


def find_open_road(queue_list):
    for i in range(len(queue_list)):
        if queue_list[i][1]:
            return i


def adjust_timer_before():
    global queue
    index_open_road = find_open_road(queue)
    if index_open_road:
        j = index_open_road - 1
        while j >= 0:
            # for first iteration (that is for the item just before open road item)
            if j == index_open_road - 1:
                queue[j][2] = (len(queue) - 1) * intervals - intervals + queue[index_open_road][2]
            # for further iterations (except first)
            else:
                queue[j][2] = queue[j + 1][2] - intervals
            j -= 1


def system_state(num_road, num_interval):
    global second
    while not close_timer:
        # decreasing timer in queue items
        for i in range(len(queue)):
            queue[i][2] -= 1
            if queue[i][2] == 0:
                if queue[i][1]:
                    if len(queue) == 1:
                        queue[i][2] = num_interval
                    else:
                        queue[i][2] = (len(queue) - 1) * num_interval
                        queue[i][1] = False
                else:
                    queue[i][2] = num_interval
                    queue[i][1] = True

        time.sleep(1)
        second += 1

        if user_input == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"! {second}s. have passed since system startup !")
            print(f"! Number of roads: {num_road} !")
            print(f"! Interval: {num_interval} !")
            print()
            for road_obj in queue:
                if road_obj[1]:
                    print(f"{road_obj[0]} is \u001B[32mopen for {road_obj[2]}s.\u001B[0m")
                else:
                    print(f"{road_obj[0]} is \u001B[31mclosed for {road_obj[2]}s.\u001B[0m")
            print()
            print('! Press "Enter" to open menu !')


print("Welcome to the traffic management system!")

num_roads = input("Input the number of roads: ")
num_roads = check_input(num_roads, "Incorrect input. Try again: ")
while num_roads <= 0:
    num_roads = input("Incorrect input. Try again: ")
    num_roads = check_input(num_roads, "Incorrect input. Try again: ")

intervals = input("Input the interval: ")
intervals = check_input(intervals, "Incorrect input. Try again: ")
while intervals <= 0:
    intervals = input("Incorrect input. Try again: ")
    intervals = check_input(intervals, "Incorrect input. Try again: ")


t = Thread(target=system_state, name="QueueThread", args=(num_roads, intervals))
t.start()
os.system('cls' if os.name == 'nt' else 'clear')

while True:
    print("Menu:")
    print("1. Add road")
    print("2. Delete road")
    print("3. Open system")
    print("0. Quit")
    user_input = input()
    try:
        user_input = int(user_input)
    except ValueError:
        print("Incorrect option")
        clear_terminal()
        continue

    if user_input == 0:
        print("Bye!")
        close_timer = True
        break
    elif user_input == 1:
        user_input = input("Input road name: ")
        if len(queue) == num_roads:
            print("Queue is full!")
        else:
            if len(queue) == 0:
                queue.append([user_input, True, intervals])
            else:
                # re-balancing timer in queue items that appear after "open" road item
                if queue[-1][1]:
                    queue.append([user_input, False, queue[-1][2]])
                else:
                    queue.append([user_input, False, queue[-1][2] + int(intervals)])

                # re-balancing timer in queue items that appear before open road item
                adjust_timer_before()
            print(f"{user_input} Added!")
        clear_terminal()
    elif user_input == 2:
        if len(queue) == 0:
            print("Queue is empty!")
        else:
            print(queue[0][0] + " deleted!")
            queue.pop(0)

            # re-balancing timer in queue items that appear before "open" road item
            adjust_timer_before()
        clear_terminal()
    elif user_input == 3:
        clear_terminal()
    else:
        print("Incorrect option")
        clear_terminal()
