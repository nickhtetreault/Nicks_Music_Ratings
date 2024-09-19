from artist_data import Artist, Album

'''
Writing functions to filter through album and song titles to avoid repeats

ex. Artist: Opeth

1995: Orchid
1995: Orchid - 2023 Abbey Road Remaster
    - Ignore the second album because it is a repeat

2003: Peacevill Presents... Opeth
    - Ignore this album because it is a compilation, not an official album
      (despite being listed as a regular album by Spotify...... >:( )

2010: In Live Concert at the Royal Albert Hall			
    - Ignore live albums (again despite being listed as a regular album)

2011: Hertitage (Special Edition)
    - Ignore special editions (repeat of originial Heritage album)

2015: Deliverance and Damnation Remixed
    - Ignore remixed albums (repeats)

2019: In Cauda Venenum (Extended Edition)
    - Ignore extended edition (repeat of In Cauda Venenum)

2019: In Cauda Venenum (Swedish Version)
    - Ignore Swedish version (it's cool but I don't speak swedish)

2006: Still Life (Remastered)
    - Remove (Remastered) from title (no non-remastered version given)

    The Moor (Remastered) - track from Still Life
        - Remove (Remastered) from title (no non-remastered version given)

2008: Watershed (Special Edition)
    - Remove (Special Edition) from title (no non-special edition given)

2001: Blackwater Park
    The Leper Affinity - Live
        - Remove track from list (bonus live track, repeat of first track)
'''

def filter_albums(album_objects):
    # Checking for repeat releases (Remastered, Special Edition, etc.)
    end = len(album_objects)
    for i in range(1, end):
        # Usually remastered album after original in list
        if (album_objects[i - 1] in album_objects[i]):
            # deleting repeats
            del album_objects[i]
            # moving back in array to check if there are multiple duplicates (ex. Opeth)
            i -= 1
            # dynamically change ending index for range of for loop, prevent index out of bounds
            end -= 1
    
    # Checking for live and compilation albums, cleaning remaining album and song titles
    for album in album_objects:
        if ("live" in album.album_title.lower()):
            del album
            continue
        if (check_comp(album.album_title)):
            del album
            continue
        clean_alb_title(album)
        for song in album.song_titles:
            clean_song_title(song)

def check_comp(title):
    remove = [
        "best of",
        "presents",
        "compilation",
        "greatest hits",
        "singles collection",
        "collection",
    ]
    return (r in title.lower() for r in remove)


def clean_alb_title(album):
    remove = [
        "(Remastered)",
        "Remastered",
        "(Remaster)",
        "Remaster",
        "(Special Edition)",
        "Special Edition",
        f"({album.release_date} Remaster)",
        f"{album.release_date} Remaster",
    ]
    for r in remove:
        pos = album.album_title.find(r)
        if (pos > -1):
            album.abum_title[0:pos].strip()

def clean_song_title(title):
    remove = [
        "(Remastered)",
        "Remastered",
        "(Remaster)",
        "Remaster",
        "(Special Edition)",
        "Special Edition",
    ]
    for r in remove:
        pos = title.find(r)
        if (pos > -1):
            title[0:pos].strip()