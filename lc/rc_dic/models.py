from django.db import models
import sqlite3
import pandas
import re
from tqdm import tqdm


class Language(models.Model):
    """Языки, диалекты и их кодировки"""
    name  = models.CharField(max_length=12, unique=True)
    name_long   = models.CharField(max_length=45, null=True, default=None)
    encoding    = models.CharField(max_length=12, null=True, default=None)

    def __str__(self):
        return self.name_long + " (" + self.encoding + ")"



class Source(models.Model):
    """Источники данных и способы обработки при их обновлении"""
    name    = models.CharField(max_length=12)
    name_long   = models.CharField(max_length=45, null=True, default=None)
    date_added  = models.DateField(auto_now_add=True)
    load_script = models.CharField(max_length=128)
    def __str__(self):
        return self.name



class Paradigm(models.Model):
    """Парадигмы словоизменения (сама парадигма записывается отдельно в коде)"""
    language    = models.ForeignKey(Language, on_delete=models.CASCADE)
    # пока что язык только один — цсл синодального периода
    name    = models.CharField(max_length=32)
    class Meta:
            indexes = [
                models.Index(fields=['name']),
            ]
    def __str__(self):
        return self.name



class Lemma(models.Model):
    """Лемма может быть не уникальной:
    или в разных диалектах она может писаться одинаково,
    или изменяться по разным парадигмам
    """
    language    = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, default=None)
    txt         = models.CharField(max_length=127, null=True, default=None)
    grammar_attributes  = models.CharField(max_length=64, null=True, default=None)
    # ?? Потом надо будет сделать отдельный класс с раскидать GrammarAttributes и раскидать
    source      = models.ForeignKey(Source, on_delete=models.CASCADE, null=True, default=None)
    paradigm    = models.ForeignKey(Paradigm, on_delete=models.CASCADE, null=True, default=None)

    class Meta:
            indexes = [
                models.Index(fields=['txt']),
            ]

    def __str__(self):
        return self.txt



class Token(models.Model):
    language    = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, default=None)
    txt         = models.CharField(max_length=127, null=True, default=None)
    lemma       = models.ForeignKey(Lemma, on_delete=models.CASCADE, null=True, default=None)
    grammar_attributes  = models.CharField(max_length=64, null=True, default=None)
    paradigm    = models.ForeignKey(Paradigm, null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return self.token_utf



def new_connection():
    conn = sqlite3.connect("../source_data/source.sqlite")
    conn.row_factory=sqlite3.Row
    return conn

def polyakov_import_tsv():
    conn = new_connection()
    sql = """CREATE TABLE "polyakov_dic" (
    "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "sort"	varchar(45) DEFAULT NULL,
    "word"	varchar(45) DEFAULT NULL,
    "lex"	varchar(45) DEFAULT NULL,
    "pos"	varchar(45) DEFAULT NULL,
    "flex_type"	varchar(45) DEFAULT NULL,
    "gram"	varchar(100) DEFAULT NULL,
    "pp"	varchar(45) DEFAULT NULL,
    "freq"	int(11) DEFAULT NULL,
    "dup"	int(11) DEFAULT NULL
    );"""
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS polyakov_dic")
    cursor.execute(sql)
    df = pandas.read_csv('../source_data/polyakov_dic.tsv', \
                        header = 0, \
                        quoting = 3, #QUOTE_NONE \
                        sep = '\t')

    df.to_sql('polyakov_dic', conn, index = False, if_exists = 'replace')
    conn.close()


def polyakov_import_all_paradigms():
    Paradigm.objects.all().delete()
    lang = Language.objects.get(encoding='polyakov')
    conn = new_connection()
    cursor = conn.cursor()
    sql = "SELECT distinct flex_type FROM polyakov_dic where flex_type IS NOT NULL and flex_type <> ''"
    cursor.execute(sql)
    p = cursor.fetchone()
    paradigm_names = set()
    while p:
        candidates = set(re.split("[/]+", p['flex_type']))
        paradigm_names |= candidates
        p = cursor.fetchone()
    paradigm_names = paradigm_names - {''}
    paradigms = list(map(lambda p: Paradigm(language = lang, name = p),
                paradigm_names))
    Paradigm.objects.bulk_create(paradigms)
    conn.close()



def polyakov_import_all_lemmas():
    Lemma.objects.all().delete()
    lang = Language.objects.get(encoding='polyakov')
    src = Source.objects.get(name='polyakov')
    connection = new_connection()
    cursor = connection.cursor()
    sql = "SELECT distinct lex, pos, flex_type FROM polyakov_dic"
    cursor.execute(sql)
    row = cursor.fetchone()
    lemmas = []
    while row:
        if row['flex_type']:
            flex_types = set(re.split("[/]+", row['flex_type']))
            for f in flex_types:
                try:
                    prd = Paradigm.objects.get(name=f)
                except:
                    prd = None
                    print("Не смог найти парадигму «%s», fles_type=«%s»" % (f, row['flex_type']))
                lemmas += [Lemma(txt = row['lex'],
                            language = lang,
                            grammar_attributes = row['pos'],
                            paradigm = prd,
                            source = src)]
        else:
            lemmas += [Lemma(txt = row['lex'],
                        language = lang,
                        grammar_attributes = row['pos'],
                        paradigm = None,
                        source = src)]
        row = cursor.fetchone()
    Lemma.objects.bulk_create(lemmas)
    connection.close()




def import_all_tokens():
    Token.objects.all().delete()
    # connection = new_connection()
    # cursor = connection.cursor()
    # sql = "SELECT * FROM liturcorpora.polyakov_dic order by lex"
    # cursor.execute(sql)
    # tokens = []
    # lemma_txt_prev = None
    # for i in tqdm(range(cursor.rowcount)):
    #     p = cursor.fetchone()
    #     # print(p['lex'], p['word'])
    #     if (p['lex'] != lemma_txt_prev):
    #         lemma_txt_prev = p['lex']
    #         lemma_obj = Lemma.objects.get(lemma_rc=p['lex'])
    #     tokens += [Token(sort_key   = p['sort'],
    #                     token_rc    = p['word'],
    #                     lemma       = lemma_obj,
    #                     part_of_speech = p['pos'],
    #                     flex_type   = p['flex_type'],
    #                     gram        = p['gram'])]
    # Token.objects.bulk_create(tokens)
    # connection.close()


def rebuild_all_polyakov():
    Language.objects.filter(encoding='polyakov').delete()
    Language(name       = 'csl_new',
             name_long  = 'церковнославянский синодального периода',
             encoding   = 'polyakov').save()
    polyakov_import_tsv()
    polyakov_import_all_paradigms()
    polyakov_import_all_lemmas()


def rebuild_all_data():
    rebuild_all_polyakov()
