import os
import pytest

from shortly import app as _app
from shortly import db as _db
from config import TEST_DATABASE_PATH

TEST_DATABASE_URI = 'sqlite:///' + TEST_DATABASE_PATH


@pytest.fixture(scope='session')
def app(request):
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI

    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope='session')
def db(app, request):
    if os.path.exists(TEST_DATABASE_PATH):
        os.unlink(TEST_DATABASE_PATH)

    _db.app = app
    _db.create_all()
    _db.session.commit()

    def teardown():
        _db.drop_all()
        os.unlink(TEST_DATABASE_PATH)

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


def google_url():
    from shortly.models import Url

    return Url(name='google-home', destination='http://google.com')


@pytest.fixture(scope='function')
def url(session):
    session.add(google_url())

    return url
