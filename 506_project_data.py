
import requests
import webbrowser
import json

#New York Times Data
nyt_ref = open("nyt_top_stories.txt","r")
nyt_str = nyt_ref.read()
nyt_data = json.loads(nyt_str)
print nyt_data
print nyt_data.keys()

#Twitter Data
#client_key = "AG9rqPpNtYug1KZy6YkUNc8nj" 
#client_secret = "to9vCIqZfkN7CCeXEec88BPYNTePqRTys3AzmZ5vxMqlsMZ8iK" 
