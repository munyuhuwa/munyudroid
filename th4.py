# -*- coding:utf-8 -*-

from PIL import Image
import time
import random
import subprocess


# バイナリを呼び出して結果を取得
# result = {萬子, 索子, 筒子, 字牌, 和了形, 挑戦回数, 実行時間}
def call_bin():
	start = time.time()
	result = subprocess.check_output('./th.exe', shell = True).decode('utf-8').strip().split(',')
	duration = time.time() - start
	result.append(duration)
	return result


# 結果のテキスト生成
def create_text(result):
	type_text = '七対子' if result[4][0] == 's' else ('国士無双' if result[4][0] == 't' else '基本形')
	text = 'おめでとうございます！\n{0}回の挑戦の結果、天和({1})が出ました。\n実行時間: {2:.6f}s'.format(result[5], type_text, result[6])
	return text


# 牌姿を画像化して出力
# 牌の画像はディレクトリtiles/に入れてください
# 出力画像用のディレクトリout/をあらかじめ用意してください
def create_picture(result):
	canvas = Image.new('RGB', (640, 128), (255, 255, 255))
	x = 40
	y = 38
	prefix = ('m', 'p', 's', 'j')
	for m in range(4):
		for n in result[m]:
			file_name = 'tiles/{}{}.png'.format(prefix[m], n)
			tile = Image.open(file_name, 'r')
			canvas.paste(tile, (x, y))
			x += 40
	file_name = 'out/' + time.strftime('%s') + str(random.randrange(1000)) + '.png'
	canvas.save(file_name, 'PNG', optimize = True)
	return file_name
