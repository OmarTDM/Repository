from flask import Blueprint, request, jsonify
from schema import schema

bp = Blueprint('graphql', __name__)


@bp.route('/graphql', methods=['GET', 'POST'])
def graphql_endpoint():
    if request.method == 'POST':
        data = request.get_json() or {}
        query = data.get('query')
        variables = data.get('variables')
        operation_name = data.get('operationName')
        result = schema.execute(query, variable_values=variables, operation_name=operation_name)
        return jsonify({
            'data': result.data,
            'errors': [str(e) for e in result.errors] if result.errors else None
        })
    return '''<html><body><h1>GraphQL endpoint</h1><p>Send POST with {"query": "..."}</p></body></html>'''
