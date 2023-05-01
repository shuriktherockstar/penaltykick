from django import forms
from django.contrib.auth.forms import UserCreationForm, User
from .models import Article, Comment


class FeedbackForm(forms.Form):
    SEX_CHOICES = (
        ('m', 'Мужской'),
        ('f', 'Женский'),
        ('none', 'Паркетный')
    )

    LEAGUE_CHOICES = (
        ('rus1', 'Российская Премьер-лига'),
        ('eng1', 'Английская Премьер-лига'),
        ('esp1', 'Ла Лига'),
        ('ger1', 'Бундеслига'),
        ('ita1', 'Серия А'),
        ('fra1', 'Лига 1'),
        ('other', 'Другая')
    )

    USABILITY_CHOICES = (
        ('5', 'Очень легко'),
        ('4', 'Легко'),
        ('3', 'Есть небольшие трудности'),
        ('2', 'Есть большие трудности'),
        ('1', 'Сайтом невозможно пользоваться'),
    )

    WILL_ADVISE_CHOICES = (
        ('yes', 'Да'),
        ('no', 'Нет'),
        ('idk', 'Затрудняюсь ответить')
    )

    name = forms.CharField(
        min_length=3,
        max_length=100,
        label='Ваше имя:'
    )
    sex = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=SEX_CHOICES,
        label='Ваш пол:'
    )
    favorite_league = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=LEAGUE_CHOICES,
        label='Выберите любимую лигу:'
    )
    impression = forms.CharField(
        widget=forms.Textarea,
        min_length=5,
        max_length=1000,
        label='Ваше впечатление о сайте:'
    )
    usability = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=USABILITY_CHOICES,
        label='Оцените удобство пользованием:'
    )
    whats_wrong = forms.CharField(
        widget=forms.Textarea,
        min_length=5,
        max_length=1000,
        label='Что не понравилось?'
    )
    will_advise = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=WILL_ADVISE_CHOICES,
        label='Посоветуете наш сайт?'
    )
    wants_to_add = forms.CharField(
        widget=forms.Textarea,
        min_length=5,
        max_length=1000,
        label='Что бы вы хотели увидеть на сайте?'
    )

    def clean_name(self):
        cleaned_name = self.cleaned_data.get('name')
        if cleaned_name and not cleaned_name.isalpha():
            raise forms.ValidationError('Имя может содержать только буквы')
        return cleaned_name

    def clean_favorite_league(self):
        cleaned_favorite_league = self.cleaned_data.get('favorite_league')
        if not cleaned_favorite_league:
            raise forms.ValidationError('Выберите хотя бы одну лигу')
        return cleaned_favorite_league

    def clean_usability(self):
        cleaned_usability = self.cleaned_data.get('usability')
        if not cleaned_usability:
            raise forms.ValidationError('Выберите хотя бы один вариант ответа')
        return cleaned_usability

    def clean_will_advise(self):
        cleaned_will_advise = self.cleaned_data.get('will_advise')
        if not cleaned_will_advise:
            raise forms.ValidationError('Выберите хотя бы один вариант ответа')
        return cleaned_will_advise


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, label='Имя пользователя')
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        email = self.cleaned_data['email']
        user.email = email
        if commit:
            user.save()
        return user


class CreateArticleForm(forms.ModelForm):
    title = forms.CharField(label='Введите название статьи')
    description = forms.CharField(label='Введите краткое описание статьи')
    content = forms.CharField(widget=forms.Textarea, label='Введите текст статьи')
    league = forms.ChoiceField(widget=forms.RadioSelect, choices=Article.LEAGUE_CHOICES, label='Выберите лигу')
    image = forms.ImageField(required=True, label='Добавьте изображение')

    class Meta:
        model = Article
        fields = ('title', 'description', 'content', 'league', 'image')


class CommentForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Поделитесь своим мнением...'}),
        min_length=3,
        max_length=1000,
        label=''
    )

    class Meta:
        model = Comment
        fields = ('text', )
