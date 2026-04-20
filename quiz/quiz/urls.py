"""
URL configuration for quiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from authentication.views import signup_view,login_view
from quizapp.views import dashboard_view
from quizapp.views import quizform_view
from quizapp.views import myquizzes_view
from quizapp.views import profile_view
from quizapp.views import takequiz_view
from authentication.views import logout_view
from quizapp.views import result_view
from quizapp.views import allquiz_views,delete_quiz



urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',signup_view,name='signup'),
    path('login/',login_view,name='login'),
    path('',dashboard_view,name= 'dashboard'),
    path('form/',quizform_view,name= 'quizform'),
    path('myquiz/',myquizzes_view,name= 'myquiz'),
    path('profile/',profile_view,name='profile'),
    path('logout/',logout_view,name='logout'),
    path('quiz/<int:quiz_id>/',takequiz_view,name='takequiz'),
    path('result/<int:quiz_id>/',result_view,name='result'),
   
    path('allquiz/',allquiz_views,name='allquiz'),
    path('delete_quiz/<int:quiz_id>/',delete_quiz,name='deletequiz'),]
    





from quizapp import views
