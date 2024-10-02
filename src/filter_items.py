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

        
The following filters seem to work for now, but there will definitely be exceptions
I plan to later add implementation that allows the user to request a "re-filter" of the artist data,
where a new request to filter the artist data will call a different filter protocol
    i.e using chatgpt api to return a list of artist's studio albums and comparing these to the albums 
    returned by spotify use as a filter 
'''

def check_bad(title):
    bad = [
        "best of",
        "presents",
        "compilation",
        "greatest hits",
        "singles collection",
        "collection",
        "remix",
        "remixed",
        "extended edition",
        "tapes",
        "reissue",
        "unfinished",
        "deluxe",
        "special edition"
    ]
    for b in bad:
        if (b in title.lower()):
            return True
    return False


def clean_alb_title(title, release):
    remove = [
        f"({release} Remaster)",
        f"{release} Remaster",
        "(Extended Edition)",
        "- Extended Edition",
        "Extended Edition",
        "(Special Edition)",
        "Special Edition",
        "(Remastered)",
        "Remastered",
        "(Remaster)",
        "Remaster",
    ]
    for r in remove:
        pos = title.find(r)
        if (pos > -1):
            return title[0:pos].strip()
    return title

def clean_song_title(title):
    remove = [
        "(Remastered)",
        "(Remaster)",
        "(Special Edition)",
        " - Remastered",
        " - Remaster",
        "Special Edition",
        "Remastered",
        "Remaster"
    ]
    for r in remove:
        pos = title.find(r)
        if (pos > -1):
            return title[:pos].strip()
    return title