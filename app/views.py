from django.shortcuts import render, redirect, get_object_or_404
from .forms import FeedbackForm, UserRegistrationForm, CreateArticleForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Article, Comment, Video
from .utils import format_date
from django.utils import timezone
from datetime import datetime, timedelta

year = '2023'
context = {'year': year}

def articles_list(request, league_name):
    if league_name is None:
        context['title'] = 'Главная'
        articles_carousel = Article.objects.all().filter(image__isnull=False).exclude(image=None).order_by('-date_published')[:3]
        articles = Article.objects.all().exclude(pk__in=articles_carousel).order_by('-date_published')
    else:
        context['title'] = f'{dict(Article.LEAGUE_CHOICES).get(league_name)} - последние статьи'
        articles_carousel = Article.objects.filter(league=league_name, image__isnull=False).order_by('-date_published')[:3]
        articles = Article.objects.filter(league=league_name).exclude(pk__in=articles_carousel).order_by('-date_published')

    articles_carousel_data_list = []
    for current_article in articles_carousel:
        article_data = {
            'id': current_article.id,
            'title': current_article.title,
            'description': current_article.description,
            'image': current_article.image
        }
        articles_carousel_data_list.append(article_data)

    context['articles_carousel'] = articles_carousel_data_list
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    articles_today = []
    articles_yesterday = []
    articles_other = []

    for current_article in articles:
        article_data = {
            'id': current_article.id,
            'title': current_article.title,
            'description': current_article.description,
            'date_published': current_article.date_published,
            'date_formatted': format_date(current_article.date_published)
        }
        if current_article.date_published.date() == today:
            articles_today.append(article_data)
        elif current_article.date_published.date() == yesterday:
            articles_yesterday.append(article_data)
        else:
            articles_other.append(article_data)
    context['articles_today'] = articles_today
    context['articles_yesterday'] = articles_yesterday
    context['articles_other'] = articles_other
    return render(request, 'app/articles_list.html', context=context)

def article(request, article_id):
    current_article = get_object_or_404(Article, id=article_id)

    leagues = {
        'rus1':
            {
                'name': 'Российской Премьер-лиге',
                'url': 'rpl'
            },
        'eng1':
            {
                'name': 'Английской Премьер-лиге',
                'url': 'efl'
            },
        'esp1':
            {
                'name': 'Ла Лиге',
                'url': 'laliga'
            },
        'ger1':
            {
                'name': 'Бундеслиге',
                'url': 'bundesliga'
            },
        'ita1':
            {
                'name': 'Серии А',
                'url': 'seriea'
            },
        'fra1':
            {
                'name': 'Лиге 1',
                'url': 'ligue1'
            }
    }

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment()
                comment.user = request.user
                comment.text = form.cleaned_data['text']
                comment.article = current_article
                comment.save()
            return redirect('article', article_id=current_article.id)
        else:
            form = CommentForm
    else:
        form = None

    comments = Comment.objects.filter(article=current_article).order_by('-date_created')
    for comment in comments:
        comment.formatted_date = format_date(comment.date_created)

    context['title'] = current_article.title
    context['article'] = current_article
    context['league'] = leagues[current_article.league]['name']
    context['league_url'] = leagues[current_article.league]['url']
    context['form'] = form
    context['comments'] = comments
    return render(request, 'app/article.html', context=context)

def pool(request):
    context['title'] = 'Обратная связь'

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form_data = {
                'name': form.cleaned_data['name'],
                'sex': dict(form.SEX_CHOICES)[form.cleaned_data['sex']],
                'favorite_league': dict(form.LEAGUE_CHOICES)[form.cleaned_data['favorite_league']],
                'impression': form.cleaned_data['impression'],
                'usability': dict(form.USABILITY_CHOICES)[form.cleaned_data['usability']],
                'whats_wrong': form.cleaned_data['whats_wrong'],
                'will_advise': dict(form.WILL_ADVISE_CHOICES)[form.cleaned_data['will_advise']],
                'wants_to_add': form.cleaned_data['wants_to_add'],
            }
            context['form_data'] = form_data
            context['form'] = None
        else:
            context['form'] = form
        return render(request, 'app/pool.html', context=context)
    else:
        form = FeedbackForm()
        context['form'] = form
    return render(request, 'app/pool.html', context=context)


def article_create(request):
    context['title'] = 'Новая статья'

    if request.method == 'POST':
        form = CreateArticleForm(request.POST, request.FILES)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.author = request.user
            new_article.date_published = timezone.now()
            new_article.save()
            return redirect('article', article_id=new_article.id)
    else:
        form = CreateArticleForm()

    context['form'] = form
    return render(request, 'app/article_create.html', context=context)

def videos(request):
    context['title'] = 'Видео'

    videos_list = Video.objects.all().order_by('-date_uploaded')[:10]
    context['videos'] = videos_list

    return render(request, 'app/videos.html', context=context)

def sign_up(request):
    context['title'] = 'Регистрация'

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    context['form'] = form
    return render(request, 'app/sign_up.html', context=context)


def sign_in(request):
    context['title'] = 'Авторизация'

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    context['form'] = form
    return render(request, 'app/sign_in.html', context=context)


def sign_out(request):
    logout(request)
    return redirect('home')

def not_found(request, path):
    context['title'] = 'Не найдено'
    return render(request, 'app/not_found.html', context=context)
