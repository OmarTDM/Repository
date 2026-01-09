import os
import sys
import json
import pandas as pd
from bson.objectid import ObjectId
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, send_file
from graphene import Schema
from schema import schema
from db import db, projects_collection
from werkzeug.utils import secure_filename
import pandas as pd
import io
import json
import traceback

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-for-sessions'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file upload

# GRAPHQL ENDPOINT
@app.route('/graphql', methods=['POST', 'GET'])
def graphql():
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
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>GraphiQL</title></head>
    <body>
        <h1>GraphQL Endpoint</h1>
        <p>Send POST requests with {"query": "..."}</p>
    </body>
    </html>
    '''

# HOME & INDEX ROUTES
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

# ============ PROJECTS ROUTES ============
@app.route('/projects')
def projects():
    try:
        query = request.args.get('query', '')
        field = request.args.get('field', 'any')
        
        projects_list = list(projects_collection.find())

        # Normalize fields for the templates (templates expect `title`)
        for project in projects_list:
            # Convert ObjectId to string for template URLs
            if '_id' in project:
                try:
                    project['_id'] = str(project['_id'])
                except Exception:
                    pass
            # Templates use `title` but DB may have `name`
            if 'title' not in project and 'name' in project:
                project['title'] = project.get('name')

        for project in projects_list:
            # Resolve references to other collections
            if "research_project" in project and project["research_project"]:
                try:
                    rp = db.research_projects.find_one({"_id": ObjectId(project["research_project"])})
                    project["research_project"] = rp.get("name", "Unknown") if rp else None
                except:
                    pass
            
            if "researcher" in project and project["researcher"]:
                try:
                    res = db.researchers.find_one({"_id": ObjectId(project["researcher"])})
                    project["researcher"] = res.get("name", "Unknown") if res else None
                except:
                    pass
            
            if "course" in project and project["course"]:
                try:
                    course_obj = db.course.find_one({"_id": ObjectId(project["course"])})
                    project["course"] = course_obj.get("name", "Unknown") if course_obj else None
                except:
                    pass
        
        # Filter projects
        if query and field:
            if field == "any":
                projects_list = [p for p in projects_list if any(query.lower() in str(v).lower() for v in p.values())]
            else:
                projects_list = [p for p in projects_list if query.lower() in str(p.get(field, '')).lower()]
        
        # Reverse for newest first
        projects_list.reverse()
        
        df = pd.DataFrame(projects_list) if projects_list else pd.DataFrame()
        table_columns = df.columns.tolist() if not df.empty else []
        table_rows = df.to_dict(orient="records") if not df.empty else []
        
        research = list(db.research_projects.find()) if hasattr(db, 'research_projects') else []
        
        return render_template(
            'projects.html',
            table_columns=table_columns,
            table_rows=table_rows,
            research=research
        )
    except Exception as e:
        print(f"Error in projects route: {e}")
        traceback.print_exc()
        return render_template('projects.html', table_columns=[], table_rows=[], research=[])

@app.route('/projectdetails')
def projectdetails():
    try:
        project_id = request.args.get('id')
        if project_id:
            project = projects_collection.find_one({"_id": ObjectId(project_id)})
            if project:
                return render_template('projectdetails.html', project=project)
        return render_template('projectdetails.html', project=None)
    except Exception as e:
        print(f"Error in projectdetails: {e}")
        return render_template('projectdetails.html', project=None)

@app.route('/createproject', methods=['GET', 'POST'])
def createproject():
    if request.method == 'POST':
        try:
            # Normalize and dedupe student names so duplicates (and different orderings) are not double-counted
            raw_students = request.form.getlist('students')

            def _normalize_name(n: str) -> str:
                if not n:
                    return ''
                s = n.strip()
                # if given as "Surname, Firstname" convert to "Firstname Surname"
                if ',' in s:
                    parts = [p.strip() for p in s.split(',', 1)]
                    s = f"{parts[1]} {parts[0]}"
                # collapse whitespace and lower for comparison
                return ' '.join(s.split()).lower()

            seen = set()
            unique_students = []
            for s in raw_students:
                key = _normalize_name(s)
                if not key:
                    continue
                if key in seen:
                    continue
                seen.add(key)
                # store original-ish formatting (trimmed)
                unique_students.append(' '.join(s.strip().replace(',', '').split()))

            project_data = {
                'name': request.form.get('name', ''),
                'description': request.form.get('description', ''),
                'students': unique_students,
                'studentCount': len(unique_students),
                'course': request.form.get('course', ''),
                'researcher': request.form.get('researcher', ''),
                'researchProject': request.form.get('research_project', ''),
                'status': request.form.get('status', 'In Progress'),
                'github': request.form.get('github', '')
            }
            
            result = projects_collection.insert_one(project_data)
            return redirect(url_for('projects'))
        except Exception as e:
            print(f"Error creating project: {e}")
            flash(f'Error creating project: {str(e)}', 'error')
    
    courses = list(db.course.find()) if hasattr(db, 'course') else []
    researchers = list(db.researchers.find()) if hasattr(db, 'researchers') else []
    research_projects = list(db.research_projects.find()) if hasattr(db, 'research_projects') else []
    
    return render_template('createproject.html', courses=courses, researchers=researchers, research_projects=research_projects)

@app.route('/editproject', methods=['GET', 'POST'])
def editproject():
    project_id = request.args.get('id')
    
    if request.method == 'POST':
        try:
            # Normalize & dedupe students same as createproject
            raw_students = request.form.getlist('students')

            def _normalize_name(n: str) -> str:
                if not n:
                    return ''
                s = n.strip()
                if ',' in s:
                    parts = [p.strip() for p in s.split(',', 1)]
                    s = f"{parts[1]} {parts[0]}"
                return ' '.join(s.split()).lower()

            seen = set()
            unique_students = []
            for s in raw_students:
                key = _normalize_name(s)
                if not key:
                    continue
                if key in seen:
                    continue
                seen.add(key)
                unique_students.append(' '.join(s.strip().replace(',', '').split()))

            update_data = {
                'name': request.form.get('name', ''),
                'description': request.form.get('description', ''),
                'students': unique_students,
                'studentCount': len(unique_students),
                'course': request.form.get('course', ''),
                'researcher': request.form.get('researcher', ''),
                'researchProject': request.form.get('research_project', ''),
                'status': request.form.get('status', 'In Progress'),
                'github': request.form.get('github', '')
            }
            
            projects_collection.update_one(
                {"_id": ObjectId(project_id)},
                {"$set": update_data}
            )
            return redirect(url_for('projects'))
        except Exception as e:
            print(f"Error updating project: {e}")
            flash(f'Error updating project: {str(e)}', 'error')
    
    project = projects_collection.find_one({"_id": ObjectId(project_id)}) if project_id else None
    courses = list(db.course.find()) if hasattr(db, 'course') else []
    researchers = list(db.researchers.find()) if hasattr(db, 'researchers') else []
    research_projects = list(db.research_projects.find()) if hasattr(db, 'research_projects') else []
    
    return render_template('editproject.html', project=project, courses=courses, researchers=researchers, research_projects=research_projects)

# ============ RESEARCHERS ROUTES ============
@app.route('/researchers')
def researchers():
    try:
        researchers_list = list(db.researchers.find()) if hasattr(db, 'researchers') else []
        return render_template('researchers.html', researchers=researchers_list)
    except:
        return render_template('researchers.html', researchers=[])

@app.route('/createresearcher', methods=['GET', 'POST'])
def createresearcher():
    if request.method == 'POST':
        try:
            researcher_data = {
                'name': request.form.get('name', ''),
                'email': request.form.get('email', ''),
                'title': request.form.get('title', '')
            }
            db.researchers.insert_one(researcher_data)
            return redirect(url_for('researchers'))
        except Exception as e:
            flash(f'Error creating researcher: {str(e)}', 'error')
    
    return render_template('createresearcher.html')

@app.route('/editresearcher', methods=['GET', 'POST'])
def editresearcher():
    researcher_id = request.args.get('id')
    
    if request.method == 'POST':
        try:
            update_data = {
                'name': request.form.get('name', ''),
                'email': request.form.get('email', ''),
                'title': request.form.get('title', '')
            }
            db.researchers.update_one(
                {"_id": ObjectId(researcher_id)},
                {"$set": update_data}
            )
            return redirect(url_for('researchers'))
        except Exception as e:
            flash(f'Error updating researcher: {str(e)}', 'error')
    
    researcher = db.researchers.find_one({"_id": ObjectId(researcher_id)}) if researcher_id else None
    return render_template('editresearcher.html', researcher=researcher)

# ============ COURSES ROUTES ============
@app.route('/courses')
def courses():
    try:
        courses_list = list(db.course.find()) if hasattr(db, 'course') else []
        return render_template('courses.html', courses=courses_list)
    except:
        return render_template('courses.html', courses=[])

@app.route('/course')
def course():
    try:
        course_id = request.args.get('id')
        if course_id:
            course_obj = db.course.find_one({"_id": ObjectId(course_id)})
            if course_obj:
                return render_template('course.html', course=course_obj)
        return render_template('course.html', course=None)
    except:
        return render_template('course.html', course=None)

@app.route('/createcourse', methods=['GET', 'POST'])
def createcourse():
    if request.method == 'POST':
        try:
            course_data = {
                'name': request.form.get('name', ''),
                'code': request.form.get('code', ''),
                'description': request.form.get('description', '')
            }
            db.course.insert_one(course_data)
            return redirect(url_for('courses'))
        except Exception as e:
            flash(f'Error creating course: {str(e)}', 'error')
    
    return render_template('createcourse.html')

@app.route('/editcourse', methods=['GET', 'POST'])
def editcourse():
    course_id = request.args.get('id')
    
    if request.method == 'POST':
        try:
            update_data = {
                'name': request.form.get('name', ''),
                'code': request.form.get('code', ''),
                'description': request.form.get('description', '')
            }
            db.course.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": update_data}
            )
            return redirect(url_for('courses'))
        except Exception as e:
            flash(f'Error updating course: {str(e)}', 'error')
    
    course_obj = db.course.find_one({"_id": ObjectId(course_id)}) if course_id else None
    return render_template('editcourse.html', course=course_obj)

# ============ RESEARCH ROUTES ============
@app.route('/research')
def research():
    try:
        research_list = list(db.research_projects.find()) if hasattr(db, 'research_projects') else []
        return render_template('research.html', research=research_list)
    except:
        return render_template('research.html', research=[])

@app.route('/createresearch', methods=['GET', 'POST'])
def createresearch():
    if request.method == 'POST':
        try:
            research_data = {
                'name': request.form.get('name', ''),
                'description': request.form.get('description', ''),
                'researcher': request.form.get('researcher', '')
            }
            db.research_projects.insert_one(research_data)
            return redirect(url_for('research'))
        except Exception as e:
            flash(f'Error creating research project: {str(e)}', 'error')
    
    researchers = list(db.researchers.find()) if hasattr(db, 'researchers') else []
    return render_template('createresearch.html', researchers=researchers)

@app.route('/editresearch', methods=['GET', 'POST'])
def editresearch():
    research_id = request.args.get('id')
    
    if request.method == 'POST':
        try:
            update_data = {
                'name': request.form.get('name', ''),
                'description': request.form.get('description', ''),
                'researcher': request.form.get('researcher', '')
            }
            db.research_projects.update_one(
                {"_id": ObjectId(research_id)},
                {"$set": update_data}
            )
            return redirect(url_for('research'))
        except Exception as e:
            flash(f'Error updating research project: {str(e)}', 'error')
    
    research_proj = db.research_projects.find_one({"_id": ObjectId(research_id)}) if research_id else None
    researchers = list(db.researchers.find()) if hasattr(db, 'researchers') else []
    return render_template('editresearch.html', research=research_proj, researchers=researchers)

# ============ DOWNLOADS ROUTES ============
@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/api/export-json')
def export_json():
    try:
        projects_list = list(projects_collection.find())
        # Convert ObjectId to string for JSON serialization
        for proj in projects_list:
            proj['_id'] = str(proj['_id'])
        
        return jsonify(projects_list), 200, {'Content-Disposition': 'attachment; filename=projects.json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-csv')
def export_csv():
    try:
        projects_list = list(projects_collection.find())
        df = pd.DataFrame(projects_list)
        
        # Convert ObjectId to string
        df['_id'] = df['_id'].astype(str)
        
        csv_data = df.to_csv(index=False)
        return csv_data, 200, {'Content-Disposition': 'attachment; filename=projects.csv'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ STATISTICS ROUTES ============
@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        total_projects = projects_collection.count_documents({})
        total_researchers = db.researchers.count_documents({}) if hasattr(db, 'researchers') else 0
        total_courses = db.course.count_documents({}) if hasattr(db, 'course') else 0
        total_research = db.research_projects.count_documents({}) if hasattr(db, 'research_projects') else 0
        
        return jsonify({
            'projects': total_projects,
            'researchers': total_researchers,
            'courses': total_courses,
            'research': total_research
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/saved-stats', methods=['GET', 'POST'])
def saved_stats():
    try:
        if request.method == 'GET':
            # return all saved stats from DB
            saved = list(db.saved_stats.find()) if hasattr(db, 'saved_stats') else []
            # serialize ObjectId
            for s in saved:
                if '_id' in s:
                    try:
                        s['_id'] = str(s['_id'])
                    except:
                        pass
            return jsonify({'stats': saved})

        elif request.method == 'POST':
            data = request.get_json() or {}
            # expected fields: name, type, query, xField, yField, data (optional)
            entry = {
                'name': data.get('name', 'Untitled'),
                'type': data.get('type', 'bar'),
                'query': data.get('query'),
                'collection': data.get('collection'),
                'projects': data.get('projects'),
                'xField': data.get('xField'),
                'yField': data.get('yField'),
                'data': data.get('data') if data.get('data') is not None else None,
                'style': data.get('style') if data.get('style') is not None else None,
                'meta': data.get('meta') if data.get('meta') is not None else None,
            }
            try:
                res = db.saved_stats.insert_one(entry)
                entry['_id'] = str(res.inserted_id)
            except Exception:
                # if DB not available, fall back to echoing entry
                pass
            return jsonify({'success': True, 'stat': entry})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/saved-stats/<stat_id>', methods=['DELETE'])
def delete_saved_stat(stat_id):
    try:
        if not hasattr(db, 'saved_stats'):
            return jsonify({'success': False, 'error': 'No saved_stats collection available'}), 404
        from bson.objectid import ObjectId
        db.saved_stats.delete_one({'_id': ObjectId(stat_id)})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/db-examples', methods=['GET'])
def db_examples():
    try:
        if not db:
            return jsonify({'collections': []})
        collections = db.list_collection_names()
        samples = {}
        for coll_name in collections:
            try:
                coll = db[coll_name]
                docs = list(coll.find().limit(10))
                # serialize ObjectId
                def _serialize(d):
                    out = {}
                    for k, v in d.items():
                        try:
                            if hasattr(v, '__class__') and v.__class__.__name__ == 'ObjectId':
                                out[k] = str(v)
                            else:
                                out[k] = v
                        except Exception:
                            out[k] = v
                    return out
                samples[coll_name] = [_serialize(doc) for doc in docs]
            except Exception:
                samples[coll_name] = []

        return jsonify({'collections': collections, 'samples': samples})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ CONFIGURATION ROUTES ============
@app.route('/configuration')
def configuration():
    try:
        configs = list(db.configurations.find()) if hasattr(db, 'configurations') else []
        return render_template('configuration.html', configs=configs)
    except:
        return render_template('configuration.html', configs=[])

@app.route('/makeconfig', methods=['GET', 'POST'])
def makeconfig():
    if request.method == 'POST':
        try:
            config_data = {
                'name': request.form.get('name', ''),
                'value': request.form.get('value', ''),
                'inuse': request.form.get('inuse') == 'on'
            }
            db.configurations.insert_one(config_data)
            return redirect(url_for('configuration'))
        except Exception as e:
            flash(f'Error creating configuration: {str(e)}', 'error')
    
    return render_template('makeconfig.html')

@app.route('/editconfig', methods=['GET', 'POST'])
def editconfig():
    config_id = request.args.get('id')
    
    if request.method == 'POST':
        try:
            update_data = {
                'name': request.form.get('name', ''),
                'value': request.form.get('value', ''),
                'inuse': request.form.get('inuse') == 'on'
            }
            db.configurations.update_one(
                {"_id": ObjectId(config_id)},
                {"$set": update_data}
            )
            return redirect(url_for('configuration'))
        except Exception as e:
            flash(f'Error updating configuration: {str(e)}', 'error')
    
    config = db.configurations.find_one({"_id": ObjectId(config_id)}) if config_id else None
    return render_template('editconfig.html', config=config)

# ============ GITHUB ROUTES ============
@app.route('/githubrepos')
def githubrepos():
    return render_template('githubrepos.html')

# ERROR ROUTES 
@app.route('/error')
def error_page():
    return render_template('error.html')

@app.route('/deleteconfirmation')
def deleteconfirmation():
    return render_template('deleteconfirmation.html')

@app.route('/api/delete-project', methods=['POST'])
def delete_project():
    try:
        project_id = request.json.get('id')
        projects_collection.delete_one({"_id": ObjectId(project_id)})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
