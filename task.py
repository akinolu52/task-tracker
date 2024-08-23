class Task:
    def __init__(self, id, description, status, created_at, updated_at):
        self.id: str = id
        self.description: str = description
        self.status: str = status  # done, in-progress, todo
        self.createdAt = created_at
        self.updatedAt = updated_at


class TaskProvider:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"

    def add(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def get(self):
        pass

    def get_all_done(self):
        pass

    def get_in_progress(self):
        pass
