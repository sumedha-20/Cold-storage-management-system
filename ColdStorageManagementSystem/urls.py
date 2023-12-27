"""ColdStorageManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from ColdStorage.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', Signup_User, name='signup'),
    path('login/', Login_User, name='login'),
    path('logout/', Logout, name='logout'),
    path('login_admin/', Login_admin, name='login_admin'),
    path('admin_home/', admin_home, name='admin_home'),
    path('add_storage/', add_storage, name='add_storage'),
    path('manage_storage/', manage_storage, name='manage_storage'),
    path('edit_storage/<int:pid>', edit_storage, name='edit_storage'),
    path('delete_storage/<int:pid>', delete_storage, name='delete_storage'),
    path('apply_now/', apply_now, name='apply_now'),
    path('apply_now_selected/<int:pid>', apply_now, name='apply_now_selected'),
    path('view_booked_storage/', view_booked_storage, name='view_booked_storage'),
    path('view_detail_booked_storage/<int:pid>', view_detail_booked_storage, name='view_detail_booked_storage'),
    path('admin_view_detail_booked_storage/<int:pid>', admin_view_detail_booked_storage, name='admin_view_detail_booked_storage'),
    path('view_new_application_request/', view_new_application_request, name='view_new_application_request'),
    path('view_all_application_request/', view_all_application_request, name='view_all_application_request'),
    path('view_accepted_application_request/', view_accepted_application_request, name='view_accepted_application_request'),
    path('view_rejected_application_request/', view_rejected_application_request, name='view_rejected_application_request'),
    path('all_users/', all_users, name='all_users'),
    path('approve_request/<int:pid>', approve_request, name='approve_request'),
    path('find_by_date/', find_by_date, name='find_by_date'),
    path('search_report/', search_report, name='search_report'),
    path('user_Change_Password/', user_Change_Password, name='user_Change_Password'),
    path('admin_Change_Password/', admin_Change_Password, name='admin_Change_Password'),
    path('edit_user/', edit_user, name='edit_user'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('gallery/', gallery, name='gallery'),
    path('delete_user/<int:pid>', delete_user, name='delete_user'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
