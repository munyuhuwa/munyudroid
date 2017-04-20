# munyudroid
Twitterでいろいろ遊ぶためのbotです。

# 前バージョンからの変更点
Python 3に対応しました(Python 2には対応しなくなりました)。
和了形の画像を投稿できるようになりました。

# ファイルの説明
- bot3.5.py
  メインプログラム
- th4.py
  天和ガチャに関する処理
- th.c
  天和ガチャの実装部
  
# 環境
  Python 3.6.1
  
# 準備・使用方法
- 必要があればPythonの環境を整備してください。
- importしているライブラリで、ないものがあれば入れてください。なお、PILはpillowの名前で配布されているようです。
- ガチャの実装部をコンパイルしてください。
  MT.hが必要なので同じディレクトリに置いてください。自動でインクルードされるはずです。
  gcc ./th.c -o ./th.exe
- 牌の画像ファイル(PNG形式)を用意して./tiles/に入れてください。
  ファイル名は"m5.png"(伍萬), "j6.png"(中)のようにしてください。
  サイズは横40px\*縦52pxにしてください。
- 画像出力用ディレクトリ./out/を作ってください
  
  
# 補足
- メルセンヌ・ツイスタのライブラリMT.hはこちらを使用させていただいています。
  http://www.sat.t.u-tokyo.ac.jp/~omi/code/MT.h
- TwitterのStreaming APIの接続が数時間〜1日前後に1回ほど突然切れることがあります。対策は考え中。

# 参考文献
http://qiita.com/yuhkan/items/299b41736a221e63b43c
http://qiita.com/FGtatsuro/items/cf178bc44ce7b068d233
http://www.sat.t.u-tokyo.ac.jp/~omi/random_variables_generation.html
http://qiita.com/yubais/items/864eedc8dccd7adaea5d
