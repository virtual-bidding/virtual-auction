from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MemberFee(models.Model):
    fee = models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.fee

class Bidder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=100,null=True)
    contact = models.CharField(max_length=10,null=True)
    image = models.FileField(null=True)
    membership = models.ForeignKey(MemberFee,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.user.username

class AuctionUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=100,null=True)
    contact = models.CharField(max_length=10,null=True)
    image = models.FileField(null=True)
    membership = models.ForeignKey(MemberFee,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name+" "+self.category.name

class SessionDate(models.Model):
    date = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.date


class SessionTime(models.Model):
    date = models.ForeignKey(SessionDate,on_delete=models.CASCADE,null=True)
    time = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.date.date+" "+self.time

class Status(models.Model):
    status = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.status

class Product(models.Model):
    product_id = models.AutoField
    temp = models.IntegerField(null=True)
    status  =models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,null=True)
    min_price = models.IntegerField(null=True)
    image = models.FileField(null=True)
    session = models.ForeignKey(SessionTime,on_delete=models.CASCADE,null=True)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    def __str__(self):
        return self.name

class Prod(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images",default="")

    # def __str__(self):
    #     return self.product_name

class AuctedProduct(models.Model):
    winner = models.CharField(max_length=100,null=True)
    user = models.ForeignKey(AuctionUser,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.user.username+ " " + self.product.name

class Result(models.Model):
    result = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.result

class Payment(models.Model):
    pay = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.pay

class Participant(models.Model):
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,null=True)
    new_price = models.IntegerField(null=True)
    result = models.ForeignKey(Result,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Bidder,on_delete=models.CASCADE,null=True)
    aucted_product = models.ForeignKey(AuctedProduct,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)

class Feedback(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message1 = models.TextField(null=True)
    date = models.CharField(max_length=30, null=True)
    def __str__(self):
        return self.profile.username



class Student1(models.Model):   
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images",default="")

    # def __str__(self):
    #     return self.product_name