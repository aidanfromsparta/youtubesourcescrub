import streamlit as st
import streamlit as st
from googleapiclient.discovery import build

# YouTube Data API setup
API_KEY = "YOUR_YOUTUBE_API_KEY"  # Replace with your YouTube Data API key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def search_youtube_videos(artist_name):
    """
    Search for videos related to the artist's topic page and extract metadata.
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    # Search for the artist's videos using a query
    search_response = youtube.search().list(
        q=artist_name + " topic",
        part="snippet",
        maxResults=50  # Adjust the max results as needed
    ).execute()

    # Filter and return video IDs
    video_ids = [
        item["id"]["videoId"]
        for item in search_response.get("items", [])
        if item["id"]["kind"] == "youtube#video"
    ]
    return video_ids

def get_video_metadata(video_ids):
    """
    Fetch video details and extract the 'Provided to YouTube by...' text.
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    video_details = youtube.videos().list(
        part="snippet,contentDetails",
        id=",".join(video_ids)
    ).execute()

    extracted_text = []
    for video in video_details.get("items", []):
        description = video["snippet"].get("description", "")
        if "Provided to YouTube by" in description:
            extracted_text.append(description)
    return extracted_text

# Streamlit app
st.title("YouTube Topic Page Scraper")
st.write("Enter an artist name to search for videos and extract 'Provided to YouTube by...' details.")

# Input form
artist_name = st.text_input("Artist Name", "")

if artist_name:
    with st.spinner("Searching for videos..."):
        video_ids = search_youtube_videos(artist_name)
        if not video_ids:
            st.warning("No videos found for the given artist.")
        else:
            with st.spinner("Fetching video details..."):
                extracted_texts = get_video_metadata(video_ids)
                if extracted_texts:
                    st.success(f"Found {len(extracted_texts)} videos with 'Provided to YouTube by...' text.")
                    for text in extracted_texts:
                        st.text_area("Extracted Text", text, height=100)
                else:
                    st.warning("No 'Provided to YouTube by...' text found in the videos.")

