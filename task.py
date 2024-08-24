import json
import os
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

TASK_FILE_PATH = './tasks.json'
STATUS_MAP = {
    'TODO': 'todo',
    'IN-PROGRESS': 'in-progress',
    'DONE': 'done',
}


class Task:
    def __init__(self, id: int, description: str, status: Optional[str], created_at: datetime, updated_at: datetime):
        self.id: int = id
        self.description: str = description
        self.status: str = status or STATUS_MAP.get('TODO')
        self.createdAt: str = created_at.isoformat()
        self.updatedAt: str = updated_at.isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Task':
        return Task(
            id=data['id'],
            description=data['description'],
            status=data['status'],
            created_at=datetime.fromisoformat(data['createdAt']),
            updated_at=datetime.fromisoformat(data['updatedAt'])
        )


class TaskProcessor:
    def __init__(self, ):
        self.tasks: List[Task] = self.load_tasks()

    @staticmethod
    def load_tasks() -> List[Task]:
        """
            check if the tasks JSON file exist and Load tasks from a file
            :return: the content of the tasks JSON file
        """
        try:
            if os.path.isfile(TASK_FILE_PATH) and os.access(TASK_FILE_PATH, os.R_OK):
                with open(TASK_FILE_PATH, 'r') as file:
                    data = json.load(file)
                    return [Task.from_dict(task) for task in data]
            else:
                # if the file is missing, then create an empty file
                with open(TASK_FILE_PATH, 'w') as file:
                    json.dump([], file)
                    return []
        except FileNotFoundError:
            return []

    def save_tasks(self) -> bool:
        """
            Save all tasks into the JSON file
            :return: boolean indicating if the process is successful or not
        """
        try:
            with open(TASK_FILE_PATH, 'w') as file:
                tasks_dict = [task.to_dict() for task in self.tasks]
                json.dump(tasks_dict, file, indent=4)
                return True
        except Exception as ex:
            print('Error: ', ex)
            return False

    def get_next_id(self) -> int:
        """
            get the largest ID in the tasks JSON and increment it by 1 or returns 1
            :return: 1 if there are no tasks else return one + the largest ID
        """
        return max(task.id for task in self.tasks) + 1 if self.tasks else 1

    def get_task_index(self, id: int) -> Union[None, int]:
        """
            This function searches through the list of tasks and
            returns the index of the task that matches the given identifier.
            If no task is found with the specified ID, it returns None.
            :param id: The identifier of the task to find.
            :return: Union[None, int]: The index of the task if found, otherwise None.
        """
        task_index = None

        # find the task
        for idx, task in enumerate(self.tasks):
            if task.id == id:
                task_index = idx
                break

        return task_index

    def add_task(self, description: str):
        """
            Add a new task
            :param description: the description of the task
        """

        # create a new task object
        new_task = Task(
            id=self.get_next_id(),
            description=description,
            status=STATUS_MAP.get('TODO'),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # add the new task to the list of tasks
        self.tasks.append(new_task)

        # save the tasks to the file
        if self.save_tasks():
            print(f"Task added successfully (ID: {new_task.id})")
            return True

        return False

    def update_task(self, id: int, description: str) -> Optional[Task]:
        """
        update the stored task based on its ID
        :param id: the id of the task
        :param description: the new description of the task
        :return: the updated task information or none if not found
        """

        task_to_update: Optional[Task] = None

        # find the task
        task_index = self.get_task_index(id)

        if isinstance(task_index, int):
            task_to_update = self.tasks[task_index]
            task_to_update.description = description
            task_to_update.updatedAt = datetime.now().isoformat()

            self.tasks[task_index] = task_to_update

            # save the updated task to JSON
            self.save_tasks()

            # return the task
            return task_to_update

        else:
            print(f"Task with ID:{id} not found!")
            return None

    def delete_task(self, id: int) -> Optional[List[Task]]:
        """
        delete a task based on the passed ID
        :param id: the ID of the task to delete
        :return: the remaining tasks information found in the JSON file
        """
        # find the task
        task_index = self.get_task_index(id)

        if isinstance(task_index, int):
            del self.tasks[task_index]

            # save the updated task to JSON
            self.save_tasks()

            # return all tasks
            return self.tasks

        else:
            print(f"Task with ID:{id} not found!")
            return None

    def mark_task(self, id: int, status: str) -> Optional[Task]:
        """
        Find and Update the task status based on the passed ID
        :param status: the new status of the task, can either be IN-PROGRESS or DONE
        :param id: the ID of the task to delete
        :return: the updated task information or none if not found
        """
        # find the task
        task_index = self.get_task_index(id)

        if isinstance(task_index, int):
            task_to_update = self.tasks[task_index]
            task_to_update.status = STATUS_MAP.get(status.upper())
            task_to_update.updatedAt = datetime.now().isoformat()

            self.tasks[task_index] = task_to_update

            # save the updated task to JSON
            self.save_tasks()

            # return the task
            return task_to_update

        else:
            print(f"Task with ID:{id} not found!")
            return None

    def get_tasks(self, status: Optional[str]) -> List[Task]:
        """
        filter tasks based on status or return all if status is empty
        :param status: can be done, in-progress, todo or None - this is a filter for the tasks
        :return: all the tasks matching the set filter
        """
        tasks: List[Task] = []

        if not status:
            return self.tasks

        if status not in ['in-progress', 'done', 'todo']:
            print("Unknown status!")
            return self.tasks

        return [
            task
            for task in self.tasks
            if task.status == STATUS_MAP.get(status.upper())
        ]
