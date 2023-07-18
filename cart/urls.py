from django.urls import path
from . import views
app_name = 'cart'

urlpatterns = [
    path('detail/', views.CartDetail.as_view(), name='cart_detail'),
    path('add/<int:good_id>/', views.CartAdd.as_view(), name='cart_add'),
    path('remove/<int:good_id>/', views.CartRemove.as_view(), name='cart_remove')
]