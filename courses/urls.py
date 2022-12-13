from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='courses-home'),
    path('user/<str:user_id>', views.user, name='courses-user'),
    path('user/<str:user_id>/delete', views.user_delete, name='courses-user_delete'),
    path('user/<str:user_id>/change', views.user_change, name='courses-user_change'),


    path('user/<str:user_id>/courses', views.user_courses, name='courses-user_courses'),
    path('user/<str:user_id>/courses/create_course', views.create_course, name='courses-create_course'),

    path('course/<str:course_id>', views.course, name='courses-course'),
    path('course/<str:course_id>/new_review', views.new_review, name='courses-new_review'),
    path('course/<str:course_id>/pages', views.pages, name='courses-pages'),
    path('api/change_cur', views.pages_change_cur, name='courses-pages-change_cur'),
    path('course/<str:course_id>/new_page', views.new_page, name='courses-new_page'),
    path('course/<str:course_id>/delete', views.delete_course, name='courses-delete_course'),
    path('course/<str:course_id>/change', views.course_change, name='courses-course_change'),
    path('course/<str:course_id>/new_ticket', views.new_ticket, name='courses-new_ticket'),
    path('course/<str:course_id>/<str:page_id>/delete_page', views.delete_page, name='courses-delete_page'),

    path('lists/<str:list_id>', views.list, name='courses-list'),
    path('list/create', views.list_create, name='courses-list_create'),

    path('admin', views.admin, name="courses-admin"),
    path('admin/tickets', views.admin_tickets, name="courses-admin_tickets"),
    path('admin/tickets/<str:ticket_id>/delete', views.admin_ticket_delete, name="courses-admin_ticket_delete"),




    path('signin', views.signin, name='courses-signin'),
    path('login', views.login, name='courses-login'),
    path('logout', views.logout, name='courses-logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)