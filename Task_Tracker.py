import json
import argparse
import os

TASKS_FILE = 'tasks.json'

    # this Function check if json file exist or not, if not return the empty list and if does read the content if redable then return it and if not then again it return the empty list and print the warning

def load_tasks():  #define a function with the name of load_tasks which doesent take any input
    if not os.path.exists(TASKS_FILE):          # check whether file exist or not
        return []                               # if file exists then it return empty list []
    try:                                        # start of a try and except block which runs if something goes wrong
        with open(TASKS_FILE, 'r') as file:     # open the fiel in the read format and close it automaticaly after reading it because of use of "with"
            content = file.read().strip()       # read the file and store it into context variable and .read() read the entire content of fiel and .strip() remove all the leadings/whitespaces
            return json.loads(content) if content else [] # return content of jason file if not empty .loads() convert json string into a python object
    except json.JSONDecodeError:                # expection block of try and except block json.JSOMDecodeError specifically means the content was invalid jason or malformed
        print("Warning: tasks.json is corrupted or empty. Reinitializing.") # print this warning if expcept block execute
        return []                               # return the empty list if json couldn't be parsed(can't be break down into smaller ones)

    # It takes the list of tasks and write in json file with the format

def save_tasks(tasks):                          # define a function with the name of save_tasks with the argument of tasks
    with open(TASKS_FILE, 'w') as file:         # open taks file in which we can write and get closed automatically after the with block executed 
        json.dump(tasks, file, indent=4)        # dump() a function of python json library that writes the JSON_formatted data / indent = 4 main the 4 spaces

# read all the tasks and create the new task with the status of "un-done" and add it into the json file

def add_task(title):                            # Define a function with the name add_task with the argument of tittle
    tasks = load_tasks()                        # load_tasks() load the tasks and store it inro tasks varible
    task = {'title': title, 'status': 'not done'} # create the dictionary of new task with the tittle and status
    tasks.append(task)                          # append the new task into the list
    save_tasks(tasks)                           # save the task in the json file with the help of save_tasks() function
    print(f"Added task: {title}")               # print the task after adding it

# update the task status

def update_task(index, status):                 # define the new function with the name of update_task() which take two arguments input index and status
    tasks = load_tasks()                        # it will load all the tasks with the help of load_tasks() function and store it into tasks variable
    if 0 <= index < len(tasks):                 # Check if the index is valid or not
        tasks[index]['status'] = status         # Status get changed by inserting the given status into the status block
        save_tasks(tasks)                       # save the task after inserting it
        print(f"Updated task {index} to status: {status}")  # print the task updated and index and status
    else:                                       # if index is not in limit the print invalid task index
        print("Invalid task index.")

# delete the task with the help of the index assigned to it

def delete_task(index):                         # define the new function with the name of delete_task() with the argument of index
    tasks = load_tasks()                        # it will load all the tasks into the Tasks varible
    if 0 <= index < len(tasks):                 #chech if index is valid or not
        removed = tasks.pop(index)              # pop the task with the help of pop() and saves into removed varible 
        save_tasks(tasks)                       # save the tasks into the file
        print(f"Deleted task: {removed['title']}") # print the tiitle of removed task 
    else:                                       # execute if index is not in limit
        print("Invalid task index.")

# print the task list

def list_tasks(filter_status=None):             # define the new function with the name of list_tasks() with the input argument filter_status optional
    tasks = load_tasks()                        # load all the tasks into the tasks varible with the help of load_tasks() function
    for idx, task in enumerate(tasks):          # loap on the tasks using the varible for index and task
        if filter_status is None or task['status'] == filter_status:    # check for filter status if applied or not and if applied then give result acc to filter status
            print(f"{idx}. [{task['status']}] {task['title']}") #print the index and task tittle and status

if __name__ == '__main__':                      # tack care of the condition that it will specifically run the script from command line
    parser = argparse.ArgumentParser(description="Task Tracker CLI") #
    subparsers = parser.add_subparsers(dest='command')

    # Add
    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('title')

    # Update
    parser_update = subparsers.add_parser('update')
    parser_update.add_argument('index', type=int)
    parser_update.add_argument('status', choices=['done', 'not done', 'in progress'])

    # Delete
    parser_delete = subparsers.add_parser('delete')
    parser_delete.add_argument('index', type=int)

    # List
    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('--status', choices=['done', 'not done', 'in progress'])

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.title)
    elif args.command == 'update':
        update_task(args.index, args.status)
    elif args.command == 'delete':
        delete_task(args.index)
    elif args.command == 'list':
        list_tasks(args.status)
    else:
        parser.print_help()
