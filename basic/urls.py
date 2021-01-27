
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    # path('quiz',views.quiz),
    path('loaderio-f3c731dc5ea8a201c360f115e6bedceb/',views.loaderio),
    
]
