# 記事URLを入力すると記事カテゴリーを返すWebアプリケーションの実装
[![Build Status](https://travis-ci.org/KosukeMizufune/gunosy_task.svg?branch=pep8-modify)](https://travis-ci.org/KosukeMizufune/gunosy_task)

## 訓練データ
今回の訓練データはgunosyの各カテゴリのトップページから100ページ目までの記事を抽出  
クロール過程で存在しないページは飛ばすようにしているのでおよそ15000件ほどの記事が手に入ると思われる  

## 実行方法  
1 課題のgunosy_taskレポジトリをクローン  
`$git clone https://github.com/KosukeMizufune/gunosy_task.git`

2 クローンしたgunosy_taskフォルダに移動  
`$cd gunosy task`

3 記事データを取得する 
 コマンドプロンプトで
`$python manage.py get_data [任意の数字]`    
と入力することで記事データを取得することができます 

4モデルを学習させる
コマンドプロンプトで
`$python manage.py train_model`
と入力することでナイーブベイズによる記事学習モデルを保存できます。

5 サーバーを起動する  
`$python manage.py runserver`  
と入力することでサーバーが起動する。記事データを訓練させるので立ち上がるまでにすこし時間がかかります  

6 4を実行後、以下のURLにアクセスする  
http://127.0.0.1:8000/articleclass/url/  

7 フォームにGunosyの記事URLを入力する

8 記事のカテゴリがURLフォームの下に表示される

## 精度評価  
14985件のデータを5-folds-crossvalidationによるaccuracyで評価をした結果、89%ほどの精度となった。  
gunosy_taskレポジトリから精度評価をする方法はコマンドプロンプトで
`$python manage,py eval_model [任意の数字]`  
と入力することでaccuracyが表示される
