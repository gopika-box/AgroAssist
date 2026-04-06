from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MarketplaceItem
# Create your views here.

@login_required
def add_item(request):

    if request.method == "POST":
        MarketplaceItem.objects.create(
            user=request.user,
            name = request.POST['name'],
            category = request.POST['category'],
            price = request.POST['price'],
            quantity = request.POST['quantity'],
            description = request.POST.get('description'),
            contact_phone = request.POST.get('contact_phone'),
            image=request.FILES.get('image')
        )
        return redirect('marketplace:view_items')
    else:
        return render(request, 'farmers/add_item.html')
    


@login_required
def view_items(request):
    items=MarketplaceItem.objects.all().order_by('-created_at')
    
    # Officer view
    if request.user.role == 'officer':
        return render(request, 'officers/view_items.html', {
            'items':items
        })

    # Farmer view
    if request.user.role == 'farmer':
        return render(request, 'farmers/view_items.html', {
            'items':items
        })
    
    if request.user.role == 'customer':
        return render(request, 'customer/view_items.html', {
            'items':items
        })

    return redirect('accounts:login')



def edit_item(request, item_id):
    item = get_object_or_404(MarketplaceItem, id=item_id, user=request.user)

    if request.method == "POST":
        item.name = request.POST.get('name')
        item.category = request.POST.get('category')
        item.price = request.POST.get('price')
        item.quantity = request.POST.get('quantity')
        item.unit = request.POST.get('unit')
        item.description = request.POST.get('description')
        item.contact_phone = request.POST.get('contact_phone')

        if request.FILES.get('image'):
            item.image = request.FILES.get('image')

        item.save()
        return redirect('marketplace:view_items')

    return render(request, 'farmers/edit_item.html', {'item': item})


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(MarketplaceItem, id=item_id, user=request.user)

    if request.method == "POST":
        item.delete()
        return redirect('marketplace:view_items')

    return render(request, 'farmers/delete_item.html', {
        'item': item
    })