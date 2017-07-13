# 記事URLを入力すると記事カテゴリーを返すWebアプリケーションの実装
[![Build Status](https://travis-ci.org/c-bata/TDD-with-Django.svg)](https://travis-ci.org/c-bata/TDD-with-Django)

## 訓練データ
今回の訓練データはgunosyの各カテゴリのトップページから100ページ目までの記事を抽出  
クロール過程で存在しないページは飛ばすようにしているのでおよそ15000件ほどの記事が手に入ると思われる  

## 実行方法  
1 課題のgunosy_taskレポジトリをクローン  
`$git clone https://github.com/KosukeMizufune/gunosy_task.git`

2 クローンしたgunosy_taskフォルダに移動  
`$cd gunosy task`

3 記事データを取得する  
`$python gettrain.py`  
ただし、このままだとデータを取得するのに8時間ほどかかるので、検証用にアプリを起動するだけならばgettrain.pyの61行目の  
`while count < 100`  
を  
`while count < 任意の数`  
などに設定し実行時間を短縮することでアプリケーションが実行できるかの確認ができると思われます。  

4 サーバーを起動する  
`$python manage.py runserver`  
と入力することでサーバーが起動する。記事データを訓練させるので立ち上がるまでにすこし時間がかかります  

5 4を実行後、以下のURLにアクセスする  
http://127.0.0.1:8000/articleclass/url/  

6 フォームにGunosyの記事URLを入力する

7 記事のカテゴリがURLフォームの下に表示される

## 精度評価  
14985件のデータを5-folds-crossvalidationによるaccuracyで評価をした結果、89%ほどの精度となった。  
gunosy_taskレポジトリから精度評価をする方法は、  
`$python cross_validation.py`  
と入力することでaccuracyが表示される
