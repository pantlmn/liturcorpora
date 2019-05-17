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

def new_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='msonGpn',
                           db='liturcorpora',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)

def import_all_lemmas():
    Lemma.objects.all().delete()
    connection = new_connection()
    cursor = connection.cursor()
    sql = "SELECT distinct lex FROM liturcorpora.polyakov_dic"
    cursor.execute(sql)
    p = cursor.fetchone()
    lemmas = []
    while p:
        lemmas += [Lemma(lemma_rc = p['lex'])]
        p = cursor.fetchone()
    Lemma.objects.bulk_create(lemmas)
    connection.close()


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


def import_all_tokens():
    Token.objects.all().delete()
    connection = new_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM liturcorpora.polyakov_dic order by lex"
    cursor.execute(sql)
    tokens = []
    lemma_txt_prev = None
    for i in tqdm(range(cursor.rowcount)):
        p = cursor.fetchone()
        # print(p['lex'], p['word'])
        if (p['lex'] != lemma_txt_prev):
            lemma_txt_prev = p['lex']
            lemma_obj = Lemma.objects.get(lemma_rc=p['lex'])
        tokens += [Token(sort_key   = p['sort'],
                        token_rc    = p['word'],
                        lemma       = lemma_obj,
                        part_of_speech = p['pos'],
                        flex_type   = p['flex_type'],
                        gram        = p['gram'])]
    Token.objects.bulk_create(tokens)
    connection.close()
