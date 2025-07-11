import json
import argparse
import os

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as file:
            content = file.read().strip()
            return json.loads(content) if content else []
    except json.JSONDecodeError:
        print("Warning: tasks.json is corrupted or empty. Reinitializing.")
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(title):
    tasks = load_tasks()
    task = {'title': title, 'status': 'not done'}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task: {title}")

def update_task(index, status):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]['status'] = status
        save_tasks(tasks)
        print(f"Updated task {index} to status: {status}")
    else:
        print("Invalid task index.")

def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"Deleted task: {removed['title']}")
    else:
        print("Invalid task index.")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    for idx, task in enumerate(tasks):
        if filter_status is None or task['status'] == filter_status:
            print(f"{idx}. [{task['status']}] {task['title']}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
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
