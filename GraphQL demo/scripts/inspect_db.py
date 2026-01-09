from pprint import pprint
import os
import sys

# Ensure project root is on sys.path so imports work when launching the script from anywhere
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import db

print('project root:', ROOT)
print('db module present:', hasattr(db, 'projects_collection'))
pc = db.projects_collection
print('projects_collection type:', type(pc))
print('has find:', hasattr(pc, 'find'))
print('has find_one:', hasattr(pc, 'find_one'))
print('has count_documents:', hasattr(pc, 'count_documents'))
try:
    count = pc.count_documents({}) if hasattr(pc, 'count_documents') else 'N/A'
except Exception as e:
    count = f'error: {e}'
print('count_documents ->', count)
try:
    docs = list(pc.find()) if hasattr(pc, 'find') else []
    print('sample docs count:', len(docs))
    if docs:
        pprint(docs[0])
except Exception as e:
    print('error listing docs:', e)
