from ast import Store
from datetime import datetime,timezone
from venv import create
from django.http import HttpResponse, HttpResponseForbidden
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.storage import FileSystemStorage
from . models import  Chat, Complaint, Delivery, DeliveryBoy, Login, OrderDetails, OrderMaster, Payment, Product, Rating, SetToDeliver, Shop, Stock, Type, User

# Create your views here.

def home(request):
    return render(request,'MediTrust/index.html')

def shopehome(request):
    s=request.session['sid']
    return render(request,'shome.html',{'s':s})

def deliveryhome(request):
    d=request.session['did']
    return render(request,'deliveryboyhome.html')

def userhome(request):
    d=request.session['uid']
    return render(request,'userhome.html')
       
def homeee(request):
     return render(request,'home2.html')

def login(request):
    if 'submit' in request.POST:
        username=request.POST['username']
        password=request.POST['password']
        try:
            log=Login.objects.get(username=username,password=password)
        except:
                return HttpResponse("<script>alert('incorrect username and password!');window.location='/login'</script>")

        try:
                log = Login.objects.get(username=username, password=password)
                if log.user_type == 'admin':
                    return HttpResponse("<script>alert('Logged in successfully!');window.location='/adminhome'</script>")
                elif log.user_type == 'shop':
                    s=Shop.objects.get(login_id=log.id)
                    if s.status == 'pending':
                        return HttpResponse("<script>alert('Sorry, Not yet Accepted');window.location='/login'</script>")
                    else:
                        request.session['sid'] = log.id
                        return HttpResponse("<script>alert('Logged in successfully!');window.location='/shome'</script>")
                elif log.user_type == 'deliveryboys':
                    request.session['did'] = log.id
                    return HttpResponse("<script>alert('Logged in successfully!');window.location='/deliveryboyhome'</script>")
                elif log.user_type == 'user':
                    request.session['uid'] = log.id
                    return HttpResponse("<script>alert('Logged in successfully!');window.location='/userhome'</script>")
                else:
                    return HttpResponse("<script>alert('incorrect username and password!');window.location='/login'</script>")
        except Login.DoesNotExist:
                return render(request,'login.html', {'error': 'Invalid username or password'})
        

    return render(request,'login.html')

def user(request):
    if 'submit' in request.POST:
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        h=request.POST['house_name']
        pincode=request.POST['pincode']
        phone=request.POST['phone']
        place=request.POST['place']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        log=Login(username=username,password=password,user_type='user')
        log.save()
        r=User(first_name=first_name,last_name=last_name,house_name=h,pincode=pincode,phone=phone,place=place,email=email,login_id=log.pk)
        r.save()
        return HttpResponse("<script>alert('Regstration Successfully!');window.location='/login'</script>")
    return render(request,'user.html')


def admin_home(request):
    return render(request,'adminhome.html')

def product(request):
    products = Product.objects.all()
    return render(request,'products.html',{'p':products})


def viewcustomer(request):
    c=User.objects.all()
    if 'submit' in request.POST:
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        cu=User(name=name,email=email,phone=phone,address=address)
        return HttpResponse("<script>alert('customer added');window.location='/user'</script>")
    return render(request,'viewcustomer.html',{'c':c})

def type(request):
    e=Type.objects.all()
    if 'submit' in request.POST:
        name=request.POST['name']
        eq=Type(type_name=name)
        eq.save()
        return HttpResponse("<script>alert('added');window.location='/type'</script>")
    return render(request,"addequipment.html",{'e':e })

def viewstock(request):
    s=Stock.objects.all()
    if 'submit' in request.POST:
        name=request.POST['name']
        quantity=request.POST['quantity']
        s=Stock(name=name,quantity=quantity)
        s.save()
        return HttpResponse("<script>alert('added stock');window.location='/viewstocks'</script>")
    return render(request,'viewstocks.html',{'s':s})




def viewtype(request):
    t=Type.objects.all()
    if 'submit' in request.POST:
        type=request.POST['type']
        t=Type(type=type)
        return HttpResponse("<script>alert('added');window.location='/type'</script>")
    return render(request,'type.html',{'t':t})

def delivery(request):
    dc=DeliveryBoy.objects.all()
    if 'submit' in request.POST:
       first_name=request.POST['first_name'] 
       last_name=request.POST['last_name'] 
       house_name=request.POST['house_name']
       phone=request.POST['phone'] 
       pincode=request.POST['pincode'] 
       place=request.POST['place'] 
       email=request.POST['email']
       username=request.POST['username']
       password=request.POST['password']
       log=Login(username=username,password=password,user_type='deliveryboys')
       log.save()
       d=DeliveryBoy(first_name=first_name,last_name=last_name,house_name=house_name,pincode=pincode,phone=phone,place=place,email=email,login_id=log.pk)
       d.save()
       return HttpResponse("<script>alert('registered');window.location='/delivery'</script>")
    return render(request,"delivery.html",{'d':dc})

def dedit(request,id):
    dc=DeliveryBoy.objects.get(id=id)
    if 'edit' in request.POST:
       dc.first_name=request.POST['first_name'] 
       dc.last_name=request.POST['last_name'] 
       dc.house_name=request.POST['house_name']
       dc.phone=request.POST['phone'] 
       dc.pincode=request.POST['pincode'] 
       dc.place=request.POST['place'] 
       dc.email=request.POST['email']
       dc.save()
       return HttpResponse("<script>alert('Delivery boy details edited');window.location='/delivery'</script>")
    return render(request,"delivery.html",{'de':dc})

def ddelete(request,id):
    ee=DeliveryBoy.objects.get(id=id)
    ee.delete()
    return HttpResponse("<script>alert('Delivery Boy deleted');window.location='/delivery'</script>")


def viewshop(request):
    s=Shop.objects.all()
    return render(request,"viewshop.html",{'s':s})

def approve_reject_shop(request,sid):
    shop = get_object_or_404(shop,id=sid)
    if request.method == 'POST':
         action = request.POST['action']
    if action == 'approve':
            shop.status = 'approved'
    elif action == 'reject':
            shop.status = 'rejected'
    
    shop.save()
    return render(request,'reject.html',{'shop':shop})

def saccepted(request,id):
    s=Shop.objects.all()
    e=Shop.objects.get(id=id)
    e.status='accepted'
    e.save()
    return HttpResponse("<script>alert('Shop Accepted');window.location='/viewshop'</script>")

def srejected(request,id):
    s=Shop.objects.all()
    e=Shop.objects.get(id=id)
    e.status='rejected'
    e.save()
    return HttpResponse("<script>alert('Shop Rejected');window.location='/viewshop'</script>")

def view_complaints(request):
    co=Complaint.objects.all()
    if 'submit' in request.POST:
        r=request.POST['reply']
        id=request.POST['id']
        o=Complaint.objects.get(id=id)
        o.reply=r
        o.save()
        return HttpResponse("<script>alert('replied');window.location='/viewcomplaint'</script>")
    return render(request,"viewcomplaints.html",{'co':co})
        
     
#MODULE2 SHOP

def shopreg(request):
    s=Shop.objects.all()
    if 'submit' in request.POST:
        shop_name=request.POST['shop_name']
        place=request.POST['place']
        landmark=request.POST['landmark']
        phone=request.POST['phone']
        email=request.POST['email']
        status='pending'
        username=request.POST['username']
        password=request.POST['password']
        log=Login(username=username,password=password,user_type='shop')
        log.save()
        shop = Shop(shop_name=shop_name,place=place,landmark=landmark,phone=phone,email=email,status=status,login_id=log.pk)
        shop.save()
        return HttpResponse("<script>alert('Shop registered successfully');window.location='/login'</script>")
    return render(request,"shopreg.html",{'s':s})

def stype(request):
    t = Type.objects.all()
    if 'submit' in request.POST:
        type_name = request.POST['type']
        t1=Type(type_name=type_name)
        t1.save()
        return HttpResponse("<script>alert('added');window.location='/stype'</script>")
           
    t = Type.objects.all()
    return render(request,"stype.html",{'t':t})

def sproducts(request):
    u=request.session['sid']
    cw=Shop.objects.get(login_id=u)
    ss=Product.objects.filter(shop_id=cw.id)
    t=Type.objects.all()
    if 'submit' in request.POST:
        product=request.POST['product_name']
        details=request.POST['details']
        type=request.POST['type']
        price=request.POST['price']
        image=request.FILES['img']
        fs = FileSystemStorage()
        saved_path=fs.save(image.name,image)
        shop_id=cw.id
        sp=Product(product_name=product,details=details,price=price,shop_id=cw.id,type_id=type, image=saved_path)
        sp.save()
        return HttpResponse("<script>alert('added products');window.location='/manage'</script>")
    return render(request,'manage.html',{'ss':ss,'t':t})

def edited(request,pid):
    sid=request.session['sid']
    cw=Shop.objects.get(login_id=sid)
    ss=Product.objects.filter(shop_id=cw.id)
    o=Product.objects.get(id=pid)
    t=Type.objects.all()
    if 'update' in request.POST:
        o.product=request.POST['product_name']
        o.details=request.POST['details']
        o.type_id=request.POST['type']
        o.price=request.POST['price']
        image = request.FILES['img']
        fs=FileSystemStorage()
        saved_path=fs.save(image.name,image)
        o.image=saved_path #update
        
        o.save()
        return HttpResponse("<script>alert('Updated!');window.location='/manage'</script>")   
    return render(request,"manage.html",{'ss':ss,'o':o,'t':t})

def deletepr(request,id):
    dp=Product.objects.get(id=id)
    dp.delete()
    return HttpResponse("<script>alert('Product Deleted');window.location='/manage'</script>")

def orders(request):
    r=request.session['sid']
    dh=Shop.objects.get(login_id=r)
    j=OrderMaster.objects.filter(shop_id=dh)
    hi=j.values_list('id',flat=True)
    o=OrderDetails.objects.filter(order_master_id__in=hi)
    return render(request,"vieworder.html",{'orders':o})
        
def oaccepted(request,id):  
    o=OrderMaster.objects.get(id=id)
    d=DeliveryBoy.objects.all()
    o.status='accepted'
    o.save()
    return render(request,"dblist.html",{'db':d,'o':id})


def orejected(request,id):
    o=OrderMaster.objects.get(id=id)
    o.status='rejected'
    o.save()
    return HttpResponse("<script>alert('rejected!');window.location='/vieworder'</script>")

def viewpayments(request):  
    o=request.session['sid']
    h=Shop.objects.get(login_id=o)
    we=OrderMaster.objects.filter(shop_id=h)
    eg=we.values_list('id',flat=True)
    pa=Payment.objects.filter(order_master_id__in=eg)
    return render(request,"viewpayments.html",{'pay':pa})


def viewrating(request):
    sid=request.session['sid']
    n=Shop.objects.get(login_id=sid)
    r=Rating.objects.filter(product_id=n.id)
    return render(request,"viewrating.html",{'ratings':r,'n':n})

# def chat(request):
#     ch=Chat.objects.all()
#     return render(request,"chat.html",{'chats':ch})

# module 3

def viewassignorder(request):
    va = SetToDeliver.objects.filter(status='Assigned')
    return render(request,"orderass.html",{'aorders':va})      
 
def pickup(request):
    up=SetToDeliver.objects.filter()
    up.status = 'pickedup'
    return render(request,"orderass.html",{'pickorders':up})

def pickeduporder(request):
    pr=SetToDeliver.objects.filter(status='Picked')
    return render(request,"vieworderpick.html",{'orders':pr})

def update_delivery(request,id):
    dc=get_object_or_404(Delivery,id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in['delivered']:
            dc.status=new_status
            dc.save()
    return render(request,"update.html",{'orders':dc})

# module4
def shops(request):
    t=Shop.objects.filter(status='accepted')
    print(t)
    return render(request,"shop1.html",{'shops':t})

def productss(request,id):
    ch=Shop.objects.get(id=id)
    ps=Product.objects.filter(shop_id=ch.id)
    print(ps)
    return render(request,"view_products.html",{'ps':ps})
from django.db.models import Q

def userchat(request,sid):
    ui=request.session['uid']
    s=Shop.objects.get(id=sid)
    si=s.login_id
    print(ui,si)
    c=Chat.objects.filter(
        Q(sender_id=ui, receiver_id=si) |
        Q(sender_id=si, receiver_id=ui)
    )
    if 'submit' in request.POST:
        chat=request.POST['chat']
        date_time=datetime.now()
        nc=Chat(sender_id=ui,message=chat, receiver_id=si,date=date_time, sender_type='User', receiver_type='Shop')
        nc.save()
    return render(request,"chatuser.html",{'c':c})

# def shopchatview(request):
#     u=User.objects.all()
#     return render(request,"chatshop.html",{'c':u})

def shopchat(request,uid):
    si=request.session['sid']
    u=User.objects.get(id=uid)
    ui=u.login_id
    c=Chat.objects.filter(
        Q(sender_id=ui, receiver_id=si) |
        Q(sender_id=si, receiver_id=ui)
    )
    if 'submit' in request.POST:
        chat=request.POST['chat']
        date_time=datetime.now()
        nc=Chat(sender_id=si,message=chat, receiver_id=ui,date=date_time, sender_type='Shop', receiver_type='User')
        nc.save()
    return render(request,"chatshop.html",{'c':c})

def Shopuservew(request,id):
    u= User.objects.all()
    return render(request,'userviewshop.html',{'c':u})


def addtocart(request,pid,price):
    ps = Product.objects.get(id=pid)
    uid=request.session['uid']
    u=User.objects.get(login_id=uid)
    if 'add_cart' in request.POST:
        qty = int(request.POST['qty']) 
        total = float(request.POST['total'])  

        try:
            res = OrderMaster.objects.get(user_id=u.pk, status='pending')
            res.total = float(res.total) + total
            res.save()

        except OrderMaster.DoesNotExist:
            current_datetime = datetime.now()
            res = OrderMaster(total=total, date_time=  datetime.now(), status='pending', user_id=u.pk, shop_id=ps.shop_id)
            res.save()
        try:
            res1 = OrderDetails.objects.get(order_master_id=res.pk,product_id=pid)
            res1.quantity = float(res1.quantity) + qty
            res1.amount=float(res1.amount)+total
            res1.save()

        except OrderDetails.DoesNotExist:
            order_detail = OrderDetails(order_master_id=res.pk,product_id=pid,quantity=qty,amount=price)
            order_detail.save()
        return HttpResponse("<script>alert('Product Added To Cart Successfully!');window.location='/shop1'</script>")
    return render(request,"cart.html",{'pro_details':ps})

def sortbyrating(request, sid):
    sort_by = request.GET.get('sort')
    products = Product.objects.filter(shop_id=sid)
    if sort_by == 'rating':
        products= products.annotate(avg_rating=('ratings__rating')).order_by('-avg_rating')
    return render(request,"rating1.html",{'products':products,'shop_id':sid})

def category(request,sid,category_id):
    products=Product.objects.filter(shop_id=sid,category_id=category_id)
    return render(request,"category.html",{'cat':products})


def productdetails(request, pid):
    product = Product.objects.get(id=pid)
    return render(request,"productdetails.html",{'product':product})

def viewcart(request):
    try:
        u=request.session['uid']
        a=User.objects.get(login_id=u)
        oe=OrderMaster.objects.get(user_id=a.id,status='pending')
        od=OrderDetails.objects.filter(order_master_id=oe.id)
        print(oe,'i')
    except:
        od=[]
        oe=''
        print('l')
    return render(request,"viewcart.html",{'o':od, 'om':oe})

def makepayment(request,id):
    u=request.session['uid']
    oe=OrderMaster.objects.filter(user_id=u)
    print(oe)
    if 'submit' in request.POST:
        m =Payment(amount=u.total,order_master_id=id,date=datetime.now(),status='pending')
        m.save()
        print('ggggggggggg',m)
        return HttpResponse("<script>alert('Payment done!');window.location='/makepay'</script>")
    return render(request, "makepay.html",{'a':oe})
    
def choosedelivery(request):
    co=Delivery.objects.all()
    if 'submit' in request.POST:
        delivery_type = request.POST.get('delivery_type')
        did = request.session['did']
        delivery_boy = DeliveryBoy.objects.get(login_id=did)
        order = OrderMaster.objects.get(id=order)
    return render(request,"choose.html",{'orders':co})

def my_orders(request):
    ul= request.session['uid']
    hr=User.objects.get(login_id=ul)
    orders=OrderMaster.objects.filter(user_id=hr)
    od=orders.values_list('id',flat=True)
    k=OrderDetails.objects.filter(order_master_id__in=od)
    print(ul)
    return render(request,'my_orders.html',{'o':k})


def order_history(request):
    orders=OrderMaster.objects.all()
    return render(request,"order_history.html",{'orders':orders})

def add_rating(request,id):
    o=OrderDetails.objects.filter(order_master_id=id)
    return render(request, 'oud.html', {'o':o})

def rating(request,id):
    o=OrderDetails.objects.get(id=id)
    
    u=request.session['uid']
    z=User.objects.get(login_id=u)
    pid=o.product_id
    g=z.id
    if 'submit' in request.POST:
        a = request.POST['ratings']
        b = request.POST['review'] 
        ra = Rating(ratings=a,review=b,date=datetime.now(),product_id=pid,user_id=g)
        ra.save()
        return HttpResponse("<script>alert('Rating Added');window.location='/order_history'</script>")
    
    return render(request, 'addrating.html')


def send_complaint(request):
    c=Complaint.objects.all()
    if 'submit' in request.POST:
       a=request.POST['complaint']
       sc=Complaint(complaint=a,reply= 'pending',date_time = datetime.now(), user_id = request.session['uid'])
       sc.save()
       return HttpResponse("<script>alert('Complaint sent successfully');window.location='/send_complaint'</script>")
    return render(request, 'send_complaint.html',{'d':c})

def view_reply(request):
    complaints = Complaint.objects.all()
    return render(request,'view_reply.html', {'complaints': complaints})

def editt(request,id):
    ee=Type.objects.get(id=id)
    e=Type.objects.all()
    if 'edit' in request.POST:
        ee.type_name=request.POST['name']
        ee.save()
        return HttpResponse("<script>alert('updated!');window.location='/type'</script>")
    return render(request,"addequipment.html",{'n':ee ,'e':e})

def deletet(request,id):
    ee=Type.objects.get(id=id)
    ee.delete()
    return HttpResponse("<script>alert('type deleted');window.location='/type'</script>")

def verified(request,id):
    sid=request.session['sid']
    dh=Shop.objects.get(login_id=sid)
    o=OrderMaster.objects.filter(shop_id=dh.id,status='pending')
    o.status='Payment Verified'
    
    return HttpResponse("<script>alert('Payment Verified');window.location='/viewpayments'</script>")

def adb(request,id,o):
    s=SetToDeliver(delivery_boy_id=id, order_master_id =o, status='Assigned')
    o=OrderMaster.objects.get(id=o)
    o.status = 'Assigned-db'
    print(o.status)
    o.save()
    s.save()
    return HttpResponse("<script>alert('added');window.location='/vieworder'</script>")











def picke(request,id):
    pi=SetToDeliver.objects.get(id=id)
    pi.status = 'Picked'
    pi.save()
    return HttpResponse("<script>alert('picked');window.location='/orderass'</script>")


def deliveryed(request,id):
    di=SetToDeliver.objects.get(id=id)
    di.status = 'Delieverd'
    di.save()
    return HttpResponse("<script>alert('delievered');window.location='/deliveryhome'</script>") 

def userpay(request,id):
    up=OrderMaster.objects.get(id=id)
    if 'payment' in request.POST:
        up.status='Payment Done'
        up.save()
        m =Payment(amount=up.total,order_master_id=id,date=datetime.now(),status='pending')
        m.save()
        return HttpResponse("<script>alert('Payment done');window.location='/userhome'</script>")
    
    return render(request,"userpayment.html")

def logout1(request):
    return render(request,"home.html")
    
def logout2(request):
    return render(request,"home.html")
def logout3(request):
    return render(request,"home.html")
def logout4(request):
    return render(request,"home.html")

def rate(request):

    w=request.session['sid']
    d=Shop.objects.get(login_id=w)
    e=Product.objects.filter(shop_id=d)
    ge=e.values_list('id',flat=True)
    t=Rating.objects.filter(product_id__in=ge)
    return render(request,"rate1.html",{'t':t})