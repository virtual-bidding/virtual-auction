from multiprocessing import context
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *
import datetime
from django.db.models import Avg, Max, Min, Sum
from math import ceil
from django.shortcuts import render
import random

# Create your views here.
def home(request):
    data = 0
    error = ""
    user=""
    try:
        user = User.objects.get(username=request.user.username)
    except:
        pass
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
            return redirect('profile1')
    except:
        pass
    try:
        data = AuctionUser.objects.get(user=user)
        return redirect('trainer_home')
    except:
        pass
    d = {'error':error,'data':data}
    
    return render(request, 'carousel.html',d)


def new():
    status = Status.objects.get(status="pending")
    new_pro = Product.objects.filter(status=status)
    return new_pro


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def loginUser(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user:
            try:
                sign = Bidder.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error = "pat"
            else:
                login(request, user)
                error = "pat1"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'login.html', d)


def loginAdmin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            error = "yes"
        else:
            error = "not"

    d = {'error': error}
    return render(request, 'loginadmin.html', d)

def signupUser(request):
    error = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        add = request.POST['add']
        d2 = request.POST['dob']
        reg = request.POST['reg']
        i = request.FILES['image']
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        mem = MemberFee.objects.get(fee="Unpaid")
        if reg == "Bidder":
            sign = Bidder.objects.create(membership=mem,user=user,contact=con,address=add,dob=d2,image=i)
        else:
            sign = AuctionUser.objects.create(membership=mem,user=user,contact=con,address=add,dob=d2,image=i)
        error = True
    d = {'error':error}
    return render(request,'signup.html',d)

def adminHome(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count=0
    if new2:
        count+=1
    all_p = 0
    all_b=0
    all_s = 0
    pro = Product.objects.all()
    bid = Bidder.objects.all()
    sel = AuctionUser.objects.all()
    for i in pro:
        all_p+=1
    for i in bid:
        all_b+=1
    for i in sel:
        all_s+=1
    data1  = User.objects.get(id=request.user.id)
    data = Bidder.objects.get(user=data1)
    d = {'data':data,'count':count,'new2':new2,'all_p':all_p,'all_b':all_b,'all_s':all_s}
    return render(request,'admin_home.html',d)

def bidderHome(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user=User.objects.get(username=request.user.username)
    error=""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    d = {'error':error,'data':data}
    return render(request,'dashboard.html',d)

def profile1(request):
    new2 = new()
    count = 0
    if new2:
        count += 1
    data = 0
    user=User.objects.get(username=request.user.username)
    error=""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    user = User.objects.get(id=request.user.id)
    u = ""
    try:
        pro = Bidder.objects.get(user=user)
        u = "member"
    except:
        pro = AuctionUser.objects.get(user=user)
        u = "trainer"
    d = {'pro':pro,'error':error,'data':data,'count':count,'new2':new2}
    return render(request,'profile1.html',d)

def auctionHome(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    sign = 0
    user = User.objects.get(username=request.user.username)
    error=""
    try:
        sign = Bidder.objects.get(user=user)
        if sign:
            error = "pat"
    except:
        sign = AuctionUser.objects.get(user=user)
    if sign.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    d = {'error': error,'data':sign}
    return render(request,'dashboard.html',d)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    sign = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        sign = Bidder.objects.get(user=user)
        if sign:
            error = "pat"
    except:
        sign = AuctionUser.objects.get(user=user)
    if sign.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    user = User.objects.get(id=request.user.id)
    u=""
    try:
        pro = Bidder.objects.get(user=user)
        u = "member"
    except:
        pro = AuctionUser.objects.get(user=user)
        u = "trainer"
    d = {'pro':pro,'error':error,"u":u,'data':sign}
    return render(request,'profile.html',d)

def logout(request):
    logout(request)
    return redirect('home')

def changePassword(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    sign = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        sign = Bidder.objects.get(user=user)
        if sign:
            error = "pat"
    except:
        sign = AuctionUser.objects.get(user=user)
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'error':error,'terror':terror,'data':sign,'count':count,'new2':new2}
    return render(request,'change_password.html',d)

def changePassword1(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    sign = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        sign = Bidder.objects.get(user=user)
        if sign:
            error = "pat"
    except:
        sign = AuctionUser.objects.get(user=user)
    if sign.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'error':error,'terror':terror,'data':sign,'count':count,'new2':new2}
    return render(request,'change_password1.html',d)

def editProfile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    terror = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            pro.image=i
            pro.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        pro.address = ad
        pro.contact=con
        user1.first_name = f
        user1.last_name = l
        user1.email = e
        user1.save()
        pro.save()
        terror = True
    d = {'terror':terror,'pro':pro,'data':pro,'count':count,'new2':new2}
    return render(request, 'edit_profile.html',d)

def editProfile1(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    if pro.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    terror = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            pro.image=i
            pro.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        pro.address = ad
        pro.contact=con
        user1.first_name = f
        user1.last_name = l
        user1.email = e
        user1.save()
        pro.save()
        terror = True
    d = {'terror':terror,'pro':pro,'data':pro,'count':count,'new2':new2}
    return render(request, 'edit_profile1.html',d)

def addCategory(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    if request.method == 'POST':
        n = request.POST['cat']
        Category.objects.create(name=n)
        error = True
    d = {'error':error,'pro':pro,'data':pro,'count':count,'new2':new2}
    return render(request, 'add_category.html',d)


def editCategory(request,pid):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    cat = Category.objects.get(id=pid)
    if request.method == 'POST':
        n = request.POST['cat']
        cat.name = n
        cat.save()
        error = True
    d = {'error':error,'pro':pro,'data':pro,'cat':cat,'count':count,'new2':new2}
    return render(request, 'edit_category.html',d)

def deleteCategory(request,pid):
    cat = Category.objects.get(id=pid)
    cat.delete()
    return redirect('view_category')


def viewCategory(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro = ""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error = "pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    cat = Category.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'cat':cat,'count':count,'new2':new2}
    return render(request,'view_category.html',d)

def viewFeedback(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro = ""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error = "pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    cat = Feedback.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'cat':cat,'count':count,'new2':new2}
    return render(request,'view_feedback.html',d)

def addSubCategory(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    cat = Category.objects.all()
    if request.method == 'POST':
        n = request.POST['cat']
        s = request.POST['scat']
        cat1 = Category.objects.get(name=n)
        SubCategory.objects.create(name=s,category=cat1)
        error = True
    d = {'error':error,'pro':pro,'data':pro,'cat':cat,'count':count,'new2':new2}
    return render(request, 'add_sub_category.html',d)


def editSubCategory(request,pid):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    cat = Category.objects.all()
    subcat = SubCategory.objects.get(id=pid)
    if request.method == 'POST':
        n = request.POST['cat']
        s = request.POST['scat']
        subcat.category = Category.objects.get(name=n)
        subcat.name = s
        subcat.save()
        error = True
    d = {'error':error,'pro':pro,'data':pro,'cat':cat,'subcat':subcat,'count':count,'new2':new2}
    return render(request, 'edit_subcategory.html',d)

def deleteSubcategory(request,pid):
    cat = SubCategory.objects.get(id=pid)
    cat.delete()
    return redirect('view_subcategory')

def deleteFeedback(request,pid):
    cat = Feedback.objects.get(id=pid)
    cat.delete()
    return redirect('view_feedback')


def viewSubcategory(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro = ""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error = "pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    cat = SubCategory.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'cat':cat,'count':count,'new2':new2}
    return render(request,'view_subcategory.html',d)


def addSessionDate(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    if request.method == 'POST':
        d = request.POST['date']
        cat1 = SessionDate.objects.create(date=d)
        error = True
    d = {'error':error,'pro':pro,'data':pro,'count':count,'new2':new2}
    return render(request, 'Add_session_date.html',d)


def editSessionDate(request,pid):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    ses = SessionDate.objects.get(id=pid)
    if request.method == 'POST':
        n = request.POST['date']
        ses.date = n
        ses.save()
        error = True
    d = {'error':error,'pro':pro,'data':pro,'ses':ses,'count':count,'new2':new2}
    return render(request, 'edit_session_date.html',d)

def deleteSessionDate(request,pid):
    cat = SessionDate.objects.get(id=pid)
    cat.delete()
    return redirect('view_session_date')


def viewSessionDate(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro = ""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error = "pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    cat = SessionDate.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'date1':cat,'count':count,'new2':new2}
    return render(request,'view_session_date.html',d)


def addSessionTime(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    sed = SessionDate.objects.all()
    if request.method == 'POST':
        d = request.POST['date']
        t = request.POST['time']
        d1 = SessionDate.objects.get(date=d)
        cat1 = SessionTime.objects.create(date=d1,time=t)
        error = True
    d = {'error':error,'pro':pro,'data':pro,'sed':sed,'count':count,'new2':new2}
    return render(request, 'add_session_time.html',d)

def newProduct(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    st = Status.objects.get(status = "pending")
    prod = Aucted_Product.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'prod':prod,'count':count,'new2':new2}
    return render(request, 'new_product.html',d)

def allProduct2(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    st = Status.objects.get(status = "pending")
    prod = Aucted_Product.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'prod':prod,'count':count,'new2':new2}
    return render(request, 'all_product2.html',d)


def bidderUser(request):
    if not request.user.is_staff:
        return redirect('login_user')
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    st = Status.objects.get(status = "pending")
    prod = Bidder.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'prod':prod}
    return render(request, 'new_user.html',d)

def sellerUser(request):
    if not request.user.is_staff:
        return redirect('login_user')
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    st = Status.objects.get(status = "pending")
    prod = AuctionUser.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'prod':prod}
    return render(request, 'auction_user.html',d)

def result(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = True
    pro1 = Participant.objects.all()
    d = {'error':error,'pro':pro1,'data':pro,'count':count,'new2':new2}
    return render(request, 'result.html',d)

def winner(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    error = ""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    pro1 = Participant.objects.get(id=pid)
    d = {'error':error,'pro':pro1,'data':pro,'count':count,'new2':new2}
    return render(request, 'winner_announced.html',d)

def winner2(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)

    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    pro2 = Product.objects.get(id=pid)
    au = Aucted_Product.objects.get(product=pro2)
    re = Result.objects.get(result="Winner")
    pro1 = Participant.objects.get(aucted_product=au, result=re)
    d = {'pro': pro1, 'error': error}
    return render(request, 'winner2.html', d)

def winner1(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    pro2 = Product.objects.get(id=pid)
    au = Aucted_Product.objects.get(product=pro2)
    re = Result.objects.get(result="Winner")
    pro1 = ""
    # print("hiii",pro1)
    try:
        pro1 = Participant.objects.get(aucted_product=au, result=re)
    except:
        pass
    terror = False
    if not pro1:
        terror=True
    d = {'pro':pro1,'error':error,'terror':terror}
    return render(request,'winner2.html',d)



def editSessionTime(request,pid):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    error = False
    sed = SessionDate.objects.all()
    sett = SessionTime.objects.get(id=pid)
    if request.method == 'POST':
        d = request.POST['date']
        t = request.POST['time']
        sedd = SessionDate.objects.get(id=d)
        sett.date = sedd
        sett.time = t
        sett.save()
        error = True
    d = {'error':error,'pro':pro,'data':pro,'sed':sed,'sett':sett,'count':count,'new2':new2}
    return render(request, 'edit_session_time.html',d)

def deleteSessionTime(request,pid):
    cat = SessionTime.objects.get(id=pid)
    cat.delete()
    return redirect('view_session_time')


def viewSessionTime(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro = ""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error = "pat"
    except:
        pro = AuctionUser.objects.get(user=user1)
    cat = SessionTime.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'time1':cat,'count':count,'new2':new2}
    return render(request,'view_session_time.html',d)


def feedback(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    date1 = datetime.date.today()
    user = User.objects.get(id=request.user.id)
    pro = ""
    try:
        pro = Bidder.objects.filter(user=user).first()
    except:
        pro = AuctionUser.objects.filter(user=user).first()
    terror = False
    if request.method == "POST":
        d = request.POST['date']
        u = request.POST['uname']
        e = request.POST['email']
        con = request.POST['contact']
        m = request.POST['desc']
        user = User.objects.filter(username=u, email=e).first()
        try:
            pro = Bidder.objects.filter(user=user, contact=con).first()
        except:
            pro = AuctionUser.objects.filter(user=user, contact=con).first()
        Feedback.objects.create(profile=user, date=d, message1=m)
        terror = True
    d = {'pro': pro, 'date1': date1,'terror':terror,'error':error}
    return render(request, 'feedback.html', d)


def addProduct(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    date1 = datetime.date.today()
    sed = SessionDate.objects.all()
    sett = SessionTime.objects.all()
    cat = Category.objects.all()
    scat = SubCategory.objects.all()
    sell = AuctionUser.objects.get(user=user)
    terror = False
    if request.method == "POST":
        c = request.POST['cat']
        s = request.POST['scat']
        p = request.POST['p_name']
        pr = request.POST['price']
        i = request.FILES['image']
        sett1 = request.POST['time']
        sed1 = request.POST['date']
        sub = SubCategory.objects.get(id=s)
        ses = SessionTime.objects.get(id=sett1)
        sta = Status.objects.get(status="pending")
        pro1=Product.objects.create(status=sta,session=ses,category=sub,name=p, min_price=pr, image=i)
        auc=Aucted_Product.objects.create(product=pro1,user=sell)
        terror = True
    d = {'sed': sed,'sett':sett,'cat': cat,'scat':scat,'date1': date1,'terror':terror,'error':error}
    return render(request, 'add_product.html', d)

def loadCourses(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    programming_id = request.GET.get('programming')
    # programming_id1 = request.GET.get('programming1')
    # print(programming_id,11111111111111111,programming_id1)
    courses = SubCategory.objects.filter(category_id=programming_id).order_by('name')
    # courses1 = SessionTime.objects.filter(date_id=programming_id1).order_by('name')
    return render(request, 'courses_dropdown_list_options.html', {'courses': courses})

def loadCourses1(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    programming_id = request.GET.get('programming')
    courses = SessionTime.objects.filter(date_id=programming_id)
    return render(request, 'courses_dropdown_list_options1.html', {'courses': courses})




def viewAuction(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    terror = False
    if request.method == "POST":
        pro1 = Product.objects.get(id=pid)
        auc = Aucted_Product.objects.get(product=pro1)
        Participant.objects.create(user=data,aucted_product=auc)
        terror = True
    pid = 0
    d1 = Participant.objects.filter(user=data)
    li = []
    for i in d1:
        li.append(i.aucted_product.product.id)

    status = Status.objects.get(status="Accept")
    pro = Product.objects.filter(status=status)
    pro1 = Product.objects.all()
    message1=""
    if not pro:
        message1 = " No Any Bidding Product "
    for i in pro:
        if i.id in li:
            i.temp = 1
            i.save()
        else:
            i.temp = 0
            i.save()
    for i in pro:
        a = i.session.date.date
        li = a.split('-')
        total_time = (int(li[0]) * 365) + (int(li[1]) * 30) + (int(li[2]))
        d1 = datetime.date.today()
        d2 = datetime.datetime.now()
        c_time = d2.strftime("%H:%M")
        y = d1.year
        m = d1.month
        d = d1.day
        now_total = (int(y) * 365) + (int(m) * 30) + (int(d))
        part = Participant.objects.all()
        for l in part:
            z=l.aucted_product.product.session.date.date
            li2 = z.split('-')
            total_time_part = (int(li2[0]) * 365) + (int(li2[1]) * 30) + (int(li2[2]))
            if total_time_part < now_total:
                if l.result is None:
                    r = Result.objects.get(result="notproper")
                    l.result = r
                    l.save()
        li2 = i.session.time.split(':')
        li3 = c_time.split(':')
        time1 = (int(li2[0]) * 60) + int(li2[1])
        time2 = (int(li3[0]) * 60) + int(li3[1])
        time3 = time1 + 60
        if total_time == now_total:
            if time1 == time2:
                i.temp = 2
                i.save()
            elif time2 < time3 and time2>time1:
                i.temp = 2
                i.save()
            elif time2 > time3:
                i.temp = 3
                i.save()
        elif total_time < now_total:

            i.temp = 3
            i.save()
    d = {'pro':pro1,'error':error,'terror':terror,'message1':message1}
    return render(request,'view_auction.html',d)

def allProduct(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)

    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    pro = Aucted_Product.objects.filter(user=data)
    d = {'pro':pro,'error':error}
    return render(request,'All_prodcut.html',d)

def productDetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    pro = Product.objects.get(id=pid)
    end = pro.session.time.split(':')
    end1=""
    if end[0]== "23":
        end1="00"
    else:
        end1 = str(int(end[0])+1)
    end2 = end1+":"+end[1]
    pro1 = Aucted_Product.objects.get(product=pro)
    d = {'pro':pro,'pro1':pro1,'error':error,'end2':end2}
    return render(request,'product_detail.html',d)

def productDetail2(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)

    pro = Product.objects.get(id=pid)
    end = pro.session.time.split(':')
    end1 = ""
    if end[0] == "23":
        end1 = "00"
    else:
        end1 = str(int(end[0]) + 1)
    end2 = end1 + ":" + end[1]
    pro1 = Aucted_Product.objects.get(product=pro)
    d = {'pro':pro,'pro1':pro1,'error':error,'data':data,'end2':end2}
    return render(request,'product_detail2.html',d)

def biddingStatus(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    pro = Participant.objects.filter(user=data)
    d = {'pro':pro,'error':error}
    return render(request,'bidding_status.html',d)

def biddingStatus2(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    pro1 =  Aucted_Product.objects.filter(user=data)
    d = {'pro':pro1,'error':error}
    return render(request,'bidding_status2.html',d)

def participatedUser(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')
    auc = Aucted_Product.objects.get(id=pid)
    pro1 =  Participant.objects.filter(aucted_product=auc)
    message1=""
    if not pro1:
        message1 = "No Bidder"
    d = {'part':pro1,'error':error,'message1':message1}
    return render(request,'particpated_user.html',d)

def paymentMode(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')

    d = {'error':error,'pid':pid}
    return render(request,'payment_mode.html',d)

def memberPaymentMode(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)

    d = {'error':error,'data':data}
    return render(request,'member_Payment.html',d)

def googlePay(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    total = Participant.objects.get(id=pid)
    terror=False
    if request.method=="POST":
        pay = Payment.objects.get(pay="paid")
        total.payment=pay
        total.save()
        terror=True
    d = {'error':error,'total':total,'terror':terror}
    return render(request,'google_pay.html',d)

def memberGooglePay(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    terror=False
    if request.method=="POST":
        mem = MemberFee.objects.get(fee="Paid")
        data.membership = mem
        data.save()
        terror=True
    d = {'error':error,'terror':terror}
    return render(request,'member_google_pay.html',d)

def creditCard(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    terror = False
    total = Participant.objects.get(id=pid)
    if request.method=="POST":
        pay = Payment.objects.get(pay="paid")
        total.payment=pay
        total.save()
        terror =True
    d = {'error':error,'total':total,'terror':terror}
    return render(request,'payment2.html',d)

def memberCreditCard(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    terror = False
    if request.method=="POST":
        mem = MemberFee.objects.get(fee="Paid")
        data.membership = mem
        data.save()
        terror =True
    d = {'error':error,'terror':terror}
    return render(request,'member_payment2.html',d)
def viewPopup(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error=True
    d = {'error':error}
    return render(request,'view_popup.html',d)

def startAuction(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('memberPaymentMode')

    pro4 = Product.objects.get(id=pid)
    end = pro4.session.time.split(':')
    end1 = ""
    if end[0] == "23":
        end1 = "00"
    else:
        end1 = str(int(end[0]) + 1)
    end2 = end1 + ":" + end[1]
    c = Aucted_Product.objects.get(product=pro4)
    pro1=""
    try:
        pro1 = Participant.objects.get(user=data, aucted_product=c)
    except:
        return redirect('view_popup')
    pro1 = Participant.objects.get(user=data, aucted_product=c)
    pro2 = Participant.objects.filter(aucted_product=c).order_by('-new_price')
    if request.method == "POST":
        p = request.POST["price"]
        pro1.new_price = p
        pro1.save()

    a = pro1.aucted_product.product.session.date.date
    li = a.split('-')
    total_time = (int(li[0]) * 365) + (int(li[1]) * 30) + (int(li[2]))
    d1 = datetime.date.today()
    d2 = datetime.datetime.now()
    c_time = d2.strftime("%H:%M")
    y = d1.year
    m = d1.month
    d = d1.day
    now_total = (int(y) * 365) + (int(m) * 30) + (int(d))
    li2 = pro1.aucted_product.product.session.time.split(':')
    li3 = c_time.split(':')
    time1 = (int(li2[0]) * 60) + int(li2[1])
    time2 = (int(li3[0]) * 60) + int(li3[1])
    time3 = time1 + 60
    terror = ""
    if total_time == now_total:
        if time1 == time2 or time2 < time3:
            pro1.aucted_product.product.temp = 2
            pro1.aucted_product.product.save()
        elif time2 > time3:
            pro1.aucted_product.product.temp = 3
            pro1.aucted_product.product.save()
            terror = "expire"
    elif total_time < now_total:
        pro1.aucted_product.product.temp = 3
        pro1.aucted_product.product.save()
        terror = "expire"
    win = Participant.objects.filter(aucted_product=c).order_by('-new_price')
    list1 = []
    for i in win:
        list1.append(i.id)
    win1 = Participant.objects.get(id=list1[0])
    if pro1.aucted_product.product.temp == 3:
        pro1.aucted_product.winner = win1.user.user.username
        pro1.aucted_product.save()
        for i in pro2:
            if i.user.user.username == pro1.aucted_product.winner:
                res = Result.objects.get(result="Winner")
                stat1 = Status.objects.get(status="Done")
                pay2 = Payment.objects.get(pay="pending")
                i.payment = pay2
                i.result = res
                i.aucted_product.product.status = stat1
                i.aucted_product.product.save()
                i.save()
            else:
                res1 = Result.objects.get(result="Defeat")
                pay1 = Payment.objects.get(pay="reject")
                i.payment = pay1
                i.result = res1
                i.save()


    d = {'pro':pro1,'pro2':pro2,'end2':end2,'error':error,'terror':terror}
    return render(request,'start_auction.html',d)

def changeStatus(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = AuctionUser.objects.get(user=user)
    terror = False
    pro1 = Product.objects.get(id=pid)
    if request.method == "POST":
        stat = request.POST['stat']
        sta = Status.objects.get(status=stat)
        pro1.status=sta
        pro1.save()
        terror=True
    d = {'pro':pro1,'error':error,'terror':terror,'data':data,'count':count,'new2':new2}
    return render(request,'status.html',d)

def winnerAnnounced(request):
    return redirect('result')


def productView(request, myid):
    prod = Prod.objects.filter(id=myid)
    print (prod)
    return render(request, 'carousel.html', {'prod': prod[0]})

# def home(request):
#     products = Product.objects.all()
#     print(products)
#     random.shuffle(products)
#     context={'products':products}
    
#     return render(request,"carousel.html",context)



def home(request): 
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        list_prod=list(prod)
        random.shuffle(list_prod)
        # print(list(prod))
        n = len(list_prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([list_prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, 'carousel.html', params)




def home1(request):
   
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, 'carousel.html', params)

