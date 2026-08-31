import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

key = os.getenv("AZURE_LANGUAGE_KEY")
endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = [
     "The Weeknd hinted at the After Hours Til Dawn tour possibly being his last performance under that stage name.",
    "Fans are reacting with a mix of excitement and nostalgia as Abel Tesfaye moves away from The Weeknd persona.",
    "After Hours Til Dawn drew massive crowds, with many fans calling it an emotional farewell tour.",
    "Speculation about the rebrand has dominated music news cycles, with some fans worried and others intrigued.",
    "Drake shocked fans by ending his final promotional livestream for his new album Iceman by pulling out three hard drives to show he was dropping three albums at once.",
  "The surprise releases achieved the highest streaming numbers of Drake's career within the first 24 hours.",
    "Fans praised the surprise drop as one of the boldest moves of Drake's career.",
    "Speculation is growing about whether Drake will announce a tour to support the new albums.",
]

response = client.analyze_sentiment(documents)

for doc in response:
    print(f"Sentiment: {doc.sentiment}")
    print(f"Positive: {doc.confidence_scores.positive}")
    print(f"Neutral: {doc.confidence_scores.neutral}")
    print(f"Negative: {doc.confidence_scores.negative}")