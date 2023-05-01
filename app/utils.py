from django.utils import timezone

def format_date(date) -> str:
    now = timezone.now()
    days_ago = (now - date).days
    if days_ago == 0:
        if now.hour < date.hour:
            return f'вчера в {date.strftime("%H:%M")}'
        else:
            return f'сегодня в {date.strftime("%H:%M")}'
    elif days_ago == 1:
        if now.hour < date.hour:
            return f'позавчера в {date.strftime("%H:%M")}'
        else:
            return f'вчера в {date.strftime("%H:%M")}'
    else:
        return date