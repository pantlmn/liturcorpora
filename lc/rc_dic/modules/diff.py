import sqlite3
import tqdm
from generate import *
import re

conn = sqlite3.connect("../../db.sqlite3")
conn.row_factory=sqlite3.Row
cursor = conn.cursor()

cursor.execute("""SELECT name from rc_dic_paradigm order by name
               """)

# db_paradigms = sorted(p['name'] for p in cursor)

# print (db_paradigms)
# code_paradigms = set(paradigms.keys())
#
# correspondence = {}
#
# for pd in db_paradigms:
#     subset = []
#     # print (pd)
#     for pc in code_paradigms:
#         if (re.match("^" + re.escape(pd) + "$", pc) is not None) or (re.match("^" + re.escape(pd) + "-[a-z]$", pc) is not None):
#             subset += [pc]
#     correspondence.update({pd : sorted(subset)})
#
# for k, v in correspondence.items():
#     print ('%s: %s' % (k, ", ".join(v)))

# print ("Есть в базе, но нет в коде:", sorted(db_paradigms - code_paradigms))
# #
# print ("Есть в коде, но нет в базе:", sorted(code_paradigms - db_paradigms))

#
# у́тренній
# generate_forms_and_print("у́тренній","A1j*-a")
# generate_forms_and_print("да́льній","A1j*-a")
# generate_forms_and_print("господній","A1j*-a")
# generate_forms_and_print("господній","#A1j*")
# print(find_matching_paradigms('а́ггельскій', 'A1k'))
# print (generate_word_forms("а́гнецъ","N1c*"))
# print (generate_word_forms("а́збучный","A1t*"))
# print (generate_word_forms("а́гнчій","A2i"))

cursor.execute("SELECT l.txt, p.name from rc_dic_lemma as l, rc_dic_paradigm as p where l.paradigm_id = p.id order by txt")

no_paradigm = []
one_paradigm = []
multiple_paradigms = []
for row in cursor:
    paradigms = find_matching_paradigms(row['txt'], row['name'])
    l = len(paradigms)
    if l==0:
        no_paradigm += [row['txt']]
    elif l == 1:
        one_paradigm += [row['txt']]
        print (row['txt'])
    else:
        multiple_paradigms += [row['txt']]
lnp = len(no_paradigm)
lop = len(one_paradigm)
lmp = len(multiple_paradigms)
total =  lnp + lop + lmp

print("Без подходящей парадигмы: %d (%.2f)" % (lnp, lnp*100/total))
print("С одной подходящей парадигмой: %d (%.2f)" % (lop, lop*100/total))
print("С несколькими подходящими парадигмами: %d (%.2f)" % (lmp, lmp*100/total))



conn.close()
