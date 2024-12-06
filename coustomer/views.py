from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404
from products.models import products
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import products, cart 
from django.db.models import Sum, F


# from django.contrib.auth import logout



def homePage(request):
  
  productsdata = products.objects.all()
  user = request.user
  cartItems = cart.objects.filter(user_id = user.id).select_related('product')
  cart_data = {}
  for item in cartItems:
      total_price = item.product.product_price * item.quantity
      cart_data[item.product_id] = {
            'product_id': item.product.id,
            'product_name': item.product.product_name,  # Access product name via the related field
            'product_price': item.product.product_price,  # Access product price via the related field
            'quantity': item.quantity,  # Quantity from cart
            'total_price': total_price,
        }
      
      
  total_bill = cartItems.aggregate(total=Sum(F('quantity') * F('product__product_price')))['total'] or 0
  data = {
    'productsdata':productsdata,
    'cart_data': cart_data,
    'total_bill': total_bill,
  }
  return render(request, "main.html", data)

def update_cart_count(request):
  user = request.user
  cartItems = cart.objects.filter(user_id = user.id).select_related('product')
  

def add_to_cart(request, product_id):
    # Simulate adding the product to the cart (replace with your logic)
    product = get_object_or_404(products, id=product_id)
    user = request.user
    
    existing_cart_item = cart.objects.filter(user_id=user.id, product_id=product_id).first()
    if existing_cart_item:
          # Update the existing cart item's quantity
        # print("Existing Cart Item Quantity:", existing_cart_item.quantity)
        existing_cart_item.quantity += 1
        # print("New Quantity to Save:", existing_cart_item.quantity)
        existing_cart_item.save()
        # print("Updated Cart Item: ", existing_cart_item)
    else:
          data = cart.objects.create(
            user_id=user.id,
            product_id=product_id,
            quantity=1,
            )
    
    cartItems = cart.objects.filter(user_id=user.id)
    cart_items_with_total = []
    for item in cartItems:
      total_price = item.product.product_price * item.quantity
      cart_items_with_total.append({
        'product_id':item.product.id,
        'product_name': item.product.product_name,  # Access product name via the related field
        'product_price': item.product.product_price,  # Access product price via the related field
        'quantity': item.quantity,  # Quantity from cart
        'total_price': total_price,
      })
      
      total_bill = cartItems.aggregate(total=Sum(F('quantity') * F('product__product_price')))['total'] or 0
    return render(request, 'partials/cart.html', {'cartItems': cart_items_with_total, 'totalBill': total_bill,})
  
  
def remove_item(request, product_id):
    product = get_object_or_404(products, id=product_id)
    user = request.user
    existing_cart_item = cart.objects.filter(user_id=user.id, product_id=product_id).first()
    if existing_cart_item:
          # Update the existing cart item's quantity
        existing_cart_item.quantity -= 1
        if existing_cart_item.quantity == 0:
            existing_cart_item.delete()
        else:
            existing_cart_item.save()
    
    cartItems = cart.objects.filter(user_id=user.id)
    cart_items_with_total = []
    for item in cartItems:
      total_price = item.product.product_price * item.quantity
      cart_items_with_total.append({
        'product_id':item.product.id,
        'product_name': item.product.product_name,  # Access product name via the related field
        'product_price': item.product.product_price,  # Access product price via the related field
        'quantity': item.quantity,  # Quantity from cart
        'total_price': total_price,
      })
    print("New items cart: ", cart_items_with_total)
    print("cart items", cartItems)
    # Render a partial template for the cart item
    total_bill = cartItems.aggregate(total=Sum(F('quantity') * F('product__product_price')))['total'] or 0
    return render(request, 'partials/cart.html', {'cartItems': cart_items_with_total,'totalBill': total_bill, })
  
  

def signup(request):
  if request.method=='POST':
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    
    if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")
    
    singupdata = User.objects.create_user(username=username, email=email, password=password)
    singupdata.save()
    return redirect("login")
     
  return render(request, "signup.html")

def login(request):
  if request.method=="POST":
    username=request.POST['username']
    password=request.POST['password']
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
      auth.login(request, user)
      return redirect('dashboard')
    else:
            messages.error(request, "Invalid username or password entered.")
       
  return render(request, "login.html")



def logout(request):
  auth.logout(request)
  return redirect('login')
  
@login_required
def confirm_order(request):
  if request.method == "POST":
    user = request.user
    return redirect("dashboard")
  else:
      return redirect("dashboard")  
  
    





# def remove_from_cart(request, product_id):
#     user = request.user
#     cart_item = cart.objects.filter(user_id=user.id, product_id=product_id).first()

#     if cart_item:
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()

#             total_price = cart_item.quantity * cart_item.product.product_price
#             cart_item_data = {
#                 'id': cart_item.id,
#                 'product_name': cart_item.product.product_name,
#                 'product_price': cart_item.product.product_price,
#                 'quantity': cart_item.quantity,
#                 'total_price': total_price,
#             }

#             return render(request, 'partials/cart_item.html', {'cartItems': cart_item_data})
#         else:
#             cart_item.delete()
#             return HttpResponse(status=204)
#     else:
#         return HttpResponse(status=404)
  
  
# def remove_item(request, item_id):
#     # Get the cart from the session
#     cart = request.session.get('cart', {})
#     if item_id in cart:
#         del cart[item_id]

#     # Update session
#     request.session['cart'] = cart

#     # Return an empty response to indicate success
#     return JsonResponse({'success': True})
