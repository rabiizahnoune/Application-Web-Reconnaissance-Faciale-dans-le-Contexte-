from django.urls import path
from . import views

urlpatterns=[
    path("select_class",views.select_class,name="select_class"),
    path("facial_recognition/<str:selected_class>/<str:selected_semester>",views.facial_recognition,name="facial_recognition"),
    path('result-page/', views.result_page, name='result_page'),
    path('login/', views.user_login, name='login'),
    path('importer_repertoire/', views.importer_repertoire, name='importer_repertoire'),
   


   
]