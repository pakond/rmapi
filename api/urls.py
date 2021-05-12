from django.conf.urls import url, include
from rest_framework import routers
from api.views import CompanyViewSet, ProfileViewSet, SmartphoneViewSet, CustomPasswordTokenVerificationView, ProductViewSet, StoreViewSet, StockViewSet
from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token
from django.urls import path


router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename="company")
router.register(r'profile', ProfileViewSet, basename="profile")
router.register(r'smartphones', SmartphoneViewSet, basename="smartphones")
router.register(r'products', ProductViewSet, basename="products")
router.register(r'storehouses', StoreViewSet, basename="stores")
router.register(r'stocks', StockViewSet, basename="stocks")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include('rest_auth.urls')),
    url(r'^register/', include('rest_auth.registration.urls')),
    path('reset_password/verify_token/', CustomPasswordTokenVerificationView.as_view(), name='password_reset_verify_token'),
    url(r'^reset_password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    url(r'^token_verify/', verify_jwt_token),
    url(r'^token_refresh/', refresh_jwt_token),
]