
"""to do list
clean the code so humans can read it also
"""

##########		libs		##########
import websocket, json, threading, time, urllib;from bs4 import BeautifulSoup as bs
##########		infos		##########
channel = input('channel:\n>>');trip = input('passwd:\n>>');nick = input('nick:\n>>')
if trip == None:
	pass
else:
	nick = nick + '#' + trip
##########		functions		##########
def _send_msg(msg):
	_send({"cmd": "chat", "text": msg})
def _send(pkg):
	encoded = json.dumps(pkg);ws.send(encoded)
def _send_msg_in_chat():
	while True:
		msg = input();		_send({"cmd": "chat", "text": msg})
def _search_tube(_input):
	a=0
	if _input['cmd']=='chat' and len(_input['text'].strip())>9 and '`search ' in _input['text']:
		_input=_input['text']
		term=_input[8::]
		encoded_search = urllib.parse.quote(term)
		print(encoded_search)
		url='https://youtube.com/results?search_query='+encoded_search
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req)
		output=bs(response,'html.parser')
		_result=[]
		for vid in output.select(".yt-uix-tile-link"):
			if a<1:
				if vid["href"].startswith("/watch?v="):
					a+=1
					vid_info = {"title": vid["title"], "link": vid["href"], "id": vid["href"][vid["href"].index("=")+1:]}
					title=vid_info['title']
					link=vid_info['link']
					url='https://youtube.com'+link
					_send_msg(url)
def _search_mtube(_input):
	a=0
	if _input['cmd']=='chat' and len(_input['text'].strip())>10 and '`msearch ' in _input['text']:
		_input=_input['text']
		term=_input[9::]
		encoded_search = urllib.parse.quote(term)
		print(encoded_search)
		url='https://youtube.com/search?q='+encoded_search
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req)
		output=bs(response,'html.parser')
		_result=[]
		for vid in output.select(".yt-uix-tile-link"):
			if a<1:
				if vid["href"].startswith("/watch?v="):
					a+=1
					vid_info = {"title": vid["title"], "link": vid["href"], "id": vid["href"][vid["href"].index("=")+1:]}
					title=vid_info['title']
					link=vid_info['link']
					url=title+'\t'+'https://music.youtube.com'+link
					_send_msg(url)
def wttr(_input):
	if _input['cmd']=='chat' and  len(_input['text'].strip())>7 and '`wttr ' in _input['text']:
		_input=_input['text']
		term=_input[6::]
		encoded_search = urllib.parse.quote(term)
		print(encoded_search)
		url='https://wttr.in/'+encoded_search+'?format=4'
		output=urllib.request.urlopen(url)
		output=bs(output,'html.parser')
		output=str(output)
		print(output)
		_send_msg(output)
		
def drug_wiki(_input):
	a=0
	if _input['cmd']=='chat' and  len(_input['text'].strip())>7 and '`drug ' in _input['text']:
		_input=_input['text']
		term=_input[6::]
		encoded_search = urllib.parse.quote(term)
		print(encoded_search)
		url='https://psychonautwiki.org/w/index.php?title=Special:Search&_=&search='+encoded_search
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req)
		output=bs(response,'html.parser')
		print(output)
		for drug in output.find_all('a', href=True):
			print(drug)
			if a<1:
				if drug["href"].startswith("/wiki"):
					a+=1
					drug_info = {"title": drug["title"], "link": drug["href"]}
					title=drug_info['title']
					link=drug_info['link']
					url=title+':\n'+'* http://psychonaut3z5aoz.onion'+link
					_send_msg(url)
		
def commands():
	while True:
		_input=json.loads(ws.recv())
		if _input['cmd']=='chat' and '`wttr ' in _input['text']:
			_send_msg('be patient tor being tor')
			wttr(_input)
		elif _input['cmd']=='chat' and '`msearch ' in _input['text']:
			_send_msg('be patient tor being tor')
			_search_mtube(_input)
		elif _input['cmd']=='chat' and '`search ' in _input['text']:
			_send_msg('be patient tor being tor')
			_search_tube(_input)
		elif _input['cmd']=='chat' and '`drug ' in _input['text']:
			_send_msg('$\\tiny\\text{be patient tor being tor}$')
			drug_wiki(_input)
##########		connections & commands/logs			##########
ws = websocket.create_connection('wss://hack.chat/chat-ws')
_send({"cmd": "join", "channel": channel, "nick": nick})
commands=threading.Thread(target=commands).start()
msg = threading.Thread(target=_send_msg_in_chat).start()
