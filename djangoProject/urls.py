from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app import views

urlpatterns = [
    path('', views.articles_list, {'league_name': None}, name='home'),
    path('rpl', views.articles_list, {'league_name': 'rus1'}, name='rpl'),
    path('efl', views.articles_list, {'league_name': 'eng1'}, name='efl'),
    path('laliga', views.articles_list, {'league_name': 'esp1'}, name='laliga'),
    path('bundesliga', views.articles_list, {'league_name': 'ger1'}, name='bundesliga'),
    path('seriea', views.articles_list, {'league_name': 'ita1'}, name='seriea'),
    path('ligue1', views.articles_list, {'league_name': 'fra1'}, name='ligue1'),
    path('articles/<int:article_id>', views.article, name='article'),
    path('videos', views.videos, name='videos'),
    path('pool', views.pool, name='pool'),
    path('create_article', views.article_create, name='createarticle'),
    path('signup', views.sign_up, name='signup'),
    path('signin', views.sign_in, name='signin'),
    path('signout', views.sign_out, name='signout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.append(path('<path:path>', views.not_found, name='notfound'))
