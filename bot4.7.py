# -*- coding:utf-8 -*-

import os

import json
import requests
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session

import base64
import time
import re
import threading

import th4
from op import OpPy
from streamlog import StreamLog
# オタク構文を使用
from wx import WotakuExp

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
	# if req.status_code == 200:
	# 	print('ok')
	# else:
	# 	print('Error: {}'.format(req.status_code))
	return (req.status_code == 200)

# 投稿(時刻を表す文字列付き)
def update_status_f(params):
	n = int(time.strftime('%s'))
	b = n.to_bytes(4, 'big')
	s = base64.b64encode(b).decode('utf-8')
	params['status'] = params['status'] + '\n' + s[:-2]
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



# 別スレッドでの処理
class TestThread(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while True:
			text = WotakuExp().generate()
			update_status({'status': text})
			time.sleep(600)

test_thread = TestThread()
test_thread.setDaemon(True)
test_thread.start()



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

# 諸機能の読み込み
oppy = OpPy()
streamlog = StreamLog()

#　タイムライン監視
for line in r.iter_lines():
	data = line.decode('utf-8')
	print(data)
	try:
		if len(data) > 0:
			status = json.loads(data)
			# ツイートのオブジェクトのとき
			if 'text' in status:
				# print(status['text'].encode('utf-8'))
				# ツイートを保存
				streamlog.save(data)
				# 自分以外のとき
				if ('user' in status) and (status['user']['screen_name'] != BOT_SCREEN_NAME):
					# 文章変換
					ans = oppy.interprete(status['text'])
					if (ans):
						if ans == '開始します。' or ans == '終了しました。':
							update_status_f({'status': ans})
						else:
							update_status({'status': ans})
					# 天鳳ガチャ
					if re.search('ガチャ', status['text']):
						result = th4.call_bin()
						ans = th4.create_text(result)
						file_name = th4.create_picture(result)
						media_ids = upload_pictures([file_name])
						text = '@{} {}'.format(status['user']['screen_name'], ans)
						update_status_f({'status': text, 'in_reply_to_status_id': status['id'], 'media_ids': media_ids})
					# 自分へのリプのとき
					# 会話
					if status['in_reply_to_screen_name'] == BOT_SCREEN_NAME:
						ans = '@{} {}'.format(status['user']['screen_name'], WotakuExp().generate())
						update_status({'status': ans, 'in_reply_to_status_id': status['id']})
	except json.decoder.JSONDecodeError:
		print('json decode error')
		pass
	except:
		print('unknown error')
		pass

# 終了時
test_thread.stop()
# 終了時のツイート
update_status_f({'status': 'おやすみ'})
