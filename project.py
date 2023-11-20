from sys import argv, exit
from csv import DictWriter, DictReader, reader
from tabulate import tabulate
import os
os.system("cls")


def main():
   
    if command_line_args() == 'default':
        mainMenu()
    if command_line_args() == 'open' or command_line_args() == 'default':
        if command_line_args() == 'open':
            while True:
                try:
                    displayTasks()
                    break
                except FileNotFoundError:
                    with open("todolist.csv", "w", newline="") as file:
                        writer = DictWriter(file, fieldnames=["id","task","status"])
                        writer.writeheader()
        while True:
            try:
                tasksArr = read()
                userInput = input("Add new task: ")
                if "-e" in userInput:
                    update(userInput)
                    displayTasks()
                elif "* -d" in userInput:
                    deleteAll()
                    displayTasks()
                elif "-d" in userInput:
                    delete(userInput)
                    displayTasks()
                elif "-c" in userInput:
                    changeStatus(tasksArr, userInput)
                    displayTasks()
                elif "-p" in userInput:
                    changeStatus(tasksArr, userInput)
                    displayTasks()
                elif "-o" in userInput:
                    displayTasks()
                elif "-i" in userInput:
                    mainMenu()
                elif "-q" in userInput:
                    exit()
                else:
                    write(tasksArr, userInput)
                    displayTasks()
            except FileNotFoundError:
                with open("todolist.csv", "w", newline="") as file:
                    writer = DictWriter(file, fieldnames=["id","task","status"])
                    writer.writeheader()
            except  ValueError as err:
                print(err)
            except KeyboardInterrupt:
                exit()
    userInput = input("Add new task: ")
    changeStatus(userInput)

# done
def displayTasks():
    tasksArr = read()
    tasks = []
    try:
        if tasksArr[0][0] == 'You have no tasks.':
            return print(tabulate(tasksArr, tablefmt="simple_grid"))
    except:
        for i in tasksArr:
            tasks.append([i["id"],i["task"], i["status"]])
        return print(tabulate(tasks, headers=['ID', 'Task', "Status"], tablefmt="simple_grid"))

# done
def deleteAll():
    with open("todolist.csv", "w", newline="") as file:
        writer = DictWriter(file, fieldnames=["id","task","status"])
        writer.writeheader()
    print('\33[2;36mAll tasks has been deleted.\033[0m')

# done
def changeStatus(tasksArr, args):
    statArr = args.split(" ")
    statusID = statArr[0]
    

    if len(statArr) > 2 or statusID.isdecimal() == False:
        raise ValueError("\033[31mPlease put the correct ID to edit.\033[0m")
    if int(statusID) > len(tasksArr):
        raise ValueError("\033[31mID not found\033[0m")
    status = statArr[1]

    if status == '-c':
        for i in range(len(tasksArr)):
            if tasksArr[i]["id"] == statusID:
                tasksArr[i]["status"] = "Complete"
        with open("todolist.csv", "w", newline="") as file:
            writer = DictWriter(file, fieldnames=["id","task","status"])
            writer.writeheader()
            for i in tasksArr:
                writer.writerow({"id": i["id"], "task": i["task"], "status": i["status"]})
        return f"ID({statusID}) is Completed."
    elif status == '-p':
        for i in range(len(tasksArr)):
            if tasksArr[i]["id"] == statusID:
                tasksArr[i]["status"] = "Pending"
        with open("todolist.csv", "w", newline="") as file:
            writer = DictWriter(file, fieldnames=["id","task","status"])
            writer.writeheader()
            for i in tasksArr:
                writer.writerow({"id": i["id"], "task": i["task"], "status": i["status"]})
        return f"ID({statusID}) is Pending."
    


def update(arg):
    update = arg.split(" ")
    taskID = update[0]
    tasks = read()
    if len(update) > 2 or taskID.isdecimal() == False:
        raise ValueError("\033[31mPlease put the correct ID to edit.\033[0m")
    if int(taskID) > len(tasks):
        raise ValueError("\033[31mID not found\033[0m")
    
    userInput = input(f"Edit ID({taskID}): ")

    for i in range(len(tasks)):
        if tasks[i]["id"] == taskID:
            tasks[i]["task"] = userInput

    with open("todolist.csv", "w", newline="") as file:
        writer = DictWriter(file, fieldnames=["id","task","status"])
        writer.writeheader()
        for i in tasks:
            writer.writerow({"id": i["id"], "task": i["task"], "status": i["status"]})
    
    print(f'\33[2;36mEdited ID({taskID}) to "{userInput}"\033[0m')



def delete(input):
    delete = input.split(" ")
    taskID = delete[0]
    tasks = read()
    if len(delete) > 2 or delete[0].isdecimal() == False:
        raise ValueError("\033[31mPlease put the correct ID to delete.\033[0m")
    if int(taskID) > len(tasks):
        raise ValueError("\033[31mID not found\033[0m")
    
    for i in range(len(tasks)):
        if tasks[i]["id"] == taskID:
            print(f"\33[2;36mDeleted ID({tasks[i]['id']})\033[0m")
            tasks.pop(i)
            break

    id_sort(tasks)

def id_sort(newTaskArr):
    tasksID = newTaskArr
    idArr = []
    id_counter = 1

    # Gathers the ID
    for i in range(len(tasksID)):
        idArr.append(tasksID[i]["id"])
    # Sorts the ID to ascending
    for i in range(len(idArr)):
        idArr[i] = id_counter
        id_counter += 1
    # Changes the id from the task array
    for i in range(len(tasksID)):
        tasksID[i]["id"] = idArr[i]
    # Updates the csv file
    with open("todolist.csv", "w", newline="") as file:
        writer = DictWriter(file, fieldnames=["id","task","status"])
        writer.writeheader()
        for i in tasksID:
            writer.writerow({"id": i["id"], "task": i["task"], "status": i["status"]})

    return tasksID
    

# done
def write(tasksArr, input):
    try:
        if tasksArr[0][0] == 'You have no tasks.':
            tasksArr = []
    except:
        pass
    newTask = {"id": len(tasksArr) + 1, "task": input, "status": "Pending"}
    tasksArr.append(newTask)
    
    # Write
    with open("todolist.csv", "w", newline="") as file:
        writer = DictWriter(file, fieldnames=["id","task","status"])
        writer.writeheader()
        for i in tasksArr:
            writer.writerow({"id": i["id"], "task": i["task"], "status": i["status"]})
    
    return tasksArr

def read():
    tasksArr = []

    with open("todolist.csv") as file:
        reader = DictReader(file)
        for i in reader:
            tasksArr.append(i)

    if len(tasksArr) <= 0:
        tasksArr = [['You have no tasks.']]
    return tasksArr


def command_line_args():
    if len(argv) == 1:
        return "default"
    elif len(argv) == 2 and argv[1] == "-o":
        return "open"
    elif len(argv) == 2 and argv[1] == "-h":
        return "help"

def mainMenu():
    print()
    print("\t\t Instruction")
    table = [
        ["-o","to open to do list"],
        ["<id> -e", "to edit task"],
        ["<id> -d", "to delete task"],
        ["<id> -c", "to change status to complete"],
        ["<id> -p", "to change status to pending"],
        ["* -d", "to delete all task"],
        ["-i","to open the instruction again"],
        ["-q / ctrl + c","to quit program"],
    ]
    print(tabulate(table, headers=["Press", "Function "], tablefmt="simple_grid", colalign=("center",)))
    print("Type -o in the command prompt as a second argument to skip displaying the instruction.\n")


if __name__ == "__main__":
    main()
