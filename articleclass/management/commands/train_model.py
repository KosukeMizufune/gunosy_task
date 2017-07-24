from django.core.management.base import BaseCommand, CommandError
from sklearn.externals import joblib

from train_mecab import train_mecab
from naivebayes import NaiveBayes


class Command(BaseCommand):
    help = 'Train naivebayes model'

    def add_arguments(self, parser):
        parser.add_argument('train_model')

    def handle(self, *args, **options):
        nb = NaiveBayes()
        tags, data = train_mecab()
        nb.train(tags, data)
        joblib.dump(nb, 'naivebayes.cmp', compress=True)
        self.stdout.write(self.style.SUCCESS('Successfully trained model'))
