from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
import re
from .models import TextBlock, Paragraph



def index(request, block_id=None):
    path = []
    paragraphs = None
    if block_id is None:
        blocks = TextBlock.objects.filter(parent_block=None)
    else:
        blocks = TextBlock.objects.filter(parent_block__id=block_id).order_by('order_id')
        block = TextBlock.objects.get(id=block_id)
        while block is not None:
            path = [[block.id, block.name_short]] + path
            block = block.parent_block
        paragraphs = Paragraph.objects.filter(parent_block__id=block_id).order_by('order_id')
    return render(request, 'textblocks.html', {'path' : path, 'blocks' : blocks, 'paragraphs' : paragraphs})


def paragraph(request, paragraph_id=None):
    paragraph = Paragraph.objects.get(id=paragraph_id)
    block = paragraph.parent_block
    path = []
    while block is not None:
        path = [[block.id, block.name_short]] + path
        block = block.parent_block
    return render(request, 'paragraph.html', {'path' : path, 'paragraph' : paragraph})
