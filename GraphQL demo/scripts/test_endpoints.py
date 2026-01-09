import sys
import os
sys.path.append(r'C:\Users\Omarb\Downloads\graphql_demo')
os.environ['DISABLE_AUTH'] = 'true'
from app import create_app
app = create_app()
client = app.test_client()

resp = client.get('/projects')
print('/projects', resp.status_code)
print('projects page length', len(resp.data))

resp2 = client.get('/stats')
print('/stats', resp2.status_code)

import json
q = json.dumps({
    "query": "query($collection:String!, $limit:Int){ queryDocuments(collection:$collection, limit:$limit) }",
    "variables": {"collection": "projects", "limit": 100}
})
resp3 = client.post('/graphql', data=q, content_type='application/json')
print('/graphql', resp3.status_code)
try:
    j = resp3.get_json()
    docs = j.get('data', {}).get('queryDocuments', [])
    print('graphql docs count', len(docs))
except Exception as e:
    print('graphql json parse error', e)
