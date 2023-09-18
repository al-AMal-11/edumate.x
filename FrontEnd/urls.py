from django.contrib import admin
from django.urls import path , include


from . import views 
urlpatterns = [
    path('', views.home,name='home_page' ),
    path('about/', views.about,name='about_page' ),
    path('recent_news/<str:news>', views.news_r,name='news_page' ),
    path('admission/',views.admission , name='admission'),
    path('admission/post',views.request_admission_assistance , name='admission_post'),
    path('contacts/', views.contacts,name='contacts_page' ),
    path('contacts/save', views.contact_form,name='contacts_save' ),
   
    path('logout/', views.dologout,name='user_logout' ),
    

    
]
