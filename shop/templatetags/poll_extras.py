from django import template

register = template.Library()

def search_itemTotal(dict_v,search_item):
    total = 0
    for iter in dict_v:
        for dict_item in iter:
            if dict_item == search_item:
                total+=iter[dict_item]
    return total

def subtract(item1,item2):
    return  item2-item1

register.filter('search_itemTotal',search_itemTotal)
register.filter('subtract',subtract)