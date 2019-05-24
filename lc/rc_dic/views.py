from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Lemma, Token

def index(request):
    return render(request, 'rc_dic/main_index.html', {})


def list_lemmas(request):
    all_lemmas = Lemma.objects.filter(~Q(txt__contains="#") & ~Q(txt__contains="+") ).order_by('txt')
    paginator = Paginator(all_lemmas, 12) # Show 12 lemmas per page
    page = request.GET.get('page')
    lemmas = paginator.get_page(page)
    return render(request, 'rc_dic/lemmas.html', {'lemmas': lemmas})


def lemma_info(request, lemma_id):
    lemma = Lemma.objects.get(pk=lemma_id)
    tokens = Token.objects.filter(lemma = lemma)
    return render(request, 'rc_dic/lemma.html', {'lemma': lemma, 'tokens' : tokens})
