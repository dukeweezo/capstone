from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from . import restapis


app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('registration/', views.registration_request, name='registration'),
    path(route='about', view=views.about, name='about'),
    path(route='contact', view=views.contact, name='contact'),

    path('api/review', restapis.get_reviews_from_cf, name='review'),


    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)