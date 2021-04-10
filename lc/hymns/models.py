from django.db import models
import sqlite3
from tqdm import tqdm
import re


class TextBlock(models.Model):
    """Фрагмент последования /
        последование /
        богослужебная книга /
        полка книг"""
    parent_block    = models.ForeignKey('self', default=None, null=True, on_delete=models.CASCADE)
    name_long       = models.CharField(max_length=256, null=True, default=None)
    name_short      = models.CharField(max_length=32, null=True, default=None)
    path_long       = models.TextField(null=True, default=None)
    path_short      = models.TextField(null=True, default=None)
    order_id        = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.name_long

    def clean(self):
        """ Удалить все подблоки """
        for book in TextBlock.objects.filter(parent_block = self):
            book.delete()
        # conn = sqlite3.connect("db.sqlite3") 
        # cursor = conn.cursor()
        # rows = cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM hymns_textblock) WHERE name='hymns_textblock'")
        # conn.close()

    def update_path(self):
        if self.parent_block is not None:
            self.path_short = self.parent_block.path_short + "/" + self.name_short
        else:
            self.path_short = self.name_short


class Paragraph(models.Model):
    """Абзац богослужебной книги"""
    txt             = models.TextField(null=True, default=None)
    txt_simplified  = models.TextField(null=True, default=None)
    parent_block    = models.ForeignKey(TextBlock, default=None, null=True, on_delete=models.CASCADE)
    order_id        = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.txt

    def clean_html(self):
        self.txt = re.sub(r"<[^>]*>", "", self.txt)

    def simplify(self):
        PUNCT = ",.:?!;\(\)–—\[\]\-"
        self.txt_simplified = re.sub(r"["+PUNCT+"]", " ", self.txt.lower())
        self.txt_simplified = re.sub(r"[ ]{2,}", " ", self.txt_simplified)
        

def source_base_path():
    return "../source_data/"


def import_Bible_1751_grazhd():
    bible, created = TextBlock.objects.get_or_create(
                name_short = "Библия1751", 
                name_long = "Библия 1751 года в гражданской графике")
    bible.update_path()
    bible.clean()
    conn = sqlite3.connect(source_base_path() + "grazhd/Bible_1751_grazhd.SQLite3") 
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    rows = cursor.execute("SELECT book_number, short_name, long_name FROM books ORDER BY book_number")
    books = {}
    for row in rows:
        print (row['long_name'])
        book = TextBlock.objects.create(parent_block = bible, 
                        name_long = row['long_name'], 
                        name_short = row['short_name'],
                        order_id = row['book_number'])
        book.update_path()
        book.save()
        books[row['book_number']] = book
    rows = cursor.execute("SELECT book_number, chapter, verse, text FROM verses ORDER BY book_number, chapter, verse")
    prev_book_number = -1
    prev_chapter = -1
    for row in tqdm(rows):
        if (row['book_number']!=prev_book_number):
            current_book = books[row['book_number']]
            prev_book_number = row['book_number']
            prev_chapter = -1
        if (row['chapter']!=prev_chapter):
            current_chapter = TextBlock.objects.create(parent_block = current_book,
                                                    name_long = "Глава %d" % row['chapter'],
                                                    name_short = str(row['chapter']),
                                                    order_id = row['chapter'])
            current_chapter.update_path()
            current_chapter.save()
            prev_chapter = row['chapter']
        par = Paragraph.objects.create(parent_block = current_chapter, 
                        txt = row['text'], 
                        order_id = row['verse'])
        par.clean_html()
        par.simplify()
        par.save()
    conn.close()