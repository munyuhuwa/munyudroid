# -*- coding:utf-8 -*-

import commands
import time

def th():
	start = time.time()
	result = commands.getoutput('./th.exe').strip().split(',')
	# print result
	duration = time.time() - start
	# print duration

	text = ''
	manzu_chars = u'☆一二三四五六七八九'
	souzu_chars = u'☆１２３４５６７８９'
	pinzu_chars = u'☆①②③④⑤⑥⑦⑧⑨'
	jihai_chars = u'☆東南西北白発中'

	for i in range(0, len(result[0])):
		text += manzu_chars[int(result[0][i])]
	for i in range(0, len(result[1])):
		text += souzu_chars[int(result[1][i])]
	for i in range(0, len(result[2])):
		text += pinzu_chars[int(result[2][i])]
	for i in range(0, len(result[3])):
		text += jihai_chars[int(result[3][i])]

	type_text = u'七対子' if result[4][0] == 's' else (u'国士無双' if result[4][0] == 't' else u'基本形')
	text = u'おめでとうございます！\n{0} ({1})\n{2}回の挑戦の結果、天和が出ました。\n実行時間: {3:.6f}s'.format(text, type_text, result[5], duration)

	# print text
	return text
