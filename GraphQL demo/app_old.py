from flask import Flask, render_template, jsonify, request
from graphene import Schema
from schema import schema

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/graphql', methods=['POST', 'GET'])
def graphql():
    if request.method == 'POST':
        data = request.get_json()
        query = data.get('query')
        result = schema.execute(query)
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/researchers')
def researchers():
    return render_template('researchers.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/projectdetails')
def projectdetails():
    return render_template('projectdetails.html')

@app.route('/createproject')
def createproject():
    return render_template('createproject.html')

@app.route('/editproject')
def editproject():
    return render_template('editproject.html')

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/createcourse')
def createcourse():
    return render_template('createcourse.html')

@app.route('/editcourse')
def editcourse():
    return render_template('editcourse.html')

@app.route('/createresearch')
def createresearch():
    return render_template('createresearch.html')

@app.route('/editresearch')
def editresearch():
    return render_template('editresearch.html')

@app.route('/createresearcher')
def createresearcher():
    return render_template('createresearcher.html')

@app.route('/editresearcher')
def editresearcher():
    return render_template('editresearcher.html')

@app.route('/configuration')
def configuration():
    return render_template('configuration.html')

@app.route('/editconfig')
def editconfig():
    return render_template('editconfig.html')

@app.route('/makeconfig')
def makeconfig():
    return render_template('makeconfig.html')

@app.route('/githubrepos')
def githubrepos():
    return render_template('githubrepos.html')

@app.route('/error')
def error_page():
    return render_template('error.html')

@app.route('/deleteconfirmation')
def deleteconfirmation():
    return render_template('deleteconfirmation.html')

@app.route('/api/saved-stats', methods=['GET', 'POST'])
def saved_stats():
    if request.method == 'GET':
        # Return saved statistics from session or database
        saved = request.args.get('data', '[]')
        return jsonify({'stats': saved})
    elif request.method == 'POST':
        # Save new statistic
        data = request.get_json()
        # In production, save to database
        return jsonify({'success': True, 'message': 'Statistic saved'})

if __name__ == '__main__':
    app.run(debug=True)
