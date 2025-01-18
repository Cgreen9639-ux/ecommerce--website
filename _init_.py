from django.http import HttpResponse
from django.urls import path
from django.contrib import admin
from django.urls import include
try:
    from myapp import views # type: ignore
except ImportError:
    import sys
    sys.path.append('..')
    from myapp import views # type: ignore

# Create a view in myapp/views.py

def home(request):
    return HttpResponse("Hello, world!")

# Map the view in myapp/urls.py

myapp_urlpatterns = [
    path('', views.home, name='home'),
]

# Include the app's URL configuration in myproject/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include((myapp_urlpatterns, 'myapp'), namespace='myapp')),
]