from scraper.client import fetch_search_page, fetch_artist_page, fetch_album_page
from scraper.parser import parse_artist_names, parse_artist_info, parse_album_info
from services.selenium_service import get_driver
from services.ultils import unique_array_of_objects_by_key, save_array_of_objects_to_jsonl_file
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time


def _process_artist_sync(artist, retry_count=0):
     driver = get_driver()
     try:
          artist_page_content = fetch_artist_page(driver, artist.url)
          updated_artist = parse_artist_info(artist_page_content, artist)

          for i, album in enumerate(updated_artist.albums):
               album_page_content = fetch_album_page(driver, album.url)
               updated_artist.albums[i] = parse_album_info(album_page_content, album)

          return updated_artist
     except Exception as e:
          if retry_count < 3:
               raise e

          time.sleep(5)
          return _process_artist_sync(artist, retry_count=retry_count + 1)
          
     finally:
          try:
               driver.quit()
          except Exception:
               pass


async def _process_artists_concurrently(artists, max_workers=5):
     loop = asyncio.get_running_loop() 
     results = []
     with ThreadPoolExecutor(max_workers=max_workers) as executor:
          tasks = [loop.run_in_executor(executor, _process_artist_sync, artist) for artist in artists]
          for coro in asyncio.as_completed(tasks, timeout=300): 
               res = await coro
               results.append(res)

     return results


async def main():
     url = 'https://www.discogs.com/pt_BR'
     limit = 10

     # usar driver temporário apenas para buscar a lista de artistas
     driver = get_driver()
     try:
          page_content = fetch_search_page(driver, url, 'Rock')
          artists = parse_artist_names(page_content, limit=limit)

          if len(artists) < limit:
               page = 2
               while True:
                    page_content = fetch_search_page(driver, url, 'Rock', page=page)
                    new_artists = parse_artist_names(page_content)
                    if not new_artists:
                         break
                    artists.extend(new_artists)
                    artists = unique_array_of_objects_by_key(artists, 'id')
                    if len(artists) >= limit:
                         artists = artists[:limit]
                         break
                    page += 1
     finally:
          try:
               driver.quit()
          except Exception:
               pass

     processed_artists = await _process_artists_concurrently(artists, max_workers=3)

     save_array_of_objects_to_jsonl_file(processed_artists, './data/discogs_scraper.jsonl')


if __name__ == '__main__':
     asyncio.run(main())