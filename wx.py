import MeCab
import random
import subprocess

CORPUS_FILE_NAME = 'wx-corpus.txt'# 例文集はテキストファイル(UTF-8)
CORPUS_NUMBER_OF_LINES = 100000# 例文集の行数を設定
STRUCTURE_FILE_NAME = 'wx-structures.txt'# 構文集のファイル名


class WotakuExp:
	def __init__(self):
		# MeCabの準備
		self.tagger = MeCab.Tagger('-Ochasen')
		self.tagger.parse('')


	def get_verb_phrases(self, text):
		morpho = list(map( lambda x: x.split(), self.tagger.parse(text).split('\n') ))
		phrases = []
		for i in range(len(morpho)):
			if len(morpho[i]) >= 4 and morpho[i][3].startswith('動詞-自立'):
				phr = morpho[i][2]# フレーズに原形を追加
				buf = ''# 文節の切れ目に対応するためのバッファ
				j = i - 1
				while j >= 0:
					if len(morpho[j]) < 4:
						break
					# 文頭のほうへ辿っていく
					surface = morpho[j][0]
					hinshi = morpho[j][3]
					if '助詞' in hinshi:
						buf = surface
					elif '名詞' in hinshi or '接頭詞' in hinshi or '接尾詞' in hinshi:
						phr = surface + buf + phr
						buf = ''
					elif '副詞' == hinshi:
						phr = surface + buf + phr
						buf = ''
					else:
						break
					j -= 1
				phrases.append(phr)
		return phrases


	def get_noun_phrases(self, text):
		morpho = list(map( lambda x: x.split(), self.tagger.parse(text).split('\n') ))
		phrases = []
		i = 0
		while i < len(morpho):
			if len(morpho[i]) >= 4 and (morpho[i][3].startswith('名詞') or morpho[i][3].startswith('接頭詞')):
				phr = morpho[i][2]# フレーズに原形を追加
				buf = ''# 文節の切れ目に対応するためのバッファ
				j = i + 1
				while j < len(morpho):
					if len(morpho[j]) < 4:
						break
					# 文末のほうへ辿っていく
					surface = morpho[j][0]
					hinshi = morpho[j][3]
					if '形容詞' in hinshi or surface == 'の':
						buf = surface
					elif '名詞' in hinshi or '接頭詞' in hinshi or '接尾詞' in hinshi:
						phr = phr + buf + surface
						buf = ''
					else:
						i = j
						break
					j += 1
				phrases.append(phr)
			i += 1
		return phrases


	# 語形変化
	def inflect(self, verb, suffix):
		# 後続の単語の音便
		onbin = {
			'た': 'だ',
			'て': 'で',
			'たり': 'だり',
			# 以下「行く」の音便なし
			'み': None,
			'すぎ': None,
			'過ぎ': None,
			'たい': None,
		}
		if not (suffix in onbin):
			return None

		result = None

		# 不規則系・例外
		# 前が音便系、後ろが規則的な連用形
		irregulars = {
			'来る': ('来', '来'),
			'くる': ('き', 'き'),
			'する': ('し', 'し'),
			'行く': ('行っ', '行き'),
			'いく': ('いっ', 'いき'),
		}
		if verb[-2:] in irregulars:
			if onbin[suffix]:# 音便で判定するが後続単語は変化せず
				result = verb[:-2] + irregulars[verb[-2:]][0] + suffix
			else:
				result = verb[:-2] + irregulars[verb[-2:]][1] + suffix
		else:
			stem1 = verb[-1]
			stem2 = verb[-2]
			stem_to_i = {
				'る': 'り',
				'う': 'い',
				'つ': 'ち',
				'む': 'み',
				'ぶ': 'び',
				'ぬ': 'に',
				'く': 'き',
				'ぐ': 'ぎ',
				'す': 'し',
			}
			if stem1 == 'る' and stem2 in 'いきぎしじちぢにひびぴみりえけげせぜてでねへべぺめれ要居入射炒煎鋳似煮見視観診看覧得獲寝経出イキギシジチヂニヒビピミリエケゲセゼテデネヘベペメレ':
				# 上/下一段
				result = verb[:-1] + suffix
			elif stem1 in 'るうつ':
				# 五段
				if onbin[suffix]:
					result = verb[:-1] + 'っ' + suffix
				else:
					result = verb[:-1] + stem_to_i[stem1] + suffix
			elif stem1 in 'むぶぬ':
				if onbin[suffix]:
					result = verb[:-1] + 'ん' + onbin[suffix]
				else:
					result = verb[:-1] + stem_to_i[stem1] + suffix
			elif stem1 == 'く':
				if onbin[suffix]:
					result = verb[:-1] + 'い' + suffix
				else:
					result = verb[:-1] + stem_to_i[stem1] + suffix
			elif stem1 == 'ぐ':
				if onbin[suffix]:
					result = verb[:-1] + 'い' + onbin[suffix]
				else:
					result = verb[:-1] + stem_to_i[stem1] + suffix
			elif stem1 == 'す':
				result = verb[:-1] + 'し' + suffix
		return result


	def fit_to_structure(self, text, structure):
		result = structure + ''
		if '{v' in structure:
			phrases = self.get_verb_phrases(text)
			if len(phrases) != 0:
				for suf in ['た', 'て', 'たり', 'み', '過ぎ', 'すぎ', 'たい']:
					token = '{v}' + suf
					while token in result:
						result = result.replace(token, self.inflect(random.choice(phrases), suf), 1)
				while '{v}' in result:
					result = result.replace('{v}', random.choice(phrases), 1)
		if '{n' in structure:
			phrases = self.get_noun_phrases(text)
			if len(phrases) != 0:
				while '{n}' in result:
					result = result.replace('{n}', random.choice(phrases))
		return result


	def get_material(self):
		result = ''
		for i in range(5):
			num = random.randrange(CORPUS_NUMBER_OF_LINES)
			result += subprocess.check_output(['sed', '-n', '{}p'.format(num), CORPUS_FILE_NAME]).decode('UTF-8')
		return result.strip()

	def get_strcuture(self):
		f = open(STRUCTURE_FILE_NAME, 'r', encoding = 'UTF-8')
		lines = f.readlines()
		return random.choice(lines)

	def get_emoji(self):
		emojies = [
			'💪',
			'😇',
			'😅',
			'👊',
			'✋',
		]
		descriptions = [
			'(語彙力)',
			'(オタク特有の早口)',
			'(ｸﾁｬｸﾁｬ)',
			'(アディダスの財布)',
			'(親が買ってきたチェックシャツ)',
			'(ダボダボのジーパン)',
			'(修学旅行で木刀購入)',
			'(午後の紅茶)',
			'(プーマの筆箱)',
			'(指紋でベタベタのメガネ)',
			'(プリパラでマジ泣き)',
			'(ドラゴンの裁縫セット)',
			'(瞬足)',
			'(コーナーで差をつけろ)'
		]
		result = ''
		r = random.random()
		if r < 0.5:
			for i in range(10):
				if random.random() < 0.5:
					result += random.choice(emojies)
		elif r < 0.7:
			for i in range(10):
				if random.random() < 0.5:
					result += random.choice(descriptions)
		return result


	def generate(self):
		return self.fit_to_structure(self.get_material(), self.get_strcuture()).strip() + self.get_emoji()
