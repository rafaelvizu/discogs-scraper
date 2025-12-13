from scraper.client import fetch_search_page, fetch_artist_page, fetch_album_page
from scraper.parser import parse_artist_names, parse_artist_info, parse_album_info
from scraper.models import Artist
from services.ultils import unique_array_of_objects_by_key, save_array_of_objects_to_jsonl_file
from playwright.async_api import async_playwright
import asyncio
import tracemalloc

tracemalloc.start()



async def process_artist(browser, artist: Artist) -> Artist:
     """Processa um artista: busca info e álbuns."""
     page = await browser.new_page()
     try:
          
          artist_content = await fetch_artist_page(page, artist.url)
          updated_artist = parse_artist_info(artist_content, artist)


          for i, album in enumerate(updated_artist.albums):
               album_content = await fetch_album_page(page, album.url)
               updated_artist.albums[i] = parse_album_info(album_content, album)

          return updated_artist
     finally:
          await page.close()


async def main():
     url = 'https://www.discogs.com'
     limit = 10

     async with async_playwright() as p:
          browser = await p.chromium.launch(headless=False, args=['--start-maximized'])
          page = await browser.new_page()

          content = await fetch_search_page(page, url, 'Rock', page_number=1)
          artists = parse_artist_names(content, limit=limit)

          if len(artists) < limit:
               page_number = 2
               while len(artists) < limit:
                    content = await fetch_search_page(page, url, 'Rock', page_num=page_number)
                    new_artists = parse_artist_names(content)
                    if not new_artists:
                         break
                    artists.extend(new_artists)
                    artists = unique_array_of_objects_by_key(artists, 'id')
                    if len(artists) >= limit:
                         artists = artists[:limit]
                         break
                    page_number += 1

          await page.close()

          tasks = []
          for artist in artists:
               tasks.append(process_artist(browser, artist))

          processed_artists = []
          for i in range(0, len(tasks), 5):
               batch = tasks[i:i+5]
               results = await asyncio.gather(*batch, return_exceptions=True)


               for result in results:
                    if not isinstance(result, Exception):
                         processed_artists.append(result)


          await browser.close()

          # Salvar resultados
          save_array_of_objects_to_jsonl_file(processed_artists, './data/discogs_scraper.jsonl')


if __name__ == '__main__':
     asyncio.run(main())