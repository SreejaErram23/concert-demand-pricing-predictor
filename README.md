Concert Demand & Ticket Pricing Predictor 

The Weeknd (Abel Tesfaye) & Drake: A Predictive Analysis Case Study 

Overview
This product builds an end to end predictive analysis pipeline for a concert promoter, forecasting ticket demand and recommended pricing for two real touring artists: The Weeknd (Abel Tesfaye) and Drake. It pulls together a relational database, AI driven sentiment analysis, a machine learning regression model, and an interactive Power BI dashboard.  

Given the artist's current public buzz, venue size, and a city's market, the model estimates expected demand and recommends a ticket price. That prediction is then compared against real, documented tour outcomes to see how well the logic actually holds up.

Why These Two Artists 
The Weeknd and Drake were chosen on purpose, and not just because they are two favorite artists, but because each one represents a genuinely different kind of demand forecasting challenge a promoter might actually face. 
The Weeknd (Abel Tesfaye) is in the middle of a rebrand. His After Hours Til Dawn tour was confirmed as his last run performing under “The Weeknd,” with future work expected under his birth name, Abel Tesfaye. Fans are wondering if his music will change along with his name. A promoter booking his next tour would have real uncertainty about whether demand holds steady through an identity change like that.
Drake released two albums (Habibti and Maid of Honour) from his planned album Iceman in a single night with almost no warning. These releases generated a massive streaming spike but no announced tour. This tests whether that kind of streaming buzz actually translates into concert demand.

Tech Stack


Database: SQLite (via DB Browser for SQLite)
Data cleaning and modeling: Python (pandas and scikit-learn)
Sentiment analysis: Azure AI Language (Text Analytics, Free F0 tier)
Visualization: Power BI



Project Architecture 
The general flow of the project looks like this: real tour data lives in SQL, Python (pandas) pulls that data together along with the Azure buzz score, feeds it into the regression model, and then the models output get written back into the Predicted_Demand table, which then powers the Power BI dashboard.

Database Schema
Five normalized tables were built and populated with real, sourced data.
Artists: artist_id, name, genre, spotify_listeners, billboard_chart_position (used here as Spotify global rank), current_status, buzz_score
Venues: holds venue name, type, city, state, capacity, and metro population, one row per real venue used on either tour
Tour_Dates: tour_date_id, venue_id (FK), artist_id (FK), date, tour_name, supporting_acts, actual_demand_percent
Ticket_Prices: holds price tier and average price, one row per tier per show, linked back to Tour_Dates
Predicted_Demand: predicted_demand_id, tour_date_id (FK), predicted_demand, recommended_price (this is the model's output)

The reference data covers 26 real U.S. tour dates: The Weeknd’s 2025 After Hours Til Dawn stadium leg (13 shows) and Drake's 2023–2024 It’s All a Blur arena tour (13 shows, spanning both the 21 Savage leg and J.Cole leg).

Predictive Model
Features used: 
buzz_score, derived from Azure AI Language sentiment analysis (as described below)
capacity, the venue size
metro_population, a proxy for city market size, sourced from US Census MSA figures
day_of_week, derived from the show date
spotify_listeners, an artist popularity proxy
Target variable: actual_demand_percent, the real, sourced venue sell through percentage.
Model: a scikit-learn LinearRegression model, with features scaled using StandardScaler, trained and tested with an 80/20 split.
Pricing Logic: the recommended price is calculated like this: 
Recommended_price = artist’s baseline average price x (predicted_demand /  artists average demand)
This scales the price up or down proportionally, based on how a show’s predicted demand compares to that artists typical demand.

Azure AI Language: Buzz Score
Buzz score is one input feature for each artist based on sentiment analysis of eight short, paraphrased news snippets (four per artist), describing what's going on with each of them. 
Buzz scores: 
The Weeknd: 0.055
Drake: 0.025

A Limitation Found During Testing:
One of the Drake snippets, “Streaming numbers for the surprise releases broke records within the first 24 hours”, was misread by Azure as 68 percent negative, even though it describes good news. This turned out to be a known limitation of automated sentiment analysis tools: dramatic or record breaking language can read as negative to the model even when the event is positive. 
Once this was caught, the snippet was revised to “The surprise releases set Spotify's biggest single day streaming record of 2026, within its first 24 hours”, which kept the same general positive meaning but read more clearly, and Azure correctly scored it as positive after that (Positive: 0.17, Negative: 0.0). 

Actual Demand Data: Sourcing and Limitations
City by city ticket attendance isn't something that gets published for most tours, so a decision was made on how to build actual_demand_percent in a way that stayed accurate to the real data.
Real, sourced figures were used where they could be found: The Weeknd’s Phoenix opener (60,000 out of 63,400 capacity, about 95 percent) and Drake's Washington DC shows (34,303 combined attendees across 2 nights out of 20,356 capacity, about 84 percent).
For every other show, that artist’s documented tour wide sellout rate was applied uniformly. The Weeknd’s 2025 leg is reported to have 40+ sold out stadium shows, so 95 percent was applied, and Drake’s It's All a Blur tour is documented as 100 percent sold out across all 80 shows.

A Limitation Found: 
A key limitation is that most shows on an artist's tour have similar demand, leaving limited city to city variation for the model to learn from. The model correctly predicted 5 out of the 6 held out shows, but this likely reflects learning the artists more than city level demand. The one outlier, Washington, DC at 84%, was also the only prediction it missed. The model predicted 100% instead. A larger, more detailed dataset would be needed to build a more sophisticated demand model. 

Ticket Pricing Data 
For tier level pricing (Floor, Lower Bowl, Upper Bowl, VIP Booth), publicly reported price ranges for each tour were used and applied as a consistent per artist average across all of that artist shows, since exact per city, per tier pricing fully available.

Dashboard
Page 1: Demand Overview: 
Predicted versus actual demand by city shown separately for each artist 
A geographic map of the tour cities (ArcGIS for Power BI was used here, since JMU’s tenant policy blocks standard Bing Maps visual), with bubble size based on venue capacity and color coded by artist 
Page 2: Pricing Strategy
Recommended ticket price by city, color coded by artist
Average ticket price by tier and artist, shown as a donut chart 

Key takeaways: 
For predictive modeling, a small, mostly uniform dataset limits how much genuine city to city distinction a model can actually pick up on, even when the overall test accuracy looks strong on the surface. 
Automated sentiment analysis can misread factually positive language as negative. Catching and correcting this error showed the importance of reviewing AI generated results rather than relying on the tool without verification. 
