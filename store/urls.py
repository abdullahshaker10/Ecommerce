from django.urls import path
from . import views
urlpatterns = [
    path('', views.Store.as_view(), name='store'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('checkout/', views.CheckOut.as_view(), name='checkout'),
    path('add-to-chart/', views.AddtoChart.as_view(), name='add_to_chart'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout_'),
    path('api/orders/<pk>', views.AddtoChart.as_view()),
    path('api/items/<pk>', views.UpdateItem.as_view())

]
