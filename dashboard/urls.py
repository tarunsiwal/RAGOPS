import statistics
from django.urls import path, re_path
from ragopsmain import settings
from . import views
from account import views as acc_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    # user account urls
    path('login/',acc_views.login_user,name="login"),
    path('signup/',acc_views.signup,name="signup"),
    path('token/' , acc_views.token , name='token'),
    path('success/' , acc_views.success, name ='success'),
    path('verify/<auth_token>/' , acc_views.verify ,name = "verify"),
    path('error/' , acc_views.error , name = "error"),
    path('logout/', acc_views.logout_user, name='logout'),

    # dashboard screens pages
    path('',views.base,name="base"),
    path('choose-llm-model/',views.choose_llm,name="choose_llm"),
    path('vector-storing/',views.vector_storing,name="vector_storing"),
    path('get-API/',views.get_API,name="get_API"),
    path('data-connection/',views.data_connect,name="data_connect"),
    path('prompt-screen/',views.prompt_screen,name="prompt_screen"),
    path('track-query/',views.track_query,name="track_query"),

    path('chat-screen/',views.chat_screen,name="chat_screen"),
    path('chat-screen-temp/',views.chat_screen_temp,name="chat_screen_temp"),
    path('chat-history/',views.chat_history,name="chat_history"),
    # path('delete_chat_history/<uuid:chat_id>/', views.delete_chat_history, name='delete_chat_history'),
    path('delete_chat_history/<chat_id>/', views.delete_chat_history, name='delete_chat_history'),
    path('update-prompt/', views.update_prompt, name="update_prompt"),
    path('new-chat/', views.new_chat, name="new_chat"),
    path('upload-file', views.file_upload, name="file_upload"),
    # path('upload-file/<str:file_name>', views.file_upload, name="file_upload"),

    # API path
    path('api/chatlog/', views.ChatLogAPIView.as_view(), name='chatlog_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
