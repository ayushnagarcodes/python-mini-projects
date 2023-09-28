import re

# course data format ->
# [course_available, num_enrolled, num_submissions, average_grade, completion score]
course_data = [["Python", "DSA", "Databases", "Flask"], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [600, 400, 480, 550]]

# students dictionary format ->
# {user_id : [first_name, last_name, email, points (in each course), completion (in each course)]}
students = {}
key_num = 1000

# list of students that have completed a course and needs to be notified
# notify_users list format -> [[user_id_1, course_index_1], [user_id_1, course_index_2], [user_id_2, course_index_1]]
notify_users = []
# list of students that have completed a course and have already been notified
notified_users = []


def check_string(string):
    if re.match("^[a-zA-Z]+(['-]?[a-zA-Z]+)*['-]?[a-zA-Z]+$", string) is None or len(string) < 2:
        return False
    return True


def check_email(string):
    if string.count("@") != 1 or string.count(".") < 1:
        return "Incorrect email"
    for value in students.values():
        if value[2] == string:
            return "This email is already taken"
    return False


def check_credentials(string):
    global key_num
    input_list = string.split()
    # input_list format -> [first_name, last_name, email]
    if len(input_list) >= 3:
        first_name = input_list[0]
        last_name = input_list[1:-1]
        email = input_list[-1]

        if not check_string(first_name):
            return "Incorrect first name"

        for word in last_name:
            if not check_string(word):
                return "Incorrect last name"

        email_status = check_email(email)
        if email_status:
            return email_status
        else:
            # adding student to the database + assigning unique id + appending empty points list for the courses
            students[key_num] = [first_name, last_name, email, [0, 0, 0, 0], [0, 0, 0, 0]]
            key_num += 1
            return "correct"

    return "Incorrect credentials"


def add_students():
    students_added = 0
    print("Enter student credentials or 'back' to return:\n(first_name last_name email)")
    while True:
        user_input_2 = input()
        if user_input_2 == "back":
            print(f'Total {students_added} students have been added.')
            break
        else:
            status = check_credentials(user_input_2)
            if status == "correct":
                students_added += 1
                print("The student has been added.")
            else:
                print(status)


def check_points(string):
    input_list = string.split()
    # input_list format -> [user_id, points_python, points_dsa, points_databases, points_flask]
    if len(input_list) == 5:
        # checking whether id is an integer or not
        try:
            user_id = int(input_list[0])
        except ValueError:
            return f'No student is found for id={input_list[0]}'

        # checking whether id exists in database
        if user_id not in students:
            return f'No student is found for id={user_id}'

        points_list = input_list[1:]
        # checking whether points are integers > 0 or not
        for obj in points_list:
            try:
                if float(obj) % 1 != 0 or float(obj) < 0:
                    return "Incorrect points format"
            except ValueError:
                return "Incorrect points format"

        # updating course and student data
        # no. of courses = 4 -> i.e. range(0, 4)
        for i in range(0, 4):
            # updating enrollments
            if students[user_id][3][i] == 0 and int(points_list[i]) > 0:
                course_data[1][i] += 1
            # updating submissions
            if int(points_list[i]) > 0:
                course_data[2][i] += 1

            # adding points to the points list in students dictionary with the corresponding id
            students[user_id][3][i] += int(points_list[i])

            # updating average
            # average of a subject = sum of scores of all students in that subject / total no. of submissions in that subject
            if course_data[2][i]:
                course_data[3][i] = 0
                for value in students.values():
                    course_data[3][i] += value[3][i]
                course_data[3][i] /= course_data[2][i]

            if int(points_list[i]) > 0:
                # updating completion percentage
                # (user_points / completion_score) * 100
                students[user_id][4][i] = round((students[user_id][3][i] / course_data[4][i]) * 100, 1)

                # updating notify_users list
                # checking whether user has completed the course or not
                if [user_id, i] not in notified_users and students[user_id][3][i] >= course_data[4][i]:
                    notify_users.append([user_id, i])

        return "correct"

    return "Incorrect points format"


def add_points():
    print("Enter an id and points or 'back' to return:\n(student_id course_1 course_2 course_3 course_4)")
    while True:
        user_input_3 = input()
        if user_input_3 == "back":
            break
        else:
            status = check_points(user_input_3)
            if status == "correct":
                print("Points updated")
            else:
                print(status)


def get_student_data():
    print("Enter an id or 'back' to return:")
    while True:
        user_input_4 = input()
        if user_input_4 == "back":
            break

        # checking whether input is an integer or not
        try:
            if float(user_input_4) in students:
                points_list = students[float(user_input_4)][3]
                print(f'{user_input_4} points: Python={points_list[0]}; DSA={points_list[1]}; Databases={points_list[2]}; Flask={points_list[3]}')
            else:
                print(f'No student is found for id={user_input_4}')
        except ValueError:
            print(f'No student is found for id={user_input_4}')


def get_values(list1, max_value, min_value, field1, field2):
    max_indexes = []
    for i in range(len(list1)):
        if list1[i] == max_value:
            max_indexes.append(i)
    result_max = ", ".join([course_data[0][x] for x in max_indexes])

    min_indexes = []
    for i in range(len(list1)):
        if list1[i] == min_value:
            min_indexes.append(i)
    min_indexes = [x for x in min_indexes if x not in max_indexes]
    if min_indexes:
        result_min = ", ".join([course_data[0][x] for x in min_indexes])
    else:
        result_min = "n/a"

    return f'''{field1}: {result_max}
{field2}: {result_min}'''


def show_stats():
    print("Type the name of a course to see details or 'back' to quit:")
    if key_num == 1000:
        print('''Most popular: n/a
Least popular: n/a
Highest activity: n/a
Lowest activity: n/a
Easiest course: n/a
Hardest course: n/a''')
    else:
        print(f'''{get_values(course_data[1], max(course_data[1]), min(course_data[1]), "Most popular", "Least popular")}
{get_values(course_data[2], max(course_data[2]), min(course_data[2]), "Highest activity", "Lowest activity")}
{get_values(course_data[3], max(course_data[3]), min(course_data[3]), "Easiest course", "Hardest course")}''')

    while True:
        user_input_5 = input()
        if user_input_5 == "back":
            break

        match = [x for x in course_data[0] if x.lower() == user_input_5.lower()]
        if len(match) == 0:
            print("Unknown course")
        else:
            print(match[0])
            print("id\t\tpoints\t\tcompleted")
            index = course_data[0].index(match[0])
            temp_list = []
            if course_data[1][index]:
                for key1, value in students.items():
                    points = value[3][index]
                    if points > 0:
                        temp_list.append([key1, points, value[4][index]])
            if temp_list:
                temp_list.sort(key=lambda x: (x[1], -x[0]), reverse=True)
                for i in range(1, len(temp_list)):
                    if temp_list[i][1] == temp_list[i - 1][1] and temp_list[i][0] < temp_list[i - 1][0]:
                        temp_list[i], temp_list[i - 1] = temp_list[i - 1], temp_list[i]
                temp_list = [[str(val) + "%" if idx == 2 else str(val) for idx, val in enumerate(sub_list)] for sub_list in temp_list]
                temp_list = ["\t\t".join(x) for x in temp_list]
                print("\n".join(temp_list))


def notify():
    temp = []
    for obj in notify_users:
        full_name = students[obj[0]][0] + " " + " ".join(students[obj[0]][1])
        print(f'''To: {students[obj[0]][2]}
Re: Your Learning Progress
Hello, {full_name}! You have accomplished our {course_data[0][obj[1]]} course!''')
        notified_users.append(obj)
        # finding unique students
        if obj[0] not in temp:
            temp.append(obj[0])

    print(f'Total {len(temp)} students have been notified.')
    notify_users.clear()


print("Learning Progress Tracker")
while True:
    user_input = input(f'''
Commands:-
1. add students
2. list
3. add points
4. find
5. statistics
6. notify
7. back
8. exit

Enter your input: ''')
    if user_input == "exit":
        print("Bye!")
        break
    elif not user_input or not user_input.strip():
        print("No input")
    elif user_input == "add students":
        add_students()
    elif user_input == "back":
        print("Enter 'exit' to exit the program")
    elif user_input == "list":
        if len(students) > 0:
            print("Student's IDs:")
            for key in students:
                print(key)
        else:
            print("No students found")
    elif user_input == "add points":
        add_points()
    elif user_input == "find":
        get_student_data()
    elif user_input == "statistics":
        show_stats()
    elif user_input == "notify":
        notify()
    else:
        print("Unknown command!")
