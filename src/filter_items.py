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
        "(live)"
        " live",
        "live ",
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
        "instrumental",
        "cover",
        "bootleg",
        "anniversary",
        "demos",
        "demo",
        "world tour",
        "recordings",
        "livetime",
        "lost not forgotten archives"
    ]
    for b in bad:
        if b in title.lower():
            return True
    return False

def check_bad_song(title):
    bad = [
        "(live)",
        " live",
        "(cover)",
        " cover",
        "-instrumental",
        "(instrumental)",
        " instrumental",
        "(demo)",
        " demo",
        "(acoustic)",
        " acoustic",
    ]
    for b in bad:
        if b in title.lower():
            return True
    return False

def clean_alb_title(title, release):
    remove = [
        f"({release} remaster)",
        f"{release} remaster",
        "(re-issue",
        "(reissue",
        "(extended edition)",
        "- extended edition",
        "extended edition",
        "(special edition)",
        "special edition",
        "(remastered)",
        "remastered",
        "(remaster)",
        "remaster",
        "(deluxe",
        "deluxe",
        "- reloaded",
        "(reloaded)",
        "reloaded",
        "(bonus",
        "bonus"
    ]
    for r in remove:
        pos = title.lower().find(r)
        if pos > -1:
            return title[0:pos].strip()
    return title

def clean_song_title(title):
    remove = [
        " - ",
        "(remastered)",
        "(remaster)",
        "(special edition)",
        " - remastered",
        " - remaster",
        "special edition",
        "remastered",
        "remaster",
        "(bonus track)",
        "bonus track",
        "(bonus)",
        "bonus"
    ]
    for r in remove:
        pos = title.lower().find(r)
        if pos > -1:
            return title[:pos].strip()
    return title