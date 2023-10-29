from django import forms
from .models import Notes, Storage, Calendar, Todo, Deadlines
from tinymce.widgets import TinyMCE


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('content', 'title', 'explanation',)
        widgets = {'content': TinyMCE()}


class StorageFolderForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ('folder',)


class StorageFileForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ('file', 'folder',)


class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ('event', 'start_date', 'end_date',)


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('task',)


class DeadlinesForm(forms.ModelForm):
    class Meta:
        model = Deadlines
        fields = ('task', 'ended_on')
