from django.contrib import admin

from .models import Lemma, Token

admin.site.register(Lemma)
admin.site.register(Token)
