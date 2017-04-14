# munyudroid
Twitterでいろいろ遊ぶためのbotです。

# ファイルの説明
- bot1.2.py
  メインプログラム
- th.py
  天和ガチャに関する処理
- th.c
  天和ガチャの実装部
  
# 補足
- メルセンヌ・ツイスタのライブラリMT.hはこちらを使用させていただいています。
  http://www.sat.t.u-tokyo.ac.jp/~omi/code/MT.h
- TwitterのStreaming APIの接続が数時間〜1日前後に1回ほど突然切れることがあります。対策として、こちらを使用させていただいています。
  http://qiita.com/tattsun58/items/67b0f16c86fbe49fe5d0
- tweepyなど必要なモジュールは適宜インストールしてください。

# 環境

Python 2.7.10

# 参考文献
http://qiita.com/yuhkan/items/299b41736a221e63b43c
http://qiita.com/FGtatsuro/items/cf178bc44ce7b068d233
http://www.sat.t.u-tokyo.ac.jp/~omi/random_variables_generation.html

# トラブルシューティング記録
- 再接続後落ちる現象が発生
  原因 シェルスクリプトからPythonを実行しているため、直接Pythonを実行したときとカレントディレクトリが異なっていた。
  解決策 シェルスクリプトに
  cd $(dirname $0)
  を加える
  原因 文字コードの設定がなぜか消えていた
  解決策 export PYTHONIOENCODING=utf-8 する



