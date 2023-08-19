from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpRequest
from django.contrib.auth.models import User, Group
from .models import *
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import MerchantDiscountForm
from django.http import JsonResponse

def finish_order(request, order_id):
    try:
        order = Orders.objects.get(order_id=order_id, orderStatus='On-going')
        order.orderStatus = 'Finished'
        order.order_time_finished = timezone.now()
        order.save()
        return JsonResponse({'success': True})
    except Orders.DoesNotExist:
        return JsonResponse({'success': False})



def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to the user page
        else:
            messages.info(request, "Username or Password is Incorrect")
    return render(request, 'Store\login.html')

def logoutUser(request):
    logout(request)
    return redirect('/')


def create_user(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save()

            group_name = form.cleaned_data['group']
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            return redirect('login')
    context = {'form': form}
    return render(request, 'Store\createUser.html', context)


def store_view(request):
    username = request.user.username
    try:
        user = User.objects.get(username=username)
        groups = user.groups.all()

        group_names = [group.name for group in groups]
        print("WORKIGN ")
        print(group_names)

    except:
        print("NOT WORKIGN ")
        pass
    ebooks = {'eBooks': Ebook.objects.all(), 'username': username}

    return render(request, 'Store\index.html', ebooks)

def cart_view(request):
    username = request.user.username
    user = User.objects.get(username=username)
    objs = Cart.objects.filter(user_id = user.id).select_related('product')
    userprods = Cart.objects.filter(user_id= user.id)
    totalPrice = 0
    if request.method == "POST":
        productAdd = request.POST.get('Add')  #adds product to the list\
        productSub = request.POST.get('Remove')
        checkout = request.POST.get('checkout')

        if productAdd != None:
            tempqty = Cart.objects.get(user_id=user.id, product_id=productAdd).quantity
            tempqty += 1
            Cart.objects.filter(product_id=productAdd, user_id=user.id).update(quantity=tempqty)
        elif productSub != None:
            tempqty = Cart.objects.get(user_id=user.id, product_id=productSub).quantity
            tempqty -= 1
            if tempqty == 0:
                Cart.objects.filter(product_id=productSub, user_id=user.id).delete()
            else:
                Cart.objects.filter(product_id=productSub, user_id=user.id).update(quantity=tempqty)
        elif checkout!=None:
            print("incheckout")
            order = Orders(user_id=1, product_id=1 , tableNumber=1, quantity=1, totalPrice =1 , paymentStatus="paid" , orderStatus="Finished")
            order.save()






            return redirect('checkout')

        return HttpResponseRedirect(reverse('cart'))

    for items in userprods:
        unitprc = items.product.price
        totalPrice += unitprc * items.quantity
    ctx = { 'username': username, 'cartV': objs, 'totalPrice':totalPrice}
    return render(request, 'Store\cart.html', ctx)

def menu_view(request):
    username = request.user.username
    store = request.POST.get('shop')  # Assuming you're getting the 'shop' from POST data
    userO = User.objects.get(username=username)

    # Fetch the id from the request (POST or GET)
    id = request.POST.get('id') or request.GET.get('id')

    if request.method == 'POST':
        product_id = request.POST.get("food_id")

        try:
            prod_exists = Cart.objects.filter(user_id=userO.id, product_id=product_id).exists()
            if prod_exists == False:
                product = Cart(product_id=product_id, user_id=userO.id, quantity=1)
                product.save()
            else:
                tempqty = Cart.objects.get(user_id=userO.id, product_id=product_id).quantity
                tempqty += 1
                Cart.objects.filter(product_id=product_id, user_id=userO.id).update(quantity=tempqty)
            messages.info(request, "Product added to the cart!")

        except:
            pass

    products = Product.objects.all()
    discounted_prices = {}

    for product in products:
        merchant_discounts = MerchantDiscount.objects.filter(store=product.store, merchant=userO)
        if merchant_discounts.exists():
            discounted_price = product.price * (1 - merchant_discounts.first().discount_percentage / 100)
            discounted_prices[product.id] = discounted_price
        else:
            discounted_prices[product.id] = product.price

    menu = redir(store, id)
    ctx = {
        'menu' : menu,
        'products': products,  # Corrected variable name here
        'store': store,
        'username': username,
        'discounted_prices': discounted_prices
    }
    return render(request, 'Store\menu.html', ctx)


#@login_required
def merchant_view(request):
    if request.method == 'POST':
        form = MerchantDiscountForm(request.POST)
        if form.is_valid():
            discount_percentage = form.cleaned_data['discount_percentage']
            store = form.cleaned_data['store']

            # Assuming the user is a merchant
            merchant = request.user

            # Apply the discount to all products of the selected store

            products = Product.objects.filter(store=store)
            for product in products:
                merchant_discount = MerchantDiscount(store=store, discount_percentage=discount_percentage, merchant=merchant)
                merchant_discount.save()

            # Redirect or render a response
            return redirect('menu')  # Replace with the actual URL name for the menu view
    else:
        form = MerchantDiscountForm()

    ongoing_orders = Orders.objects.filter(orderStatus='On-going')
    finished_orders = Orders.objects.filter(orderStatus='Finished')
    return render(request, 'merchant.html', {'form': form, 'ongoing_orders': ongoing_orders,
        'finished_orders': finished_orders})
def checkout(request):
    username = request.user.username

    ctx = {'username': username}
    return render(request, 'Store\checkout.html', ctx)
