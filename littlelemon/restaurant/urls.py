from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet, basename='booking')
router.register(r'users', views.UserViewSet, basename='api-user')

urlpatterns = [
    path('', views.index, name='home'),
    path('api/menu-items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('api/menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-item-detail'),
    path('api/', include(router.urls)),
]
