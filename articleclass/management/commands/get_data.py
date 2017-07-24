import argparse

from django.core.management.base import BaseCommand

from gettrain import get_data


class Command(BaseCommand):
    help = 'Train naivebayes model'
    parser = argparse.ArgumentParser(description='Process some integers.')

    def add_arguments(self, parser):
        """
        スクレイプする予定の、各タグの記事一覧ページの数をオプション引数として加える関数

        :param parser: argparse.ArgumentParser, パーサー
        """
        parser.add_argument('page_count', nargs=1, type=int)

    def handle(self, *args, **options):
        """
        コマンドが実行された際に呼ばれるメソッド

        :param args: tuple, 余った引数を受け取るタプル
        :param options: dict, 余ったキーワード引数を受け取り
        """
        page_count = options['page_count']
        get_data(page_count)
        self.stdout.write(self.style.SUCCESS('Successfully get model'))
