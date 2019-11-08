from django.db import models
import sqlite3
import pandas
import re
from tqdm import tqdm
import os
from bs4 import BeautifulSoup

from rc_dic.models import Language

class Book(models.Model):
    """Богослужебные книги"""
    name        = models.CharField(max_length=40, unique=True, default=None)
    name_long   = models.CharField(max_length=128, null=True, default=None)
    language    = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.name_long + " (" + self.language + ")"


def ponomar_import_all_books():
    print ("Составляем список книг в репозитории…")
    Book.objects.all().delete()
    lang = Language.objects.get(name='csl_utf')
    path = "../source_data/ponomar/"
    books = []
    for dirname in os.listdir(path):
        if (not dirname.startswith('.')) and os.path.isdir(path + dirname):
            # print (path + dirname)
            manifest = path + dirname + '/manifest.xml'
            if os.path.exists(manifest):
                with open(manifest, 'r') as f:
                    soup = BeautifulSoup(f, "html.parser")
                    title = soup.find('meta', attrs = {'name' : 'title'})
                    if title:
                        books += [Book(name = dirname, name_long = title['content'], language = lang)]
    print ("Добавляем %d книг." % len(books), end = ' ')
    Book.objects.bulk_create(books)
    print ("Готово.")