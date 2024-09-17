from artist_data import Artist, Album

'''
Writing functions to filter through album and song titles to avoid repeats

ex. Artist: Opeth

1995: Orchid

1995: Orchid - 2023 Abbey Road Remaster

    - We want to ignore the second album because it is a repeat

ex. Artist: Opeth

2003: Peacevill Presents... Opeth

    - We want to ignore this album because it is a compilation, not an official album
      (despite being listed as a regular album by Spotify...... >:( )

ex. Artist: Opeth

2010: In Live Concert at the Royal Albert Hall			

    - We want to ignore live albums (again despite being listed as a regular album)

'''

def filter_albums(album_objects):
    return 0