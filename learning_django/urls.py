"""
URL configuration for learning_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),
    
    # Product endpoints
    path('products', views.product_list_create, name='product-list-create'),
    path('products/<int:product_id>', views.product_detail_update_delete, name='product-detail-update-delete'),
    
    # Cart endpoints
    path('carts', views.cart_list_create, name='cart-list-create'),
    path('carts/<int:cart_id>', views.cart_detail, name='cart-detail'),
    path('carts/<int:cart_id>/products', views.cart_add_get_products, name='cart-add-product'),
    path('carts/<int:cart_id>/products/<int:product_id>', views.cart_remove_product, name='cart-remove-product'),
    path('carts/<int:cart_id>/pay', views.cart_pay, name='cart-pay'),
    
    # Swagger/OpenAPI documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
