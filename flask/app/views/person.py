from flask_restx import Namespace, Resource
from flask import request
from app.helpers.response import get_success_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.app_config import config
from common.services import PersonService

# Create the organization blueprint
person_api = Namespace('person', description="Person-related APIs")


@person_api.route('/me')
class Me(Resource):
    
    @login_required()
    def get(self, person):
        return get_success_response(person=person)
        
    @login_required()
    @person_api.expect(
        {'type': 'object', 'properties': {
            'first_name': {'type': 'string'},
            'last_name': {'type': 'string'}
        }}
    )
    def put(self, person):
        """Update the current user's profile information"""
        parsed_body = parse_request_body(request, ['first_name', 'last_name'])
        
        validate_required_fields(parsed_body)

        # # Require at least one field to be provided
        if not parsed_body.get('first_name') and not parsed_body.get('last_name'):
            return get_success_response(
                message="No changes provided. Please provide at least first_name or last_name.",
                person=person
            )
            
        person_service = PersonService(config)
        updated_person = person_service.update_person_name(
            person.entity_id,
            parsed_body.get('first_name'),
            parsed_body.get('last_name')
        )
        
        return get_success_response(
            message="Profile updated successfully.",
            person=updated_person
        )
