from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('setting/<int:pk>', views.SettingView.as_view(), name='setting'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('group/create/', views.GroupCreateView.as_view(), name='group_create'),
    path('group/update/<int:pk>', views.GroupUpdateView.as_view(), name='group_update'),
    path('group/detail/<int:pk>', views.GroupDetailView.as_view(), name='group_detail'),
    path('group/invite/<int:pk>', views.GroupInviteView.as_view(), name='group_invite'),
    path('group/requests/<int:pk>', views.GroupRequestView.as_view(), name='group_request'),
    path('group/quit/confirm/<int:pk>', views.GroupQuitConfirmView.as_view(), name='group_quit_confirm'),
    path('group/quit/done/<int:pk>', views.GroupQuitDoneView.as_view(), name='group_quit_done'),
    path('group/join/request/confirm/<int:pk>', views.GroupJoinRequestConfirmView.as_view(), name='group_join_request_confirm'),
    path('group/join/request/done/<int:pk>', views.GroupJoinRequestDoneView.as_view(), name='group_join_request_done'),
    path('group/join/accept/<int:pk>', views.GroupJoinAcceptView.as_view(), name='group_join_accept'),
]
