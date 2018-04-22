from django.conf.urls import url
from import_data.views import import_data_prime, main, restaurant, news, memory, paint, wallpapers, airhockey, photoshare, \
    jigsawpuzzle


urlpatterns = [
    url(r'^$', main, name='main'),
    url(r'^import_data_prime/$', import_data_prime, name='import_data_prime'),
    url(r'^restaurant/$', restaurant, name='restaurant'),
    url(r'^news/$', news, name='news'),
    url(r'^news/$', news, name='news'),
    url(r'^memory/$', memory, name='memory'),
    url(r'^paint/$', paint, name='paint'),
    url(r'^wallpapers/$', wallpapers, name='wallpapers'),
    url(r'^airhockey/$', airhockey, name='airhockey'),
    url(r'^photoshare/$', photoshare, name='photoshare'),
    url(r'^jigsawpuzzle/$', jigsawpuzzle, name='jigsawpuzzle'),
]