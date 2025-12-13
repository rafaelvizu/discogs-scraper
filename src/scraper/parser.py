from bs4 import BeautifulSoup
import re
from services.ultils import unique_array_of_objects_by_key
from scraper.models import Artist, Member, Album, Track, Site
from typing import List
from services import log_service

def parse_artist_names(html_content: str, limit = 10) -> List[Artist]:
     
     log_service.log_info("Parsing artist names from HTML content...")

     soup = BeautifulSoup(html_content, 'html.parser')
     artist_elements = soup.find_all('a', href=re.compile(r'^(/[\w]+)?/artist/\d+-'))

     log_service.log_info(f"Found {len(artist_elements)} artist elements in HTML content.")

     artists: List[Artist] = list()
     for element in artist_elements:
          # pegar id, nome, url
          href = element.get('href')

          log_service.log_info(f"Processing artist element with href: {href}")

          match = re.match(r'^(/[\w]+)?/artist/(\d+)-(.+)$', href)
          if match:
               artist_id = match.group(2)
               artist_name = match.group(3).replace('-', ' ')
               artist_url = f"https://www.discogs.com{href}?format=Album"

               artists.append(
                    Artist(
                         id=artist_id,
                         name=artist_name,
                         url=artist_url
                    )
               )

               log_service.log_info(f"Added artist: {artist_name} with ID: {artist_id}")

     return unique_array_of_objects_by_key(artists, 'id')[:limit]     

def parse_artist_info(html_content: str, artist: Artist, limit_albums: int = 10) -> Artist:
     soup = BeautifulSoup(html_content, 'html.parser')

     log_service.log_info("Parsing artist info from HTML content...")
     
     try:
        
          table_element = soup.find(class_=re.compile(r"^table_"))
          tbody = table_element.find("tbody")
     except Exception as e:
          log_service.log_error(f"Error parsing artist info table: {e}")
          raise e

     log_service.log_info("Parsing members from artist info...")
     
     try:
          members_row = tbody.select_one("tr:has(th h2:contains('Members'))")


          if members_row:
               members_td = members_row.find("td")
               members: List[Member] = list()


               for a in members_td.find_all("a", href=re.compile(r'^(/[\w]+)?/artist/\d+-')):
                    href = a.get('href')
                    match = re.match(r'^(/[\w]+)?/artist/(\d+)-(.+)$', href)
                    if match:
                         member_id = match.group(2)
                         member_name = match.group(3).replace('-', ' ')
                         member_url = f"https://www.discogs.com{href}"
                         members.append(
                              Member(
                                   id=member_id,
                                   name=member_name,
                                   url=member_url
                              )
                         )
               artist.members = unique_array_of_objects_by_key(members, 'id')

               log_service.log_info(f"Found {len(artist.members)} members for artist.")
     except Exception as e:
          log_service.log_error(f"Error parsing members: {e}")
          raise e


  
     log_service.log_info("Parsing sites from artist info...")
     try: 
          sites_row = tbody.select_one("tr:has(th h2:contains('Sites'))")
          if sites_row:
               sites_td = sites_row.find("td")
               sites: List[Site] = list()
               for a in sites_td.find_all("a", href=True):
                    site_url = a.get('href')
                    sites.append( 
                         Site(
                              url=site_url,
                         )
                    )

               artist.sites = unique_array_of_objects_by_key(sites, 'url')
               log_service.log_info(f"Found {len(artist.sites)} sites for artist.")
     except Exception as e:
          log_service.log_error(f"Error parsing sites: {e}")
          raise e

  
     try:
          album_info_elements = soup.find('table', class_=re.compile(r"^releases_")) \
               .find('tbody') \
               .find_all('tr')
          
             
          log_service.log_info(f"Parsing album from {artist.name}'s discography...")
          album_list: List[Album] = list()
          for album_tr_element in album_info_elements:

               a = album_tr_element.find('td', class_=re.compile(r"^title_")) \
                    .find('a', href=re.compile(r'^(/[\w]+)?/(master|release)/\d+-')) 


      
               href = a.get('href')
               match = re.match(r'^(/[\w]+)?/(master|release)/(\d+)-(.+)$', href)

               if match:
                    album_id = match.group(3)
                    album_name = match.group(4).replace('-', ' ')
                    album_url = f"https://www.discogs.com{href}"

                    album_obj = Album(
                         id=album_id,
                         title=album_name,
                         url=album_url
                    )

                    album_list.append(album_obj)

                    record_label_elements = album_tr_element.find('td', class_=re.compile(r"^discographyLabel_")) \
                         .findAll('a')
               
                    if record_label_elements:
                         # transformar em objeto
                         album_obj.record_labels = [a.text.strip() for a in record_label_elements]
                         
          artist.albums = unique_array_of_objects_by_key(album_list, 'id')[:limit_albums]

          log_service.log_info(f"Found {len(album_list)} albums for artist {artist.name}.")
     except Exception as e:
          log_service.log_error(f"Error parsing albums for artist {artist.name}: {e}")
          raise e
     



     return artist

def parse_album_info(html_content: str, album: Album) -> Album:
     soup = BeautifulSoup(html_content, 'html.parser')

     table_info_element = soup.find(class_=re.compile(r"^info_")) \
          .find("table") \
          .find("tbody")
     
     try:
          log_service.log_info("Parsing album info from HTML content...")
          style_element = table_info_element.findAll("a", href=re.compile(r'^(/[\w]+)?/style/'))

          if style_element:
               album.styles = [a.text.strip() for a in style_element]

          genres = table_info_element.findAll("a", href=re.compile(r'^(/[\w]+)?/genre/'))
          if genres:
               album.genres = [a.text.strip() for a in genres]
          
          year_element = table_info_element.find("time", string=re.compile(r'^\d{4}$'))

          if year_element:
               album.year = year_element.text.strip()

          log_service.log_info("Album info parsed successfully.")
     except Exception as e:
          log_service.log_error(f"Error parsing album info: {e}")
          raise e


     try:
          log_service.log_info("Parsing album tracks from HTML content...")
          track_list_element = soup.find(id='release-tracklist') \
               .find("div", class_=re.compile(r"^content_")) \
               .findAll("tr", attrs={"data-track-position": True})

          tracks = list()
          for track in track_list_element:
               title = track.find("td", class_=re.compile(r"^trackTitle")).text.strip()

               duration_element = track.find("td", class_=re.compile(r"^duration_"))
               duration = duration_element.text.strip() if duration_element else ""

               tracks.append(
                    Track(
                         title=title,
                         duration=duration
                    )
               )

          album.tracks = tracks
          album.track_count = len(tracks)

          log_service.log_info(f"Found {album.track_count} tracks for album.")
     except Exception as e:
          log_service.log_error(f"Error parsing album tracks: {e}")
          raise e

     return album

     