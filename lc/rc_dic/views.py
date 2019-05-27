from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Lemma, Token

import importlib.util
spec = importlib.util.spec_from_file_location("generate_word_forms", 'rc_dic/generate_word_forms.py')
generate_word_forms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_word_forms)
# from gen import generate_forms


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
    try:
        possible_tokens = generate_word_forms.generate_forms(lemma.txt, lemma.paradigm.name)
    except:
        possible_tokens = None
    possible_tokens.update({k : possible_tokens[k].rstrip('^') for k in possible_tokens.keys()})
    tokens = Token.objects.filter(lemma = lemma)
    for t in tokens:
        if t.grammar_attributes in possible_tokens:
            if t.txt == possible_tokens[t.grammar_attributes]:
                possible_tokens.pop(t.grammar_attributes, None)
    return render(request, 'rc_dic/lemma.html',
                {'lemma': lemma,
                'tokens' : tokens,
                'possible_tokens' : possible_tokens})
