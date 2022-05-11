from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from auction.view.main import bot


urlpatterns = [
    path('bot', bot,name="bot"),
    path('',home,name="home"),
    path('user_home',bidderHome,name="user_home"),
    # path('trainer_home',auctionUser,name="trainer_home"),
    path('login_user',loginUser,name="login_user"),
    path('contact',contact,name="conRtact"),
    path('about',about,name="about"),
    path('contact',contact,name="contact"),
    path('edit_profile',editProfile,name="edit_profile"),
    path('edit_profile1',editProfile1,name="edit_profile1"),
    path('logout', logout, name="logout"),
    path('login_admin',loginAdmin,name="login_admin"),
    path('signup', signupUser,name="signup"),
    path('change_password',changePassword,name="change_password"),
    path('change_password1',changePassword1,name="change_password1"),
    path('admin_home', adminHome,name="admin_home"),
    path('feedback', feedback,name="feedback"),
    path('add_product', addProduct,name="add_product"),
    path('new_product', newProduct,name="new_product"),
    path('bidder_user', bidderUser,name="bidder_user"),
    path('view_popup', viewPopup,name="view_popup"),
    path('seller_user', sellerUser,name="seller_user"),
    path('all_product2', allProduct2,name="all_product2"),
    path('profile', profile, name='profile'),
    path('result', result, name='result'),
    path('view_auction(<int:pid>)', viewAuction, name='view_auction'),
    path('particpated_user(<int:pid>)', participatedUser, name='particpated_user'),
    path('google_pay(<int:pid>)', googlePay, name='google_pay'),
    path('payment2(<int:pid>)', creditCard, name='payment2'),
    path('profile1', profile1, name='profile1'),
    path('status(<int:pid>)', changeStatus, name='status'),
    path('winner(<int:pid>)', winner,name='winner'),
    path('winner2(<int:pid>)', winner2,name='winner2'),
    path('winner1(<int:pid>)', winner1,name='winner1'),
    path('start_auction(<int:pid>)', startAuction, name='start_auction'),
    path('view_category', viewCategory, name='view_category'),
    path('view_feedback', viewFeedback, name='view_feedback'),
    path('view_subcategory', viewSubcategory, name='view_subcategory'),
    path('view_session_date', viewSessionDate, name='view_session_date'),
    path('view_session_time', viewSessionTime, name='view_session_time'),
    path('add_category', addCategory, name='add_category'),
    path('memberCreditCard', memberCreditCard, name='memberCreditCard'),
    path('memberGooglePay', memberGooglePay, name='memberGooglePay'),
    path('memberPaymentMode', memberPaymentMode, name='memberPaymentMode'),
    path('Payment_mode(<int:pid>)', paymentMode, name='Payment_mode'),
    path('add_subcategory', addSubCategory, name='add_subcategory'),
    path('add_session_date', addSessionDate, name='add_session_date'),
    path('add_session_time', addSessionTime, name='add_session_time'),
    path('bidding_status', biddingStatus, name='bidding_status'),
    path('bidding_status2', biddingStatus2, name='bidding_status2'),
    path('all_product', allProduct, name='all_product'),
    path('edit_category(<int:pid>)', editCategory, name='edit_category'),
    path('product_detail(<int:pid>)', productDetail, name='product_detail'),
    path('edit_subcategory(<int:pid>)', editSubCategory, name='edit_subcategory'),
    path('edit_session_date(<int:pid>)', editSessionDate, name='edit_session_date'),
    path('edit_session_time(<int:pid>)', editSessionTime, name='edit_session_time'),
    path('delete_category(<int:pid>)', deleteCategory, name='delete_category'),
    path('delete_feedback(<int:pid>)', deleteFeedback, name='delete_feedback'),
    path('delete_subcategory(<int:pid>)', deleteSubcategory, name='delete_subcategory'),
    path('delete_session_date(<int:pid>)', deleteSessionDate, name='delete_session_date'),
    path('delete_session_time(<int:pid>)', deleteSessionTime, name='delete_session_time'),
    path('load-courses/', loadCourses, name='ajax_load_courses'),
    path('load-courses1/', loadCourses1, name='ajax_load_courses1'),
    path('product_detail2(<int:pid>)', productDetail2, name='product_detail2'),    
    path("productView/<int:myid>",productView, name="ProductViews"),
    path("prod/<int:myid>",productView, name="ProductView"),
]
