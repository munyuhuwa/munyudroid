# -*- coding:utf-8 -*-

# ライブラリ
import tweepy
import time

# 自作モジュール
import th
import re


def time_text():
	return time.strftime("%y%m%d%H%M%S")


CK = ''
CS = ''
AT = ''
ATS = ''

BOT_SCREEN_NAME = 'munyudroid'

auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, ATS)


# restのオブジェクト
api = tweepy.API(auth)

class Listener(tweepy.StreamListener):
	def on_status(self, status):
		print(status.text)
		if status.user.screen_name != BOT_SCREEN_NAME:
			if re.search(u"ガチャ", status.text):
				ans = th.th()
				api.update_status(status = u'@{0} {1}\n{2}'.format(status.user.screen_name, ans, time_text()), in_reply_to_status_id = status.id)
		return True

	def on_error(self, status_code):
		print(str(status_code))
		return True


# streamのオブジェクト
listener = Listener()
stream = tweepy.Stream(auth, listener)


api.update_status(status = u'起動\n{0}'.format(time_text()))
stream.userstream()
