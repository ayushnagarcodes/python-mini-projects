def print_post_card(sub_lists):
    # making the postcard in the form of a string
    string = "-" * 50 + "\n"
    for i in range(1, 29):
        if i == 27:
            string += "|" + " " * 19 + "Merry Xmas" + " " * 19 + "|" + "\n"
        else:
            string += "|" + " " * 48 + "|" + "\n"
    string += "-" * 50

    # adding trees by replacing the spaces in the postcard
    for sub_list in sub_lists:
        width = 51
        height, interval, line, column = sub_list
        string_list = list(string)

        # adding the top part of the tree
        string_list[width * line + column] = "X"
        string_list[width * (line + 1) + column] = "^"

        # adding the mid-part of the tree
        decor_index = 0
        next_decor_index = 1
        i = 2
        while i <= height:
            index = width * (line + i) + column - i + 1
            string_list[index] = "/"
            index += 1

            j = 0
            while j < 2 * (i - 1) - 1:
                if j % 2 == 1:
                    decor_index += 1
                if decor_index == next_decor_index:
                    string_list[index] = "O"
                    next_decor_index += interval
                else:
                    string_list[index] = "*"
                j += 1
                index += 1

            string_list[index] = "\\"
            i += 1

        # adding the bottom part of the tree
        index = width * (line + height + 1) + column
        string_list[index - 1] = "|"
        string_list[index + 1] = "|"

        # joining the list to make a string
        string = "".join(string_list)

    # printing the postcard
    print(string)


def print_tree(height, interval):
    # adding the top part of the tree
    string = " " * (height - 1) + "X"
    string += "\n"
    string += " " * (height - 1) + "^"
    string += "\n"

    # adding the mid-part of the tree
    decor_index = 0
    next_decor_index = 1
    i = 2
    while i <= height:
        string += " " * (height - i) + "/"

        j = 0
        while j < 2 * (i - 1) - 1:
            if j % 2 == 1:
                decor_index += 1
            if decor_index == next_decor_index:
                string += "O"
                next_decor_index += interval
            else:
                string += "*"
            j += 1

        string += "\\"
        string += "\n"
        i += 1

    # adding the bottom part of the tree
    num_spaces = int((2 * height - 4) / 2)
    string += " " * num_spaces + "| |"

    # printing the tree
    print(string)


# start of the program
user_input = input().split()
user_input = [int(x) for x in user_input]
if len(user_input) == 2:
    # printing the tree if only 2 values separated by spaces
    # input format -> height interval
    # Ex: 8 2
    print_tree(user_input[0], user_input[1])
else:
    # printing the post card if no. of values are in multiples of 4 separated by spaces
    # input format -> height1 interval1 line1 column1 height2 interval2 line2 column2 ....
    # Ex: 3 2 9 31 11 3 7 25 5 1 15 35 6 3 15 15
    # the above input will print 4 trees
    sub_input = [user_input[i:i + 4] for i in range(0, len(user_input), 4)]
    print_post_card(sub_input)
