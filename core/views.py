from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView
from .models import Item,OrderItem,Order
from django.utils import timezone
from django.contrib import messages
# Create your views here.
def list_view(request):
    items = Item.objects.all()
    context = {
        'items':items
    }
    return render(request,'home.html',context)
def checkout_view(request):
    return render(request,'checkout-page.html')
def productpage_view(request):
    return render(request,'product-page.html')
class ProductListView(ListView):
    model = Item
    template_name = "home.html"
class ProductDetailView(DetailView):
    model = Item
    template_name = 'product-detail.html'

def add_to_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_item,created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(order_qs)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            print("order item is here")
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "this item quantity was updated")
        else:
            print("no order iteme here")
            order.items.add(order_item)
            messages.info(request, "this item was added to cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date =  ordered_date)
        order.items.add(order_item)       
        messages.info(request, "this item was added to cart")
    return redirect("core:product-detail",slug=slug)
def remove_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item = item,
                    user = request.user,
                    ordered = False
                )[0]
                order.items.remove(order_item)    
                messages.info(request, "this item was removed from cart")
                return redirect("core:product-detail", slug=slug)
        else:
            # add message that user does not have order
            
            messages.info(request, "this item was not in your cart")
            return redirect("core:product-detail", slug=slug)
            

    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product-detail", slug=slug)
