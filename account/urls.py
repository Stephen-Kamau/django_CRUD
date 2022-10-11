from django.conf.urls import include
from django.urls import re_path as url, path
from .import views


urlpatterns = [

    path("", views.home),
    #signin/up

    path("login/", views.login),
    path("signup/", views.signup),
    #meter urls.
    path('mater/', views.saveMater),
    path('mater/edit/<str:id>/',views.editMater),
    path('mater/update/<str:id>/',views.updateMater),
    path('mater/delete/<str:id>/', views.destroy),


    #employee urls
    path('emp/', views.saveEmp),
    path("dept/", views.addDept),
    path('emp/edit/<str:id>/', views.empEdit),
    path('emp/update/<str:id>/', views.empUpdate),
    path('emp/delete/<str:id>/', views.empDestroy),
]
