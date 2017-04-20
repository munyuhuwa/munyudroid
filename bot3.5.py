# -*- coding:utf-8 -*-

import os

import json
import requests
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session

import base64
import time

import re
import th4


os.environ['PYTHONIOENCODING'] = 'UTF-8'



# キーなど
CK = ''
CS = ''
AT = ''
ATS = ''

# 自分のscreen_name
BOT_SCREEN_NAME = 'munyudroid'



# REST関係
REST_UPDATE_URL = 'https://api.twitter.com/1.1/statuses/update.json'
REST_UPLOAD_URL = 'https://upload.twitter.com/1.1/media/upload.json'

# 投稿
# params == {'status': text, 'in_reply_to_status_id': id, 'media_ids': id2s}
def update_status(params):
	twitter = OAuth1Session(CK, CS, AT, ATS)
	req = twitter.post(REST_UPDATE_URL, params)
	return (req.status_code == 200)

# 投稿(時刻を表す文字列付き)
def update_status_f(params):
	n = int(time.strftime('%s'))
	b = n.to_bytes(4, 'big')
	s = base64.b64encode(b).decode('utf-8')
	params['status'] = params['status'] + '\n' + s
	update_status(params)

# 画像付き投稿
def upload_pictures(file_names):
	media_ids = []
	for file_name in file_names:
		twitter = OAuth1Session(CK, CS, AT, ATS)
		req = twitter.post(REST_UPLOAD_URL, files = {'media': open(file_name, 'rb')})
		if req.status_code != 200:
			return None
		media_id = json.loads(req.text)['media_id']
		media_ids.append(media_id)
	return media_ids



# ストリーミング関係
STREAM_URL = 'https://userstream.twitter.com/1.1/user.json?replies=all'

auth = OAuth1(CK, CS, AT, ATS)
r = requests.post(STREAM_URL, auth = auth, stream = True)

# ステータスコードを確認
if r.status_code == 200:
	print('connection ok')
else:
	print('error: {0}'.format(r.status_code))


# 起動時のツイート
update_status_f({'status': 'おはよう'})


#　タイムライン監視
for line in r.iter_lines():
	data = line.decode('utf-8')
	print(data)
	try:
		if len(data) > 0:
			status = json.loads(data)
			# ツイートのオブジェクトのとき
			if 'text' in status:
				print(status['text'].encode('utf-8'))
				# 自分以外のとき
				if ('user' in status) and (status['user']['screen_name'] != BOT_SCREEN_NAME):
					if re.search('ガチャ', status['text']):
						result = th4.call_bin()
						ans = th4.create_text(result)
						file_name = th4.create_picture(result)
						media_ids = upload_pictures([file_name])
						text = '@{} {}'.format(status['user']['screen_name'], ans)
						update_status_f({'status': text, 'in_reply_to_status_id': status['id'], 'media_ids': media_ids})
	except json.decoder.JSONDecodeError:
		print('json decode error')
		pass
	except:
		print('unknown error')
		pass

# 終了時のツイート
update_status_f({'status': 'おやすみ'})
