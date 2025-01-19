from django.urls import path
from . import views
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_view,name='login'),
    path('',views.home,name='home'),
    path('logout/',views.logout_view, name='logout'),
    path('sale_item/<int:item_id>/', views.sale_item, name='sale_item'),
    path('transaction/',views.transaction_view,name='transaction'),
    path('profit/',views.profit_view,name='profit'),
    path('expenses/',views.expenses_view,name='expenses'),
    path('expenses_history/',views.expenses_history_view,name='expenses_history'),
    path('additem/',views.additem_view,name='additem'),
    path('additem_history/',views.additem_history_view,name='additem_history'),
    path('statement/',views.statement_view,name='statement')
    # path('/sale_item/<id>/',views.sale_item,name='sale_item')
]
