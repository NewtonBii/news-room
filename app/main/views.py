from flask import render_template, request, redirect, url_for, abort
from . import main
from ..requests import get_sources, get_articles
from flask_login import login_required
from ..models import User
# from .forms import ReviewForm, UpdateProfile


@main.route('/')
def index():
    """View root page function that returns index page and the various news sources"""
    title = 'Home- Welcome to the best News source page'
    # Getting the news sources
    news_sources = get_sources('sources')
    return render_template('index.html', title=title, news_sources=news_sources)


@main.route('/articles/<source_id>', methods=['GET', 'POST'])
@login_required
def source(source_id):
    """View for top story articles"""
    # articles = get_articles('articles')
    source_and_articles = get_articles(source_id)
    return render_template('articles.html', source_and_articles=source_and_articles)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)
