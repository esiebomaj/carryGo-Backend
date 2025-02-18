from django.urls import path
from rest_framework.routers import DefaultRouter
from .import views

app_name = "core"

router = DefaultRouter()
router.register(r'packages', views.PackageViewset, basename="packages")
router.register(r'trackers', views.TrackerViewSet, basename="trackers")

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('wallets/<int:pk>/deposit/<int:amount>/', views.WalletDepositView.as_view(), name='deposit'),
    path('wallets/<int:pk>/withdraw/<int:amount>/', views.WalletWithrawView.as_view(), name='withdraw'),
    path('wallets/transfer/<int:amount>/', views.TranserView.as_view(), name='transfer'),

]
urlpatterns += router.urls
