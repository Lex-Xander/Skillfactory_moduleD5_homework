from django import template

register = template.Library()


@register.filter(
    name='censor')  # регистрируем наш фильтр под именем censor, чтоб django понимал, что это именно фильтр, а не простая функция
def cut(value):
    Banned_List = ["блять", "ебать", "пиздец"]
    new_sentence = ""

    for word in value.lower().split():
        if word in Banned_List:
            new_sentence += '*** '
        else:
            new_sentence += word + ' '
    return new_sentence