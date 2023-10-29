from django.urls import path, include
from .views import workspace_view, logout_view, ListNotes, EditNotes, DeleteNotes, create_view, upload_image, \
    calendar_view, deadlines_view, music_view, trash_view, summarization_view, dashboard_view, \
    storage_view, move_to_trash, notes, EditTodo
from django.conf.urls.static import static
from eduweb.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('', workspace_view, name='workspace'),
    path('logout/', logout_view, name='logout'),
    path('notes/<int:pk>', notes, name='notes'),
    path('notes/', ListNotes, name='notes'),
    path('todo/<int:pk>/edit', EditTodo.as_view(), name='edit_todo'),
    path('notes/<int:pk>/edit', EditNotes.as_view(), name='edit'),
    path('notes/<int:pk>/delete', DeleteNotes.as_view(), name='delete'),
    path('create_new/', create_view, name='create_new'),
    path('create_new/upload_image', upload_image, name='upload_image'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('calendar/', calendar_view, name='calendar'),
    path('deadlines/', deadlines_view, name='deadlines'),
    path('music/', music_view, name='music'),
    path('trash/', trash_view, name='trash'),
    path('move_to_trash/', move_to_trash, name='movetotrash'),
    path('storage/', storage_view, name='storage'),
    path('summarization/', summarization_view, name='summarization'),
    ] + static(MEDIA_URL, document_root=MEDIA_ROOT)