from playwright.async_api import Page
from services import log_service
import asyncio


async def fetch_search_page(
     page: Page,
     url: str,
     genre: str,
     wait_time: int = 5,
     page_number: int = 1
) -> str:
    log_service.log_info(
        f"Fetching search page for genre '{genre}' at page {page_number}..."
    )

    await page.goto(url)
    log_service.log_info(f"Page loaded for URL: {url}")

    log_service.log_info("Waiting for header shadow root element to be present...")

    try:
        header_shadow_root_element = await page.wait_for_selector(
            "[id^='__header_root_']",
            timeout=20_000
        )

        shadow_root = await header_shadow_root_element.evaluate_handle(
            "el => el.shadowRoot"
        )

        search_link = await shadow_root.query_selector(
            "a[data-tracking='explore-all']"
        )

        log_service.log_info("Found search link in header shadow root.")

        href = await search_link.get_attribute("href")
        search_url = f"{url}{href}?genre_exact={genre}&page={page_number}"

        await page.goto(search_url)
        await asyncio.sleep(wait_time)

        log_service.log_info(
            f"Search page loaded for genre '{genre}' at page {page_number}."
        )

    except Exception as e:
        log_service.log_error(f"Error while fetching search page: {e}")
        raise

    page_source = await page.content()

    log_service.log_info(
        f"Returning page source for genre '{genre}' at page {page_number}."
    )

    return page_source


async def fetch_artist_page(page: Page, artist_url: str) -> str:
    """Busca página de artista do Discogs."""
    log_service.log_info(f"Fetching artist page for URL: {artist_url}")

    await page.goto(artist_url, wait_until='domcontentloaded', timeout=60000)
    await page.wait_for_selector('[class*="releases_"]', timeout=30000)
    log_service.log_info(f"Artist page loaded for URL: {artist_url}")

    content = await page.content()

    return content


async def fetch_album_page(page: Page, album_url: str) -> str:
    """Busca página de álbum do Discogs."""
    log_service.log_info(f"Fetching album page for URL: {album_url}")

    await page.goto(album_url, wait_until='domcontentloaded', timeout=60000)
    log_service.log_info(f"Album page loaded for URL: {album_url}")

    content = await page.content()
    return content
