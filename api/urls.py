from django.urls import path
from . import views

urlpatterns = [
    path('adduser/', views.user_list),
    path('createuser',views.create_user),
    path('delete-user/<int:uid>', views.user_delete),
    path('userlogin', views.user_login),
    path('saveresult',views.save_result),
    path('overrideResult',views.Override),
    path('showresult',views.show_result),
    path('showResultApp',views.show_result_app),
    path('recentResult', views.show_result_on_time),
    path('todayResult',views.show_today_result, name='todayResult'),
    path('adminlogin',views.Admin_login),
    path('updateAdminPass',views.update_admin_password),
    path('blockuser',views.Block_user),
    path('updateCredit',views.UpdateCredit),
    path('saveTransaction',views.save_transaction),
    path('showTransaction',views.show_transaction,name='showTransaction'),
    path('showAccount',views.show_Account_date),
    path('winPercentage',views.get_win_per),
    path('credit',views.Credit),
    path('redeem',views.Redeem_slip),
    path('cancelTsn/<str:tsn_id>',views.delete_tsn_entry),
    path('reprintSlip/<str:tsn_id>',views.ReprintSlip),
    path('userStatus/<str:uname>',views.User_status),
]
