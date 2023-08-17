from googleapiclient.discovery import build

# Replace with your API key
API_KEY = 'AIzaSyAB1n-r48JillEO7DDFGphdxa9QCNCyxvk'

def search_channels_by_keyword(keyword):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    search_response = youtube.search().list(
        q=keyword,
        type='channel',
        part='id',
        maxResults=50  # Adjust this number as needed
    ).execute()

    channel_ids = [item['id']['channelId'] for item in search_response.get('items', [])]
    return channel_ids

keyword = 'Quizie'
channel_ids = search_channels_by_keyword(keyword)

for channel_id in channel_ids:
    print(f"Channel ID: {channel_id}")
