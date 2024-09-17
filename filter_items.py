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
    return 0