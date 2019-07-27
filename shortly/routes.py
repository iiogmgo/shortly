from flask import Blueprint, request, redirect, url_for, render_template
from shortly.models import Url
from shortly import db
from sqlalchemy import exc
from shortly.utils import get_random_shortly_name

bp = Blueprint('routes', __name__)


@bp.route('/')
def index():
    if 'name' in request.args:
        name = request.args['name']
        destination = request.args['destination']
        message = request.args['message']
        return render_template('index.html', name=name, destination=destination, message=message)

    return render_template('index.html')


@bp.route('/urls', methods=['GET'])
def urls():
    return render_template('urls.html', urls=Url.query.all())


def insert_url_with_retry(is_hash_name, name, destination):
    url = Url(name=name, destination=destination)
    db.session.add(url)
    try:
        db.session.commit()
        return redirect(url_for('routes.urls'))
    except exc.IntegrityError:
        if is_hash_name:
            insert_url_with_retry(is_hash_name, get_random_shortly_name(), destination)
        else:
            return redirect(url_for('index',
                                    name=name, destination=destination,
                                    message='The name({}) already registered.'.format(name)))


@bp.route('/urls', methods=['POST'])
def create():
    is_hash_name = False if request.form['name'] else True
    destination = request.form['destination']
    name = get_random_shortly_name() if is_hash_name else request.form['name']

    return insert_url_with_retry(is_hash_name, name, destination)


@bp.route('/urls/delete', methods=['POST'])
def delete():
    url_id = request.form['url_id']
    url = Url.query.get(url_id)
    db.session.delete(url)
    db.session.commit()

    return redirect(url_for('routes.urls'))


@bp.route('/<url_name>', methods=['GET'])
def redirect_to_destination(url_name):
    url = Url.query.filter_by(name=url_name).first()

    return redirect(url.destination) if url else redirect(url_for('index'))
