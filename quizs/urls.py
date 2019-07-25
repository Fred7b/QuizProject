from django.conf.urls import url
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    url(r'^@(?P<username>\w+)/$', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('examinee/', include(([
        path('', views.QuizListView.as_view(), name='quiz_list'),
        path('taken/', views.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', views.take_quiz, name='take_quiz'),
    ], 'examinee'), namespace='examinee')),
]
