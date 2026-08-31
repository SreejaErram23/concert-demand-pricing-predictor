from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import sqlite3
import pandas as pd

conn = sqlite3.connect('concert_demand.db')
query = """
SELECT 
    Tour_Dates.tour_date_id,
    Tour_Dates.date,
    Tour_Dates.actual_demand_percent,
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
conn.close()

df['date'] = pd.to_datetime(df['date'])
df['day_of_week'] = df['date'].dt.dayofweek
print(df[['date', 'day_of_week', 'actual_demand_percent']])

X = df[['buzz_score', 'capacity', 'metro_population', 'day_of_week', 'spotify_listeners']]
y = df['actual_demand_percent']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
_, names_test = train_test_split(df['name'], test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train_scaled, y_train)

predictions = model.predict(X_test_scaled)

print("\nPredictions vs Actual:")
for pred, actual in zip(predictions, y_test):
    print(f"Predicted: {pred:.2f}%  |  Actual: {actual:.2f}%")

avg_demand_by_artist = df.groupby('name')['actual_demand_percent'].mean()

baseline_price_by_artist = {
    'The Weeknd': 475,
    'Drake': 600
}

print("\nRecommended Prices:")
for pred, actual, artist in zip(predictions, y_test, names_test):
    avg_demand = avg_demand_by_artist[artist]
    baseline = baseline_price_by_artist[artist]
    recommended_price = baseline * (pred / avg_demand)
    print(f"{artist}: Predicted Demand {pred:.2f}%  |  Recommended Price: ${recommended_price:.2f}")

X_all_scaled = scaler.transform(X)
df['predicted_demand'] = model.predict(X_all_scaled)

def calculate_price(row):
    baseline = baseline_price_by_artist[row['name']]
    avg_demand = avg_demand_by_artist[row['name']]
    return baseline * (row['predicted_demand'] / avg_demand)

df['recommended_price'] = df.apply(calculate_price, axis=1)

print("\nFull dataset with predictions:")
print(df[['date', 'name', 'actual_demand_percent', 'predicted_demand', 'recommended_price']])


conn = sqlite3.connect('concert_demand.db')
cursor = conn.cursor()

for index, row in df.iterrows():
    cursor.execute(
        "INSERT INTO Predicted_Demand (tour_date_id, predicted_demand, recommended_price) VALUES (?, ?, ?)",
        (row['tour_date_id'], row['predicted_demand'], row['recommended_price'])
    )

conn.commit()
conn.close()

print("\nPredictions written to database successfully.")