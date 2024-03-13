import json
import requests

search_word = 'hyde'
response = requests.get ("http://gutendex.com/books/?search=" + search_word)
data = json.loads (response.content)
print (data)
