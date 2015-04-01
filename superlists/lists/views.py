from django.shortcuts import redirect, render
from lists.models import Item, List
from django.http import HttpResponse


# Create your views here.
def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id, ))


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)

    #just testing:
    if request.method == "GET":
        return redirect('/lists/%d/' % (list_.id,))

    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))


# if request.method == 'POST':
# 	return render(request, 'home.html', {
# 		'new_item_text': request.POST['item_text'],
# 		})
