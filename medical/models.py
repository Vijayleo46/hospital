from django.db import models


class Login(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    user_type = models.CharField(max_length=50)

  
class Shop(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200)
    place = models.CharField(max_length=100)
    landmark = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    status = models.CharField(max_length=20)


class DeliveryBoy(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    house_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    place = models.CharField(max_length=100)
    email = models.EmailField()


class User(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    house_name = models.CharField(max_length=150)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    place = models.CharField(max_length=100)
    email = models.EmailField()

 
class Type(models.Model):
    type_name = models.CharField(max_length=100)

   
class Product(models.Model):
    type = models.OneToOneField(Type, on_delete=models.CASCADE)
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

class OrderMaster(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30)

class OrderDetails(models.Model):
    order_master = models.OneToOneField(OrderMaster, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()


class Payment(models.Model):
    order_master = models.OneToOneField(OrderMaster, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=30)

class SetToDeliver(models.Model):
    delivery_boy = models.OneToOneField(DeliveryBoy, on_delete=models.CASCADE)
    order_master = models.OneToOneField(OrderMaster, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)

class Delivery(models.Model):
    order_master = models.OneToOneField(OrderMaster, on_delete=models.CASCADE)
    boy = models.OneToOneField(DeliveryBoy, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    date_time = models.DateTimeField(auto_now_add=True)

class Complaint(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    complaint = models.TextField()
    reply = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_time = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField()
    review = models.TextField()
    date = models.DateField(auto_now_add=True)

class Chat(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    sender_type=models.CharField(max_length=100)
    receiver_type= models.CharField(max_length=100)