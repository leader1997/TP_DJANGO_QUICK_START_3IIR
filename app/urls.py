from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.list_products, name="product_list"),
    path('add_produit/', views.add_product, name="add_product"),
    path('delete_product/<int:product_id>/',
         views.delete_product, name="delete_product"),
    path('update_product/<int:product_id>/',
         views.update_product, name='update_product'),
         
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),

    path('add_cart/<int:product_id>',views.add_to_cart,name="add_to_cart"),
    path('add_cart/<int:product_id>/<int:quantity>',views.add_to_cart,name="add_to_cart_qte"),
    path('update_cart/<int:product_id>/<int:quantity>',views.add_to_cart,name="update_cart"),
    path('delete_cart/<int:product_id>',views.delete_from_cart,name="delete_cart"),
    path('cart/',views.get_cart,name="my_cart")

]
