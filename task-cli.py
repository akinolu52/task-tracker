import sys
from typing import List

from task import TaskProcessor, Task


def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [options]")
        return

    command = sys.argv[1]
    task_processor = TaskProcessor()

    if command == 'add':
        if len(sys.argv) != 3:
            print("Usage: task-cli add <description>")
            return

        description = sys.argv[2]

        if len(description) < 1:
            print("Usage: task-cli add <description>")
            return

        task_processor.add_task(description)

    elif command == 'update':
        if len(sys.argv) != 4:
            print("Usage: task-cli update <id> <description>")
            return

        id = int(sys.argv[2])
        description = sys.argv[3]

        updated_task = task_processor.update_task(id, description)

        if isinstance(updated_task, Task):
            print('Task updated successfully')
            print(updated_task.to_dict())

    elif command == 'delete':
        if len(sys.argv) != 3:
            print("Usage: task-cli delete <id>")
            return

        id = int(sys.argv[2])
        tasks = task_processor.delete_task(id)

        if len(tasks):
            print('Task deleted successfully')
            print([Task.to_dict(task) for task in tasks])

    elif command == 'list':
        print("Listing tasks")
    elif command == 'done':
        print("Completing task")
    else:
        print("Unknown command")


if __name__ == '__main__':
    main()
