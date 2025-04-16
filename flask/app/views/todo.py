from flask_restx import Namespace, Resource
from flask import request
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, validate_required_fields_from_list
from app.helpers.decorators import login_required
from common.app_config import config
from common.services import TodoService
from common.models import Todo

# Create the todo blueprint
todo_api = Namespace('todo', description="Todo related APIs")


@todo_api.route('/')
class TodoList(Resource):
    @login_required()
    @todo_api.doc(params={
        'status': 'Filter todos by status: "complete" or "incomplete". If not provided, returns all todos.',
        'page': 'Page number for pagination (default: 1)',
        'per_page': 'Number of todos per page (default: 10)'
    })
    def get(self, person):
        """Get all todos for the logged-in user with pagination"""
        todo_service = TodoService(config)
        
        # Get pagination parameters
        try:
            page = int(request.args.get('page', 1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
            
        try:
            per_page = int(request.args.get('per_page', 10))
            if per_page < 1:
                per_page = 2
            elif per_page > 100:  # Set a maximum limit to prevent excessive queries
                per_page = 100
        except ValueError:
            per_page = 10
        
        # Check if status parameter is provided
        status = request.args.get('status')
        
        # Return data based on status parameter
        if status == 'completed':
            todos = todo_service.get_completed_todos_by_person_id(person.entity_id, page, per_page)
            total_todos = todo_service.count_completed_todos_by_person_id(person.entity_id)
        elif status == 'incomplete':
            todos = todo_service.get_incomplete_todos_by_person_id(person.entity_id, page, per_page)
            total_todos = todo_service.count_incomplete_todos_by_person_id(person.entity_id)
        else:
            # Default: return all todos if no valid status parameter is provided
            todos = todo_service.get_todos_by_person_id(person.entity_id, page, per_page)
            total_todos = todo_service.count_todos_by_person_id(person.entity_id)

        total_all_todos = todo_service.count_todos_by_person_id(person.entity_id)
        total_completed_todos = todo_service.count_completed_todos_by_person_id(person.entity_id)
        total_incomplete_todos = todo_service.count_incomplete_todos_by_person_id(person.entity_id)

        print(f"Total todos: {todos}")
        # Calculate pagination metadata
        total_pages = (total_todos + per_page - 1) // per_page  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1
            
        return get_success_response(
            todos=[todo.as_dict() for todo in todos],
            pagination={
                'page': page,
                'per_page': per_page,
                'total_todos': total_todos,
                'total_completed_todos': total_completed_todos,
                'total_incomplete_todos': total_incomplete_todos,
                'total_all_todos': total_all_todos,
                'total_pages': total_pages,
                'has_next': has_next,
                'has_prev': has_prev
            }
        )
    
    @login_required()
    @todo_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string'},
            'description': {'type': 'string'}
        }}
    )
    def post(self, person):
        """Create a new todo for the logged-in user"""
        parsed_body = parse_request_body(request, ['title', 'description'])
        validate_required_fields_from_list(parsed_body, ['title'])

        todo_service = TodoService(config)
        todo = todo_service.save_todo(person.entity_id, parsed_body.get('title'), parsed_body.get('description'))
        
        return get_success_response(todo=todo.as_dict())

@todo_api.route('/<string:todo_id>')
class TodoItem(Resource):
    @login_required()
    def get(self, person, todo_id):
        """Get a specific todo for the logged-in user"""
        todo_service = TodoService(config)
        todo = todo_service.get_todo_by_id(todo_id)
        
        if not todo or todo.person_id != person.entity_id:
            return get_failure_response(message="Todo not found or not authorized")
        
        return get_success_response(todo=todo.as_dict())
    
    @login_required()
    @todo_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string'},
            'description': {'type': 'string'},
            'is_completed': {'type': 'boolean'}
        }}
    )
    def put(self, person, todo_id):
        """Update a specific todo for the logged-in user"""
        todo_service = TodoService(config)
        todo = todo_service.get_todo_by_id(todo_id)

        if not todo or todo.person_id != person.entity_id:
            return get_failure_response(message="Todo not found or not authorized")
        
        parsed_body = parse_request_body(request, ['title', 'description', 'is_completed'])

        todo.title = parsed_body['title'] or todo.title 
        todo.description = parsed_body['description'] or todo.description
        # Check if is_completed is in the parsed_body and is a boolean type
        if 'is_completed' in parsed_body and isinstance(parsed_body['is_completed'], bool):
            todo.is_completed = parsed_body['is_completed']
         
        todo = todo_service.save_todo_object(todo)
        return get_success_response(todo=todo.as_dict())
    
    @login_required()
    def delete(self, person, todo_id):
        """Delete a specific todo for the logged-in user"""
        todo_service = TodoService(config)
        todo = todo_service.get_todo_by_id(todo_id)
        
        if not todo or todo.person_id != person.entity_id:
            return get_failure_response(message="Todo not found or not authorized")
        
        todo_service.delete_todo(todo_id)
        
        return get_success_response(message="Todo deleted successfully") 