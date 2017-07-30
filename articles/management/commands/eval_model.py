from django.core.management.base import BaseCommand

from cross_validation import cv_accuracy
from utils import get_train_data


class Command(BaseCommand):
    help = 'Evaluate naivebayes model'

    def add_arguments(self, parser):
        """
        k-交差検証のkの値をオプションの引数でつける関数

        :param parser: argparse.ArgumentParser, パーサー
        """
        parser.add_argument('number_split', nargs=1, type=int)

    def handle(self, *args, **options):
        """
        コマンドが実行された際に呼ばれるメソッド

        :param args: tuple, 余った引数を受け取るタプル
        :param options: dict, 余ったキーワード引数を受け取り
        """
        k = options['number_split'][0]
        tags, data = get_train_data()
        print(cv_accuracy(tags, data, k))
        self.stdout.write(self.style.SUCCESS('Successfully trained model'))
