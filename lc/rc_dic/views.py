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
    all_lemmas = Lemma.objects.filter(~Q(lemma_rc__contains="#") & ~Q(lemma_rc__contains="+") ).order_by('lemma_rc')
    paginator = Paginator(all_lemmas, 12) # Show 12 lemmas per page
    page = request.GET.get('page')
    lemmas = paginator.get_page(page)
    return render(request, 'rc_dic/lemmas.html', {'lemmas': lemmas})
