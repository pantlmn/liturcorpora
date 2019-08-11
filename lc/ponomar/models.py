from django.db import models
import sqlite3
import pandas
import re
from tqdm import tqdm

from rc_dic.models import Language

class Book(models.Model):
    """Богослужебные книги"""
    name  = models.CharField(max_length=12, unique=True)
    name_long   = models.CharField(max_length=45, null=True, default=None)
    language       = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.name_long + " (" + self.language + ")"
