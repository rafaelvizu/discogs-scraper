import os
from scraper.parser import parse_artist_names, parse_artist_info, parse_album_info
from scraper.models import Artist
from scraper.models import Artist, Album




def load_fixture(name: str) -> str:
    path = os.path.join(os.path.dirname(__file__), 'fixtures', name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def test_parse_artist_names_basic():
    html = load_fixture('artist_search.html')
    artists = parse_artist_names(html, limit=2)

    assert len(artists) == 2
    assert artists[0].id == '101'
    assert 'The Beatles' in artists[0].name


def test_parse_artist_info_members_sites_and_albums():
    html = load_fixture('artist_page.html')
    # criar artista mínimo para ser preenchido
    artist = Artist(id='999', name='Test Artist', url='https://example.com')

    updated = parse_artist_info(html, artist)

    # members
    assert hasattr(updated, 'members')
    assert any(m.id == '201' for m in updated.members)

    # sites
    assert hasattr(updated, 'sites')
    assert any(s.url == 'https://example.com' or 'example.com' in s.url for s in updated.sites)

    # albums
    assert hasattr(updated, 'albums')
    assert len(updated.albums) == 1
    assert updated.albums[0].id == '555'

def test_parse_album_info_tracks_styles_and_year():
    html = load_fixture('album_page.html')
    album = Album(id='555', title='Some Album', url='https://example.com/release/555')

    updated = parse_album_info(html, album)

    assert updated.year == '1999'
    assert any('Rock' in s for s in (updated.styles or []))
    assert updated.track_count == 2
    assert updated.tracks[0].title == 'First Track'

