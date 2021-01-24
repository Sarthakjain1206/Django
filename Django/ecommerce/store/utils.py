import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print("CArt:", cart)
    order = {'get_cart_total':0, 'get_cart_items':0}
    items = []
    cartItems = order['get_cart_items']

    # Build the order --- in this we are not saving anything from database, we are building the cart order from cart cookie
    for i in cart:
        # This try except block is implemented to avoid the error which guest user might encounter
        # As lets say user, few days back, added a particular item in a cart but after that admin deleted that product.
        # but that product still exists inside cookie. #!----
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i) #! so this line will throw an error as product is deleted from databse.
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            
            # mimic the items list of (logged in user) and pass it on template
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    
    return {'items': items, 'order': order, 'cartItems': cartItems}
    
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        #! get_or_create() method checks whether object exists or not if exists, it returns the object else create the new object.
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        ## OrderItem is connected to Order with foreign key, this means Order is parent of OrderItem
        # So, to access all orderitem of particular order in django, we need to follow this convention
        #! <parent model>.<child model>_set.all()
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items}
