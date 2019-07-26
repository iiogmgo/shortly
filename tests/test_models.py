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
