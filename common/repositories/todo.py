from common.repositories.base import BaseRepository
from common.models.todo import Todo


class TodoRepository(BaseRepository):
    MODEL = Todo
    
    def get_todos_by_person_id(self, person_id: str, offset: int = 0, limit: int = None):
        """Get all todos for a specific person with pagination"""
        return self.get_many({"person_id": person_id}, offset=offset, limit=limit)
    
    def get_completed_todos_by_person_id(self, person_id: str, offset: int = 0, limit: int = None):
        """Get completed todos for a specific person with pagination"""
        return self.get_many({"person_id": person_id, "is_completed": True}, offset=offset, limit=limit)
    
    def get_incomplete_todos_by_person_id(self, person_id: str, offset: int = 0, limit: int = None):
        """Get incomplete todos for a specific person with pagination"""
        return self.get_many({"person_id": person_id, "is_completed": False}, offset=offset, limit=limit)
    
    def count(self, filter_dict):
        """Count records matching the given filter"""
        results = self.get_many(filter_dict)
        return len(results)
    
    def count_todos_by_person_id(self, person_id: str):
        """Count all todos for a specific person"""
        return self.count({"person_id": person_id})
    
    def count_completed_todos_by_person_id(self, person_id: str):
        """Count completed todos for a specific person"""
        return self.count({"person_id": person_id, "is_completed": True})
    
    def count_incomplete_todos_by_person_id(self, person_id: str):
        """Count incomplete todos for a specific person"""
        return self.count({"person_id": person_id, "is_completed": False}) 