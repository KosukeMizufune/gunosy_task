from django.core.management.base import BaseCommand
from sklearn.externals import joblib

from naivebayes import NaiveBayes
from utils import get_train_data


class Command(BaseCommand):
    help = 'Train naivebayes model'

    def handle(self, *args, **options):
        """
        コマンドが実行された際に呼ばれるメソッド

        :param args: tuple, 余った引数を受け取るタプル
        :param options: dict, 余ったキーワード引数を受け取り
        """
        nb = NaiveBayes()
        tags, data = get_train_data()
        nb.train(tags, data)
        joblib.dump(nb, 'naivebayes.cmp', compress=True)
        self.stdout.write(self.style.SUCCESS('Successfully trained model'))
