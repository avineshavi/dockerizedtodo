from django.urls import path
from core.views import (
    index,
    todo_create_view, 
    todo_update_view,
    delete_view,
    send_email, 
    filter_records
    )

urlpatterns = [
    # path("", root, name=""),
    path("", index, name='index'),
    path('create-task/', todo_create_view, name='create-task'),
    path('update-task/<int:id>/', todo_update_view, name='update-task'),
    path('ajax-delete-task/<int:id>/', delete_view, name='delete-task'),
    path('send-email/', send_email, name='send-email'),
    path('filter-records/', filter_records, name='filter-records'),

]
