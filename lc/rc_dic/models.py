from django.db import models
import pymysql.cursors
from tqdm import tqdm


class Lemma(models.Model):
    lemma_rc    = models.CharField(max_length=45)
    lemma_utf   = models.CharField(max_length=45)

    def __str__(self):
        return self.lemma_utf

    def rc2utf(self):
        self.lemma_utf = self.lemma_rc + '+'
        self.save()


class Token(models.Model):
    sort_key    = models.CharField(max_length=45)
    token_rc    = models.CharField(max_length=45)
    token_utf   = models.CharField(max_length=45, null=True, default=None)
    lemma       = models.ForeignKey(Lemma, on_delete=models.CASCADE)
    part_of_speech = models.CharField(max_length=45, null=True, default=None)
    flex_type   = models.CharField(max_length=45, null=True, default=None)
    gram        = models.CharField(max_length=45, null=True, default=None)

    def __str__(self):
        return self.token_utf
