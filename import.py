from pymongo import MongoClient
from py2neo import Graph

# Connect to MongoDB
client = MongoClient('mongodb://mongodb:27017/')
db = client['spotify']
tracks = list(db.tracks.find({}))
artists = list(db.artists.find({}))
top_tracks = list(db.top.find({}))
top_artists = list(db.top_artists.find({}))

# Connect to Neo4j
graph = Graph("bolt://neo4j:7687", auth=("neo4j", "password"))

# Delete all nodes and relationships
graph.run("MATCH (n) DETACH DELETE n")

# Insert genres and ensure they are unique
for artist in artists:
    genres = artist.get('genres', ['Unknown'])
    for genre in genres:  # Insert all genres
        graph.run("MERGE (g:Genre {name: $genre})", genre=genre)

# Insert top genres and ensure they are unique
for artist in top_artists:
    genres = artist.get('genres', ['Unknown'])
    for genre in genres:  # Insert all top genres
        graph.run("MERGE (g:TopGenre {name: $genre})", genre=genre)

# Insert top tracks separately
for track in top_tracks:
    graph.run("""
        MERGE (t:TopTrack {id: $track_id})
        ON CREATE SET t.name = $track_name, t.artist_name = $artist_name, t.album_name = $album_name
    """, track_id=track['track_id'], track_name=track['track_name'], artist_name=track['artist_name'], album_name=track['album_name'])

# Insert artists and connect them with their genres
for artist in artists:
    graph.run("""
        MERGE (a:Artist {id: $id})
        ON CREATE SET a.name = $name, a.popularity = $popularity
    """, id=artist['id'], name=artist['name'], popularity=artist['popularity'])
    genres = artist.get('genres', ['Unknown'])
    for genre in genres:  # Connect artist to all genres
        graph.run("""
            MATCH (a:Artist {id: $id})
            MATCH (g:Genre {name: $genre})
            MERGE (a)-[:HAS_GENRE]->(g)
        """, id=artist['id'], genre=genre)

# Insert top artists and connect them with their genres
for artist in top_artists:
    graph.run("""
        MERGE (a:TopArtist {id: $id})
        ON CREATE SET a.name = $name, a.popularity = $popularity
    """, id=artist['id'], name=artist['name'], popularity=artist['popularity'])
    genres = artist.get('genres', ['Unknown'])
    for genre in genres:  # Connect top artist to all top genres
        graph.run("""
            MATCH (a:TopArtist {id: $id})
            MATCH (g:TopGenre {name: $genre})
            MERGE (a)-[:HAS_GENRE]->(g)
        """, id=artist['id'], genre=genre)

# Insert tracks and connect them with artists and albums
for track in tracks:
    # Create album node
    graph.run("""
        MERGE (al:Album {id: $album_id})
        ON CREATE SET al.name = $album_name
    """, album_id=track['album_id'], album_name=track['album_name'])

    # Create track node
    graph.run("""
        MERGE (t:Track {id: $track_id})
        ON CREATE SET t.name = $track_name
    """, track_id=track['track_id'], track_name=track['track_name'])

    # Connect the track to the artist
    graph.run("""
        MATCH (t:Track {id: $track_id})
        MATCH (a:Artist {id: $artist_id})
        MERGE (t)-[:PERFORMED_BY]->(a)
    """, track_id=track['track_id'], artist_id=track['artist_id'])
    
    # Connect the track to the album
    graph.run("""
        MATCH (t:Track {id: $track_id})
        MATCH (al:Album {id: $album_id})
        MERGE (t)-[:PART_OF]->(al)
    """, track_id=track['track_id'], album_id=track['album_id'])

# Insert top tracks and connect them with artists and albums
for track in top_tracks:
    # Create top album node
    graph.run("""
        MERGE (al:TopAlbum {id: $album_id})
        ON CREATE SET al.name = $album_name
    """, album_id=track['album_id'], album_name=track['album_name'])

    # Create top track node
    graph.run("""
        MERGE (t:TopTrack {id: $track_id})
        ON CREATE SET t.name = $track_name
    """, track_id=track['track_id'], track_name=track['track_name'])

    # Connect the top track to the top artist
    graph.run("""
        MATCH (t:TopTrack {id: $track_id})
        MATCH (a:TopArtist {id: $artist_id})
        MERGE (t)-[:PERFORMED_BY]->(a)
    """, track_id=track['track_id'], artist_id=track['artist_id'])
    
    # Connect the top track to the top album
    graph.run("""
        MATCH (t:TopTrack {id: $track_id})
        MATCH (al:TopAlbum {id: $album_id})
        MERGE (t)-[:PART_OF]->(al)
    """, track_id=track['track_id'], album_id=track['album_id'])

# Verification
print("Total Genres: ", graph.evaluate("MATCH (g:Genre) RETURN count(g)"))
print("Total Top Genres: ", graph.evaluate("MATCH (g:TopGenre) RETURN count(g)"))
print("Total Artists: ", graph.evaluate("MATCH (a:Artist) RETURN count(a)"))
print("Total Top Artists: ", graph.evaluate("MATCH (a:TopArtist) RETURN count(a)"))
print("Total Tracks: ", graph.evaluate("MATCH (t:Track) RETURN count(t)"))
print("Total Top Tracks: ", graph.evaluate("MATCH (t:TopTrack) RETURN count(t)"))
print("Total Albums: ", graph.evaluate("MATCH (al:Album) RETURN count(al)"))
print("Total Top Albums: ", graph.evaluate("MATCH (al:TopAlbum) RETURN count(al)"))