from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Product
from .models import Category
from .models import Customer
from .models import Order
from django.contrib.auth.hashers import make_password,check_password
from django.views import View





class Index(View):
    def post(self,request):
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity= cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1

                        
                else:
                    cart[product]=quantity+1


               
            else:
                cart[product]=1


            
        else:
            cart={}
            cart[product]=1

        request.session['cart']=cart
        print('cart',request.session['cart'])

        return redirect('home')        


    def get(self,request):

        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}
        products=None
        
        
        categories=Category.get_all_categories()
        categoryID=request.GET.get('category')
        if categoryID:
             products=Product.get_all_products_by_categoryid(categoryID)

        else:
            products=Product.get_all_products()
        data={}
        data['products']=products
        data['categories']=categories
        print('you are:',request.session.get('email'))
        return render(request,'index.html',data)



    

class Signup(View):
    def get(self,request):
        return render(request, 'signup.html')

    def post(self,request):
        postData = request.POST
        username = postData.get('username')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'username': username,
            
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(username=username,
                            
                            phone=phone,
                            email=email,
                            password=password)
        
      
        

    
        
        if (not username):
            error_message = " Name Required !!"
       
        
        elif not phone:
            error_message = 'Phone Number required'
        
        elif not password:
            error_message = 'Password must be 6 char long'
        
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        if not error_message:
            print(username, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('home')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)
class Login(View):
    def get(self,request):
        return render(request , 'login.html')

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer']=customer.id
                
                return redirect('home')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')



class Cart(View):
    def get(self,request):
        ids=(list(request.session.get('cart').keys()))
        products=Product.get_products_by_id(ids)
        print(products)

        return render(request , 'cart.html',{'products':products})


        
class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Orders(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')



class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})