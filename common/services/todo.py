from common.repositories.factory import RepositoryFactory, RepoType
from common.models.todo import Todo


class TodoService:
    def __init__(self, config):
        self.config = config
        self.repository_factory = RepositoryFactory(config)
        self.todo_repo = self.repository_factory.get_repository(RepoType.TODO)
    
    def save_todo(self, person_id: str, title: str, description: str):
        todo = Todo(
            person_id=person_id,
            title=title,
            description=description
        )

        return self.save_todo_object(todo)
    
    def save_todo_object(self, todo: Todo):
        """Save an existing Todo object"""
        return self.todo_repo.save(todo)
    
    def get_todo_by_id(self, entity_id: str):
        """Get a todo by its ID"""
        return self.todo_repo.get_one({"entity_id": entity_id})
    
    def get_todos_by_person_id(self, person_id: str, page: int = 1, per_page: int = 10):
        """Get all todos for a person with pagination"""
        offset = (page - 1) * per_page if page > 0 else 0
        return self.todo_repo.get_todos_by_person_id(person_id, offset=offset, limit=per_page)
    
    def get_completed_todos_by_person_id(self, person_id: str, page: int = 1, per_page: int = 10):
        """Get completed todos for a person with pagination"""
        offset = (page - 1) * per_page if page > 0 else 0
        return self.todo_repo.get_completed_todos_by_person_id(person_id, offset=offset, limit=per_page)
    
    def get_incomplete_todos_by_person_id(self, person_id: str, page: int = 1, per_page: int = 10):
        """Get incomplete todos for a person with pagination"""
        offset = (page - 1) * per_page if page > 0 else 0
        return self.todo_repo.get_incomplete_todos_by_person_id(person_id, offset=offset, limit=per_page)
    
    def count_todos_by_person_id(self, person_id: str):
        """Count all todos for a person"""
        return self.todo_repo.count_todos_by_person_id(person_id)
    
    def count_completed_todos_by_person_id(self, person_id: str):
        """Count completed todos for a person"""
        return self.todo_repo.count_completed_todos_by_person_id(person_id)
    
    def count_incomplete_todos_by_person_id(self, person_id: str):
        """Count incomplete todos for a person"""
        return self.todo_repo.count_incomplete_todos_by_person_id(person_id)
    
    def delete_todo(self, entity_id: str):
        """Delete a todo by its ID"""

        todo = self.get_todo_by_id(entity_id) 

        if todo:
            return self.todo_repo.delete(todo)
        return False 