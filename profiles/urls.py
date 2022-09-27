from django.urls import path
from profiles import views

urlpatterns = [
    path('<str:user_name>/', views.profileHome, name='profileHome'),
    path('<str:user_name>/edit', views.profileEdit, name='profileEdit'),
    path('userprofile/<str:username>', views.userProfile, name='userProfile'),
    path('<str:user_name>/sms', views.sms, name='sms'),
    path('checksms/<str:username>', views.checksms, name='checksms'),
    path('sendsms/<str:username>', views.sendsms, name='sendsms'),
    # path('report/<str:username>', views.report, name='report'),

]
