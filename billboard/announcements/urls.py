from django.urls import path
from .views import AnnouncementsList, AnnouncementDetail, AnnouncementCreate, \
                   AnnouncementUpdate, AnnouncementDelete, comments_list, \
                   comment_create, comment_approve, comment_update, comment_delete


urlpatterns = [
   path('', AnnouncementsList.as_view(), name='announcements'),
   path('announcements/<int:pk>', AnnouncementDetail.as_view(), name='announcement'),
   path('announcements/create/', AnnouncementCreate.as_view(), name='announcement_create'),
   path('announcements/<int:pk>/update/', AnnouncementUpdate.as_view(), name='announcement_update'),
   path('announcements/<int:pk>/delete/', AnnouncementDelete.as_view(), name='announcement_delete'),
   path('comments/', comments_list, name='comments'),
   path('announcements/<int:pk>/comments/create/', comment_create, name='comment_create'),
   path('announcements/<int:pk1>/comments/<int:pk2>/approve/', comment_approve, name='comment_approve'),
   path('announcements/<int:pk1>/comments/<int:pk2>/update/', comment_update, name='comment_update'),
   path('announcements/<int:pk1>/comments/<int:pk2>/delete/', comment_delete, name='comment_delete'),
]
