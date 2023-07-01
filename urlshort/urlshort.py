from flask import render_template , request , redirect, url_for ,flash,abort,session ,jsonify , Blueprint
import json , os.path
from werkzeug.utils import secure_filename
bp = Blueprint('urlshort' , __name__)

@bp.route('/')

def home():
    return render_template('home.html',name='Sriram Sivaraman' , codes = session.keys()) # we also can pass info to the template access this variable in the html file using {{}}

@bp.route('/about')
def about():
    return "this is my first flask app."

@bp.route('/your-url' , methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        url = {}

        if os.path.exists('urls.json'):
            with open('urls.json' , 'r') as urls_json:
                url = json.load(urls_json)
        
        if request.form['code'] in url:
            flash('this shorten name is already taken')
            return redirect(url_for('urlshort.home'))
        
        # for processing url
        if 'url' in request.form.keys():
            url[request.form['code']] = {'url':request.form['url']}
            print(url)
        else:
        # for processing files
            f = request.files['file']
            full_name = request.form['code'] + "_" +secure_filename(f.filename)
            f.save('/Users/sriramsivaraman/Desktop/flask_project/urlshort/static/user_files/' + "_"+full_name)
            url[request.form['code']] = {'file':full_name}
           
    
        with open('urls.json' , 'w') as url_file:
            json.dump(url , url_file)
            session[request.form['code']] = True
        return render_template('your_url.html')
    
    #for get requests
    elif request.method == 'GET':
        flash("get requests is unsupported. This is all on the developer")
        return redirect(url_for('urlshort.home'))
    
@bp.route('/<string:code>')
def redirect_to_url(code):
    url = {}
    if os.path.exists('urls.json'):
            with open('urls.json' , 'r') as urls_json:
                url = json.load(urls_json)
                if code in url.keys():
                    if 'url' in url[code].keys():
                        return redirect(url[code]['url'])
                    else:
                        return redirect(url_for('static', filename = 'user_files/'+"_"+url[code]['file']))
    return abort(404)       

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html') , 404

#api
@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
