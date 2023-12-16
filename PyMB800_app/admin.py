from django.contrib import admin
from .models import BaseQuestion, MultipleChoice, DropDown, DragDropOrder, DragDropPairs

admin.site.register(BaseQuestion)
admin.site.register(MultipleChoice)
admin.site.register(DropDown)
admin.site.register(DragDropOrder)
admin.site.register(DragDropPairs)
