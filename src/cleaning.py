import pandas as pd
import os

songs = []
unicode = ["\u2005", "\u205f"]
rows = []


# Exclusion list - (removing rows/text files manually - prologues, remixes, messages, poems )
files_to_remove = ["1989_TaylorsVersion__Prologue_", "Forever_Always_PianoVersion__TaylorsVersion_",
                   "LoveStory_TaylorsVersion__ElviraRemix_", "SnowOnTheBeach_feat_MoreLanaDelRey_",
                   "Karma_Remix_", "AllTooWell_TaylorsVersion_", "AMessageFromTaylor",
                   "StateOfGrace_AcousticVersion__TaylorsVersion_", "IfYoureAnythingLikeMe_Poem_",
                   "Reputation_Prologue_", "ReputationMagazineVol_1", "WhySheDisappeared_Poem_",
                   "TeardropsonMyGuitar_PopVersion_", "TaylorSwift_LinerNotes_"]

albums = ["1989_TaylorsVersion_", "Evermore", "Fearless_TaylorsVersion_", "Folklore", "Lover",
          "Midnights_TheTillDawnEdition_", "Red_TaylorsVersion_", "Reputation", "SpeakNow_TaylorsVersion_",
          "TaylorSwift", "THETORTUREDPOETSDEPARTMENT_THEANTHOLOGY"]

# Nested iteration, albums > songs
for album in albums:

    album_path = os.path.join("../data/raw/Albums/", album)
    album_songs = os.listdir(album_path)

    for song in album_songs:
        full_path = os.path.join(album_path, song)
        song_lyrics = []

        song_title = song[:-4]

        if song_title not in files_to_remove:

            with open(full_path, mode='r', encoding='utf-8') as file:

                for line in file:
                    line = line.strip()

                    for code in unicode:
                        line = line.replace(code, " ")

                    if "Embed" in line:
                        line = line.split("Embed")[0]
                        line = line.rstrip("0123456789")

                    if '[' not in line and line:
                        song_lyrics.append(line)

                joined = " ".join(song_lyrics)
                songs.append(joined)

                rows.append(
                    {
                        "album": album,
                        "song": song_title,
                        "lyrics": joined,
                    }
                )

song_df = pd.DataFrame(rows, columns=["album", "song", "lyrics"])

rename_albums = {
    'THETORTUREDPOETSDEPARTMENT_THEANTHOLOGY': 'TTPD',
    'Midnights_TheTillDawnEdition_': 'Midnights',
    'Fearless_TaylorsVersion_': 'Fearless (TV)',
    'SpeakNow_TaylorsVersion_': 'Speak Now (TV)',
    'Red_TaylorsVersion_': 'Red (TV)',
    '1989_TaylorsVersion_': '1989 (TV)'
}

song_df['album'] = song_df['album'].replace(rename_albums)
# print(song_df.head())

# saving the final cleaned dataset to the processed data folder
song_df.to_csv("../data/processed/processed_song_data.csv", index=False)