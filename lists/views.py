from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html')

def view_list(request, id):
    list_ = List.objects.get(id=id)
    return render(request, 'list.html', {'list':list_})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % list_.id)

def add_item(request, id):
    list_ = List.objects.get(id=id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % list_.id)