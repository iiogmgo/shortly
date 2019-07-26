from shortly.models import Url
from tests.conftest import google_url


def test_check_init_record(url):
    urls = Url.query.all()
    assert len(urls) == 1


def test_fail_to_insert_unique_name(url, session):
    new_url = google_url()
    session.add(new_url)
    try:
        session.commit()
        assert False
    except Exception:
        assert True


def test_validation_logic(session):
    new_url = Url(name='이것은 테스트! HI', destination='www.naver.com')
    session.add(new_url)
    session.commit()
    try:
        url = Url.query.filter_by(name='이것은테스트HI').first()
        assert url.destination == 'http://www.naver.com'
    except Exception:
        assert False