from django.urls import path
from .views import OwnerCrudOperations, OwnerLogin, get_owners, get_customers, ManageUserView, activate_user, deactivate_user, get_inactive_users, search_users, CustomerLogin, CustomerProfile

urlpatterns = [
    path('registrationbyowner/', OwnerCrudOperations.as_view(), name='registration_by_owner'),
    path('loginbyowner/', OwnerLogin.as_view(), name='login_by_owner'),
    path('get-users/', get_owners, name='get_users'),
    path('get-customers/', get_customers, name='get_customers'),
    path("manage-users/<int:pk>/", ManageUserView.as_view(), name="manage-user"),
    path("activate-user/<int:pk>/", activate_user, name="activate-user"),
    path("deactivate-user/<int:pk>/", deactivate_user, name="deactivate-user"),
    path("get-inactive-users/", get_inactive_users, name="get-inactive-users"),
    path("search-users/", search_users, name="search-users"),
    path("customer-login/", CustomerLogin.as_view(), name="customer-login"),
    path("profile/", CustomerProfile.as_view(), name="customer-profile"),

]

