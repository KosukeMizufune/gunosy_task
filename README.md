# 記事URLを入力すると記事カテゴリーを返すWebアプリケーションの実装

## 訓練データ
今回の訓練データはgunosyの各カテゴリのトップページから100ページ目までの記事を抽出  
クロール過程で存在しないページは飛ばすようにしているのでおよそ15000件ほどの記事が手に入ると思われる  

##実行環境  
python3.5.0  
django1.10  
certifi==2017.4.17  
chardet==3.0.3  
cssselect==1.0.1  
Django==1.10  
django-bootstrap-form==3.2.1  
idna==2.5  
lxml==3.7.3  
mecab-python3==0.7  
pymongo==3.4.0  
requests==2.17.3  
urllib3==1.21.1  

## 実行方法  
1 課題のgunosy_taskレポジトリをクローン  
`$git clone https://github.com/KosukeMizufune/gunosy_task.git`

2 クローンしたgunosy_taskフォルダに移動  
`$cd gunosy task`

3 記事データを取得する  
`$python gettrain.py`  
ただし、このままだとデータを取得するのに8時間ほどかかるので、検証用にアプリを起動するだけならばgettrain.pyの55行目の  
`while count < 100`  
を  
`while count < 任意の数`  
などにすることで実行時間を短縮することで十分であると思われる  

4 サーバーを起動する  
`$python manage.py runserver`  
と入力することでサーバーが起動する。記事データを訓練させるので立ち上がるまでにすこじ時間がかかる  

5 4を実行後、以下のURLにアクセスする  
http://127.0.0.1:8000/articleclass/url/  

6 フォームにURLを入力する

7 記事のカテゴリがURLフォームの下に表示される

## 精度評価  
14985件のデータを5-folds-crossvalidationによるaccuracyで評価をした結果、89%ほどの精度となった。  
gunosy_taskレポジトリから精度評価をする方法は、  
`$python cross_validation.py`  
と入力することでaccuracyが表示される