import types
from types import SimpleNamespace

import scraper.client as client


def make_mock_driver(page_source: str):
    class MockDriver:
        def __init__(self):
            self.page_source = page_source
            self.get_calls = []

        def get(self, url):
            self.get_calls.append(url)

        def execute_script(self, script, arg):
            return None

    return MockDriver()


def test_fetch_artist_page_returns_page_source(monkeypatch):
    mock = make_mock_driver('<html>artist page</html>')
    monkeypatch.setattr(client, 'log_service', SimpleNamespace(log_info=lambda *a, **k: None, log_error=lambda *a, **k: None))

    result = client.fetch_artist_page(mock, 'https://example.com/artist', wait_time=0)
    assert 'artist page' in result
    assert mock.get_calls[0] == 'https://example.com/artist'


def test_fetch_album_page_returns_page_source(monkeypatch):
    mock = make_mock_driver('<html>album page</html>')
    monkeypatch.setattr(client, 'log_service', SimpleNamespace(log_info=lambda *a, **k: None, log_error=lambda *a, **k: None))

    result = client.fetch_album_page(mock, 'https://example.com/album', wait_time=0)
    assert 'album page' in result
    assert mock.get_calls[0] == 'https://example.com/album'


def test_fetch_search_page_builds_search_url_and_returns_page(monkeypatch):
    mock_driver = make_mock_driver('<html>search page</html>')

    header_element = SimpleNamespace()
    shadow_root = SimpleNamespace()
    search_link = SimpleNamespace()
    search_link.get_attribute = lambda attr: 'https://www.discogs.com/explore'
    shadow_root.find_element = lambda by, sel: search_link

    class FakeWait:
        def __init__(self, driver, timeout):
            pass

        def until(self, cond):
            return header_element

    def fake_execute_script(script, arg):
        return shadow_root

    monkeypatch.setattr(client, 'WebDriverWait', FakeWait)
    mock_driver.execute_script = fake_execute_script
    monkeypatch.setattr(client, 'log_service', SimpleNamespace(log_info=lambda *a, **k: None, log_error=lambda *a, **k: None))

    result = client.fetch_search_page(mock_driver, 'https://www.discogs.com/pt_BR', 'Rock', wait_time=0, page=2)

    assert 'search page' in result
    assert len(mock_driver.get_calls) >= 2
    assert any('genre_exact=Rock' in u and 'page=2' in u for u in mock_driver.get_calls)
