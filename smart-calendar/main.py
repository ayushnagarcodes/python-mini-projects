import datetime
import re


notes_file = './notes.txt'
birthdates_file = './birthdates.txt'
user_datetime_obj = None
temp_date = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d") + " 00:00", "%Y-%m-%d %H:%M")
text = None


def read_file(file_name):
    file = open(file_name, 'r')
    file_list = file.readlines()
    file.close()
    return file_list


def write_file(file_name, data):
    file = open(file_name, 'a')
    file.write(data + '\n\n')
    file.close()


def check_date_time(index, string):
    global user_datetime_obj
    while True:
        continue_loop = False
        date_time = input(string.replace("#", f'#{index + 1}'))

        # splitting user string at "-", ":" and " "
        split_date_time = re.split("[-: ]", date_time)
        # iterating to search whether it contains non-digit characters
        # if yes, then skipping the current cycle of the while loop using continueLoop variable
        for item in split_date_time:
            if re.search('\D', item):
                print("Incorrect format. Please try again (use the format «YYYY-MM-DD HH:MM»):")
                continue_loop = True
                break
        if continue_loop:
            continue

        # adding defaults (hour = 00 and minutes = 00) in case of birthdates
        if len(split_date_time) == 3:
            split_date_time.extend(["00", "00"])
            date_time += " 00:00"

        # checking for correct values of month, hour and minute
        if 1 > int(split_date_time[1]) or int(split_date_time[1]) > 12:
            print("Incorrect format. Please try again (use the format «YYYY-MM-DD HH:MM»):")
            print("Incorrect month value. The month should be in 1-12.")
            continue_loop = True
        if 0 > int(split_date_time[3]) or int(split_date_time[3]) > 23:
            print("Incorrect hour value. The hour should be in 00-23.")
            continue_loop = True
        if 0 > int(split_date_time[4]) or int(split_date_time[4]) > 59:
            print("Incorrect minute value. The minutes should be in 00-59.")
            continue_loop = True
        if continue_loop:
            continue

        # checking for correct format «YYYY-MM-DD HH:MM»
        # also checking for correct values of day (so that "2023-02-31" doesn't pass) and year (so that year is not empty)
        try:
            user_datetime_obj = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Incorrect format. Please try again (use the format «YYYY-MM-DD HH:MM»):")
            continue

        break


def search_text(data_list, user_input):
    index_list = []
    index = 0
    while index < len(data_list):
        if re.search(user_input, data_list[index], flags=re.IGNORECASE):
            index_list.append(index)
        index += 2
    return index_list


def add_notes():
    global text
    num_notes = int(input("\nHow many notes do you want to add?\n"))
    # adding note + checking datetime format of user input
    for i in range(num_notes):
        notes_string = f"\nEnter date and time of note # (in format «YYYY-MM-DD HH:MM»):\n"
        check_date_time(i, notes_string)
        text = input(f"Enter text of note #{i + 1}:\n")

        # calculating time left for the event from now
        difference = user_datetime_obj - datetime.datetime.now()
        display_event = f'Before the event note "{text}" remains: {difference.days} day(s), {difference.seconds // 3600} hour(s) and {difference.seconds // 60 % 60} minute(s)'

        write_file(notes_file, display_event)
    print("\nNotes added!\n")


def add_birthdays():
    num_birthdates = int(input("\nHow many dates of birth do you want to add?\n"))
    # adding birthdate + checking datetime format of user input
    for i in range(num_birthdates):
        name = input(f"\nEnter the name of #{i + 1}:\n")
        birthdates_string = f"Enter the date of birth of # (in format «YYYY-MM-DD»):\n"
        check_date_time(i, birthdates_string)

        # calculating time left for the event from now
        next_birthday = datetime.datetime.strptime(str(temp_date.year) + '-' + user_datetime_obj.strftime("%m-%d %H:%M"),
                                                   "%Y-%m-%d %H:%M")
        if next_birthday < temp_date:
            next_birthday = datetime.datetime.strptime(
                str(temp_date.year + 1) + '-' + user_datetime_obj.strftime("%m-%d %H:%M"), "%Y-%m-%d %H:%M")
        difference = next_birthday - temp_date

        message = None
        if difference.days == 0:
            message = "today"
        elif difference.days == 1:
            message = "tomorrow"
        else:
            message = f"in {difference.days} days"
        display_event = f'{name}’s birthday is {message}. He (she) turns {(next_birthday - user_datetime_obj).days // 365} years old.'

        write_file(birthdates_file, display_event)
        print("\nBirthdates added!\n")


def view_date():
    global user_datetime_obj
    while True:
        user_input = input("\nEnter date: (in format «YYYY-MM-DD):\n")
        split_date_time = re.split("[-: ]", user_input)

        # adding defaults (hour = 00 and minutes = 00) in case of birthdates
        if len(split_date_time) == 3:
            split_date_time.extend(["00", "00"])
            user_input += " 00:00"

        # checking for correct format «YYYY-MM-DD HH:MM»
        try:
            user_datetime_obj = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Incorrect format. Please try again (use the format «YYYY-MM-DD HH:MM»):")
            continue
        else:
            break

    count_notes = 0
    count_birthdates = 0
    # 1st list inside events_list is for notes and the 2nd one is for birthdates
    events_list = [[], []]

    # First, searching "date" in notes_file
    file_list_notes = read_file(notes_file)
    i = 0
    while i < len(file_list_notes):
        if "today" in file_list_notes[i]:
            required_date = datetime.datetime.now()
        elif "tomorrow" in file_list_notes[i]:
            required_date = datetime.datetime.now() + datetime.timedelta(days=1)
        else:
            split_date = [int(x) for x in
                          re.split(": | day\(s\), | hour\(s\) and | minute\(s\)\n", file_list_notes[i])[1:-1]]
            required_date = datetime.datetime.now() + datetime.timedelta(days=split_date[0], hours=split_date[1],
                                                                      minutes=split_date[2])
        if required_date.date() == user_datetime_obj.date():
            count_notes += 1
            events_list[0].append(i)
        i += 2

    # Now, searching "date" in birthdates_file
    file_list_birthdates = read_file(birthdates_file)
    j = 0
    while j < len(file_list_birthdates):
        if "today" in file_list_birthdates[j]:
            required_date = datetime.datetime.now()
        elif "tomorrow" in file_list_birthdates[j]:
            required_date = datetime.datetime.now() + datetime.timedelta(days=1)
        else:
            split_date = [int(x) for x in
                          re.split("is in | days. He \(she\) turns", file_list_birthdates[j])[1:-1]]
            required_date = datetime.datetime.now() + datetime.timedelta(days=split_date[0])
        if required_date.date() == user_datetime_obj.date():
            count_birthdates += 1
            events_list[1].append(j)
        j += 2

    # displaying results
    print(f"\nFound {count_notes} note(s) and {count_birthdates} date(s) of birth on this date:\n")
    for note_index in events_list[0]:
        print(file_list_notes[note_index])
    for birthdate_index in events_list[1]:
        print(file_list_birthdates[birthdate_index])

    return events_list, file_list_notes, file_list_birthdates


def view_note():
    user_input = input("Enter text of note:\n")

    file_list = read_file(notes_file)

    result = search_text(file_list, user_input)

    while len(result) == 0:
        user_input = input("No such note found. Try again:\n")
        result = search_text(file_list, user_input)

    # displaying results
    print(f'\nFound {len(result)} note(s) that contain "{user_input}":\n')
    for i in range(len(result)):
        print(file_list[result[i]])

    return result, file_list


def view_name():
    user_input = input("Enter name:\n")

    file_list = read_file(birthdates_file)

    result = search_text(file_list, user_input)

    while len(result) == 0:
        user_input = input("No such person found. Try again:\n")
        result = search_text(file_list, user_input)

    # displaying results
    print(f"\nFound {len(result)} date of birth:\n")
    for i in range(len(result)):
        print(file_list[result[i]])

    return result, file_list


def delete_event(index_list, file_list, file_name, pattern, string):
    for index in index_list:
        temp_text = '"' + re.search(pattern, file_list[index]).group(1).strip() + '"'
        user_input = input(
            f'Are you sure you want to delete {temp_text}? (yes, no)\n')
        if user_input == "yes":
            del file_list[index:index + 2]
            file = open(file_name, 'w')
            file.writelines(file_list)
            file.close()
            print(f'{string} deleted!')
        elif user_input == "no":
            print("Deletion canceled.")


# Main Program
print('Current date and time:')
print(datetime.datetime.now())
while True:
    user_input = input("\nEnter the command (add, view, delete, exit):\n")
    if user_input == "add":
        while True:
            user_input = input("\nWhat do you want to add (note, birthday)?\n")
            if user_input == "note":
                add_notes()
                break
            elif user_input == "birthday":
                add_birthdays()
                break
            else:
                print("This command is not in the menu")
    elif user_input == "view":
        while True:
            user_input = input("\nWhat do you want to view? (date, note, name)?\n")
            if user_input == "date":
                view_date()
                break
            elif user_input == "note":
                view_note()
                break
            elif user_input == "name":
                view_name()
                break
            else:
                print("This command is not in the menu")
    elif user_input == "delete":
        while True:
            user_input = input("\nWhat do you want to delete (date, note, name)?\n")
            if user_input == "date":
                index_list, file_list_notes, file_list_birthdates = view_date()
                delete_event(index_list[0], file_list_notes, notes_file, r'"([^"]*)"', "Note")
                delete_event(index_list[1], file_list_birthdates, birthdates_file, r'(.+?).s birthday', "Birthdate")
                break
            elif user_input == "note":
                index_list, file_list_notes = view_note()
                delete_event(index_list, file_list_notes, notes_file, r'"([^"]*)"', "Note")
                break
            elif user_input == "name":
                index_list, file_list_birthdates = view_name()
                delete_event(index_list, file_list_birthdates, birthdates_file, r'(.+?).s birthday', "Birthdate")
                break
            else:
                print("This command is not in the menu")
    elif user_input == "exit":
        exit()
    else:
        print("This command is not in the menu")
