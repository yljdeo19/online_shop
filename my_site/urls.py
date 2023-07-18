from django.urls import path
from . import views
app_name = 'my_site'

urlpatterns = [
    path('index/', views.IndexView.as_view(),
     name='index'),
    path('index/<int:category>', views.IndexView.as_view(),
     name='index'),
    path('detail/<int:id>', views.DetailView.as_view(),
     name='detail'),
    path('registration', views.UserRegistrationView.as_view(), name='registration'),
    path('about', views.AboutView.as_view(), name='about'),
    path('contacts', views.ContactsView.as_view(), name='contacts'),
]
