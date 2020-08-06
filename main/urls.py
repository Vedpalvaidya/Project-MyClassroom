from django.urls import path
from . import views

app_name : 'main'
urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('upload/<int:assn_no>',views.upload,name='upload'),
    path('student',views.student,name='student'),
    path('logout',views.logout,name='logout'),
    path('teacher',views.teacher,name='teacher'),
    path('assignment_structure',views.assign_structure,name='assign_structure'),
    path('remove_assignment/<int:assn_no>',views.remove_assn,name='remove_assn'),
    path('batch',views.batch,name='batch'),
    path('test',views.test,name='test'),
    path('about',views.about,name="about")

]