from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
import re
from .models import Lemma, Token



def index(request):
    return render(request, 'rc_dic/main_index.html', {})

def robots(request):
    return render(request, 'rc_dic/robots.txt', content_type="text/plain")

# from gererate_word_forms import generate_forms


def list_lemmas(request):
    all_lemmas = Lemma.objects.filter(~Q(txt__contains="#") & ~Q(txt__contains="+") ).order_by('txt')
    paginator = Paginator(all_lemmas, 12) # Show 12 lemmas per page
    page = request.GET.get('page')
    lemmas = paginator.get_page(page)
    return render(request, 'rc_dic/lemmas.html', {'lemmas': lemmas})


def lemma_info(request, lemma_id):
    lemma = Lemma.objects.get(pk=lemma_id)
    tokens = Token.objects.filter(lemma = lemma).order_by('txt')
    try:
        possible_tokens_list_of_dicts = lemma.generate_forms()
        print("Сгенерировали список словарей длиной %d" % len(possible_tokens_list_of_dicts))
        unused_tokens_dict = {}
        for possible_tokens in possible_tokens_list_of_dicts:
            print("Возможные словоформы: %s " % set(possible_tokens.values()))
            possible_tokens.update({k : possible_tokens[k].rstrip('^') for k in possible_tokens.keys()})
            print("После обновления: %s" % set(possible_tokens.values()))
            unused_tokens_set = set(possible_tokens.values()) - set(t.txt for t in tokens)
            print("Неупотребленные: %s" % unused_tokens_set)
            for gram, txt in possible_tokens.items():
                if (re.match(r"^[^=].*", txt) is not None) & (txt in unused_tokens_set):
                    gram = re.sub(r"\.[0-9]", "", gram)
                    gram = re.sub("\+", ",", gram)
                    print ("Добавлеям к слову %s форму %s" % (txt, gram))
                    if txt in unused_tokens_dict:
                        new_gram = unused_tokens_dict[txt] | {gram}
                        print ("new_gram: %s" % new_gram)
                        unused_tokens_dict.update({txt : new_gram})
                    else:
                        unused_tokens_dict.update({txt : {gram}})
        print(unused_tokens_dict)
        for k in unused_tokens_dict.keys():
            new_gram = " | ".join(unused_tokens_dict[k])
            unused_tokens_dict.update({k : new_gram})
    except:
        possible_tokens = None
        unused_tokens_dict = None
    prev_lemmas = Lemma.objects.filter(~Q(txt__contains="#")
                                    & ~Q(txt__contains="+")
                                    & Q(txt__lte = lemma.txt)).order_by('-txt', '-id')
    try:
        i = 1
        while (prev_lemmas[i].txt == lemma.txt) & (prev_lemmas[i].id >= lemma.id):
            i+=1
        prev_lemma = prev_lemmas[i]
    except:
        prev_lemma = None
    next_lemmas = Lemma.objects.filter(~Q(txt__contains="#")
                                    & ~Q(txt__contains="+")
                                    & Q(txt__gte = lemma.txt)).order_by('txt', 'id')
    try:
        i = 1
        while (next_lemmas[i].txt == lemma.txt) & (next_lemmas[i].id <= lemma.id):
            i+=1
        next_lemma = next_lemmas[i]
    except:
        next_lemma = None

    return render(request, 'rc_dic/lemma.html',
                {'lemma': lemma,
                'tokens' : tokens,
                'paradigms' : ", ".join(lemma.paradigms()),
                'unused_tokens' : unused_tokens_dict,
                'prev_lemma' : prev_lemma,
                'next_lemma' : next_lemma,
                })
