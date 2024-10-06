# Nick's Music Ratings

Inspiration for spreadsheet [here](https://docs.google.com/spreadsheets/d/1xHZ8XMuCCnNd88tfcPiWxfFuq6EHfB9t3V-EMD7jm6M/edit?usp=sharing)

Spreadsheet maintained by the code in this repository [here](https://docs.google.com/spreadsheets/d/1Jc7roe2tmtVx-0hdn6DPI2zDh6NcPyWLBMVZN20a5WM/edit?usp=sharing)

### Functionality to implement:

- [x] Access spreadsheet
- [x] Format artist albums
    - [X] Re-implement as batch updates
- [x] Format arist non-album section
    - [X] Re-implement as batch updates
- [x] Design new "home" page
    - [x] Embed link to generated spreadsheet in cell
- [ ] Make spreadsheets update upon new releases (w/o overwriting)
    - [ ] Deploy web hook on cloud to accomplish
- [ ] Generate new sheets when band name added to list
- [ ] Trigger python scripts when specific cells update
    - [ ] Create new sheet for artist entered on List of Artists sheet
    - [ ] Bold + color change highest rated song on album
    - [ ] Update top 10 songs
    - [ ] update album rankings
- [ ] Stat diagnostic for each artist page
    - [ ] Average song rating per album
    - [ ] Average album rating
- [ ] Compile database of my ratings
    - [ ] AI model to recommend me music based on rankings?
- [x] Access spotify api
- [x] Get band data
    - [x] List of album titles
        - [x] Filter out live albums and repeat releases
        - [ ] Add backup filter protocols if others fail
    - [x] List of songs for each album
    - [x] Song lengths
    - [x] Album release years
    - [x] Get album cover pictures
    - [x] Make an Artist class
    - [x] Make an Album class
- [ ] Create Playlists based on song ratings
    - [ ] 8+ songs go in playlist, etc.