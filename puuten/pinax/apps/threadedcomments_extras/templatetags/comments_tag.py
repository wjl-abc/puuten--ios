from django import template

register = template.Library()

def comments(context, obj):
    if 'user' in context:
        return {
            'object': obj,
            'request': context['request'],
            'user': context['user'],
        }
    else:
        return {
            'object': obj,
            'request': context['request'],
            'user': obj.sender,
        }

register.inclusion_tag('threadedcomments/comments.html', takes_context=True)(comments)

def comments_next(context, obj, next):
    if next:
        context['request'].path=next
    if 'user' in context:
        return {
            'object': obj,
            'request': context['request'],
            'user': context['user'],
        }
    else:
        return {
            'object': obj,
            'request': context['request'],
            'user': obj.sender,
        }

register.inclusion_tag('threadedcomments/comments_next.html', takes_context=True)(comments_next)
