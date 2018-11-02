from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import CsrfProtect

from forms import PostForm
from models import Post, initialize

DEBUG = True
PORT = 5000
HOST = '0.0.0.0'

csrf = CsrfProtect()
app = Flask(__name__)
app.secret_key = 'lf;ksd;flkajsd'
csrf.init_app(app)


@app.route('/')
@app.route('/entries', methods=('GET', 'POST'))
def index():
    """Shows all the posts-home page"""
    posts = Post.select().limit(100)
    return render_template('index.html', stream=posts)


@app.route('/entries/<title>', methods=('GET', 'POST'))
def view_post(title="LIFE"):
    """Shows the post selected"""
    post = Post.select().where(Post.title == title).get()
    return render_template('detail.html', post=post)


@app.route('/entries/<title>/edit', methods=('GET', 'POST'))
def edit(title):
    """Edits the selected entry"""
    post = Post.select().where(Post.title == title).get()
    form = PostForm()

    if form.validate_on_submit():
        # re-saving the data in the database
        post.title = form.title.data
        post.date = form.date.data
        post.timespent = form.timespent.data
        post.content = form.content.data
        post.resources = form.resources.data
        post.save()
        flash("Post successfully edited!", "success")
        return redirect(url_for('index'))
    else:
        # saving default info to the template
        form.title.default = post.title
        form.date.default = post.date
        form.timespent.default = post.timespent
        form.content.default = post.content
        form.resources.default = post.resources
        form.process()
        return render_template('edit-template.html', form=form)


@app.route('/entries/add', methods=('GET', 'POST'))
def add():
    """Adds new entry"""
    form = PostForm()
    if form.validate_on_submit():
        Post.create(
            title=form.title.data,
            date=form.date.data,
            timespent=form.timespent.data,
            content=form.content.data,
            resources=form.resources.data
        )
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.route('/entries/<title>/delete')
def delete(title):
    """Deletes the selected post."""
    post = Post.select().where(Post.title == title).get()
    post.delete_instance()
    flash('The post has been deleted', "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)
