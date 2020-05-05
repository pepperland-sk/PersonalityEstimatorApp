from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'apiv1'

urlpatterns = [
    path('', views.MbtiAPIView.as_view()),
    # path('status/', include(views.approvereject)),
]