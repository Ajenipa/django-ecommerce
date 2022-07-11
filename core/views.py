from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView,View
from .models import Item,OrderItem,Order,BillingAddress
from django.utils import timezone
from django.contrib import messages
from .forms import CheckoutForm
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
class CheckoutView(View): 
    def get(self,*args,**kwargs):
        form = CheckoutForm()
        context = {
            'form':form
        } 
        return render(self.request,'checkout-page.html',context)
    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get("street_address")
                apartment_address = form.cleaned_data.get("apartment_address")
                country = form.cleaned_data.get("country")
                zip_code = form.cleaned_data.get("zip_code")
                #same_shipping_address = form.cleaned_data.get("same_shipping_address")
                #save_info = form.cleaned_data.get("save_info")
                #payment_option = form.cleaned_data.get("payment_option ")
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country ,
                    zip_code=zip_code
            )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                #TODO : add redirect to selected payment option
                #print(form.cleaned_data)
                #print("the form id valid")
                return redirect("core:check-out")
            print("FAILED")
            messages.warning(self.request, "Failed Checkout")
            
            return redirect("core:check-out")

        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an active order ")
            return redirect("core:order-summary")     
class ProductListView(ListView):
    model = Item
    template_name = "home.html"
    paginate_by = 10
class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object':order
            }
            return render(self.request,'order-summary.html', context )
        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an active order")
            return redirect('/')
        
class ProductDetailView(DetailView):
    model = Item
    template_name = 'product-detail.html'
@login_required
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
    return redirect("core:order-summary")

@login_required
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
                return redirect("core:order-summary")
        else:
            # add message that user does not have order
            
            messages.info(request, "this item was not in your cart")
            return redirect("core:product-detail", slug=slug)
            

    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product-detail", slug=slug)
@login_required
def remove_single_item_from_cart(request,slug):
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
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()                    
                else:
                    order.items.remove(order_item) 
                  
                messages.info(request, "this item quantity was updated")
                return redirect("core:order-summary")
        else:
            # add message that user does not have order
            
            messages.info(request, "this item was not in your cart")
            return redirect("core:product-detail", slug=slug)
            

    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product-detail", slug=slug)
