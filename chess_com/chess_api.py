import json
from requests_html import HTMLSession

'''
HTTP Responses from Chess.com
200 = "enjoy your JSON"
301 = if the URL you requested is bad, but we know where it should be; your client should remember and correct this to use the new URL in future requests
304 = if your client supports "ETag/If-None-Match" or "Last-Modified/If-Modified-Since" caching headers and the data have not changed since the last request
404 = we try to tell you if the URL is malformed or the data requested is just not available (e.g., a username for a user that does not exist)
410 = we know for certain that no data will ever be available at the URL you requested; your client should not request this URL again
429 = we are refusing to interpret your request due to rate limits; see "Rate Limiting" above
'''

session = HTMLSession()

def chess_com_data(url_endpoint):
	response = session.get(url_endpoint)
	return json.loads(response.html.html)

def archived_games(archive_endpoint):
	"""returns a list of monthly endpoints"""
	return chess_com_data(archive_endpoint)['archives']

def monthly_games(monthly_endpoint):
	"""returns a list of dictionaries, where each dictionary contains game information"""
	return chess_com_data(monthly_endpoint)['games']

def player_info(player_endpoint):
	"""returns a dictionary of player info"""
	return chess_com_data(player_endpoint)