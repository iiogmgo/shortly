from flask import Blueprint, request, redirect, url_for, render_template
from shortly.models import Url
from shortly import db

bp = Blueprint('routes', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/urls', methods=['GET'])
def urls():
    return render_template('urls.html', urls=Url.query.all())


@bp.route('/urls', methods=['POST'])
def create():
    from shortly.utils import get_random_shortly_name

    destination = request.form['destination']
    name = request.form['name'] if request.form['name'] else get_random_shortly_name()

    # todo : 자동 생성된 hash로 인해 name unique 에러 뜰 경우 처리
    url = Url(name=name, destination=destination)
    db.session.add(url)
    db.session.commit()

    return redirect(url_for('routes.urls'))


@bp.route('/urls/delete', methods=['POST'])
def delete():
    url_id = request.form['url_id']
    url = Url.query.get(url_id)
    db.session.delete(url)
    db.session.commit()

    return redirect(url_for('routes.urls'))
