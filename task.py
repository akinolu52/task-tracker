import json
import os
from typing import List, Optional, Dict, Any
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
                # file is missing or not readable, then create an empty file
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

    def add_task(self, description: str):
        """
            Add a new task
            :param description: the description of the task
        """

        # create a new task object
        new_task = Task(
            id=len(self.tasks) + 1,
            description=description,
            status=STATUS_MAP.get('TODO'),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # add the new task to the list of tasks
        self.tasks.append(new_task)
        print(self.tasks, type(self.tasks))

        # save the tasks to the file
        if self.save_tasks():
            print(f"Task added successfully (ID: {new_task.id})")
            return True

        return False

    def update_task(self, id: int, description: str) -> Task:
        """
        This method will update the stored task based on its ID
        :param id: the id of the task
        :param description: the new description
        :return: the task information
        """


    def delete(self):
        pass

    def get(self):
        pass

    def get_all_done(self):
        pass

    def get_in_progress(self):
        pass
