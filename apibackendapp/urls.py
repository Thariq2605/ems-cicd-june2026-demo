from rest_framework.routers import DefaultRouter
from .import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
#defaultrouter is a class that automatically creates URLs for viewset

router=DefaultRouter()
router.register(r'employees',views.employeeviewset)
router.register(r'departments',views.departmentviewset)
router.register(r'projects',views.projectviewset)

#signupAPIView is an APIView,not a viewset
urlpatterns=[
    path("signup/",views.signupapiview.as_view(),name="user-signup"),
    path("login/",views.loginapiview.as_view(),name="user-login"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
]

urlpatterns+=router.urls