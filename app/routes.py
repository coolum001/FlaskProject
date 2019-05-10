from flask import render_template
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename


from app import app

from app.forms import LoginForm

import os


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Everyman'}
    posts = [
        {'author': {'username': 'John'}, 'body': 'Blog post 1'},
        {'author': {'username': 'Anon'}, 'body': 'Blog post 2'},
    ]

    return render_template('index.html', user=user, posts=posts)


# end index


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash(
            'Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data
            )
        )
        return redirect('/index')
    # end if

    return render_template('login.html', title='Sign In', form=form)


# end login
ALLOWED_EXTENSIONS = set(['jpg'])


def allowed_file(filename):
    return ('.' in filename) and (
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# end allowed_file


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # end if
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # end if
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            flash('Loading .. ' + filename)
            flash('Saving to ' + app.config['UPLOAD_FOLDER'])
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return redirect('/index')
        # end if
    # end if
    return render_template('upload.html', title='Upload File')


# end upload_file


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

