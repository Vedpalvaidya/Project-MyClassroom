from django.urls import path
from . import views

urlpatterns = [
    path('editor/',views.editor, name='editor'),
    path('editor/<int:assn_no>',views.editorForSubmission, name='editorForSubmission'),
    path('Teditor/<str:run_path>/',views.Teditor,name='Teditor'),
    path('editor/compiler/',views.compiler_n,name='compiler1'),
    path('Teditor/<str:run_path>/compiler/',views.compiler, name='compiler2'),
    path('submit', views.submit,name='submit'),
]