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
        possible_tokens = lemma.generate_forms()
        possible_tokens.update({k : possible_tokens[k].rstrip('^') for k in possible_tokens.keys()})
        unused_tokens_set = set(possible_tokens.values()) - set(t.txt for t in tokens)
        unused_tokens_dict = {}
        for gram, txt in possible_tokens.items():
            if re.match(r"^[^=].*", txt):
                gram = re.sub(r"\.[0-9]", "", gram)
                gram = re.sub("\+", ",", gram)
                if txt in unused_tokens_set:
                    if txt in unused_tokens_dict:
                        new_gram = unused_tokens_dict[txt] + " | " + gram
                        unused_tokens_dict.update({txt : new_gram})
                    else:
                        unused_tokens_dict.update({txt : gram})
    except:
        possible_tokens = None
        unused_tokens_dict = None
    prev_lemmas = Lemma.objects.filter(~Q(txt__contains="#")
                                    & ~Q(txt__contains="+")
                                    & Q(txt__lt = lemma.txt)).order_by('-txt')
    try:
        prev_lemma = prev_lemmas[0]
    except:
        prev_lemma = None
    next_lemmas = Lemma.objects.filter(~Q(txt__contains="#")
                                    & ~Q(txt__contains="+")
                                    & Q(txt__gt = lemma.txt)).order_by('txt')
    try:
        next_lemma = next_lemmas[0]
    except:
        next_lemma = None

    return render(request, 'rc_dic/lemma.html',
                {'lemma': lemma,
                'tokens' : tokens,
                'unused_tokens' : unused_tokens_dict,
                'prev_lemma' : prev_lemma,
                'next_lemma' : next_lemma,
                })
