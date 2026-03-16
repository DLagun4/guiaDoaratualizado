from django.contrib import admin
from guiadoars.models import Topic, Entry

admin.site.register(Topic)
admin.site.register(Entry)

from django.contrib import admin
from .models import Instituicao

admin.site.register(Instituicao)