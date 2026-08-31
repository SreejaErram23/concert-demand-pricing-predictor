import sqlite3
import pandas as pd

conn = sqlite3.connect('concert_demand.db')

query = """
SELECT 
    Tour_Dates.date,
    Artists.name,
    Artists.buzz_score,
    Artists.spotify_listeners,
    Venues.venue_name,
    Venues.capacity,
    Venues.metro_population
FROM Tour_Dates
JOIN Artists ON Tour_Dates.artist_id = Artists.artist_id
JOIN Venues ON Tour_Dates.venue_id = Venues.venue_id;
"""

df = pd.read_sql_query(query, conn)
print(df)

conn.close()

