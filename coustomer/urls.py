"""
URL configuration for coustomer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from coustomer import views
# from .views import confirm_order
from .views import confirm_order,add_to_cart,remove_item


urlpatterns = [
    path('add-to-cart/<int:product_id>', add_to_cart, name='add_to_cart'),
    path('remove-item/<int:product_id>', remove_item, name='remove_item'),
    path("confirm_order/", confirm_order, name="confirm_order"),
    path('admin', admin.site.urls),
    path('', views.homePage, name="dashboard"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/',views.logout, name='logout')
]
