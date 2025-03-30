from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import book_appointment, cancel_appointment,contact_view
from .views import create_order, payment_success,subscribe
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('appointment', views.appointment, name='appointment'),
    path('contact', views.contact, name='contact'),
    path('opening', views.opening, name='opening'),
    path('price', views.price, name='price'),
    path('service', views.service, name='service'),
    path('team', views.team, name='team'),
    path('testimonial', views.testimonial, name='testimonial'),

    path("book-appointment/", book_appointment, name="book_appointment"),
    path("cancel-appointment/<int:appointment_id>/", cancel_appointment, name="cancel_appointment"),

    path("contact/", contact_view, name="contact"),


    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('create-order/', create_order, name='create_order'),
    path('payment-success/', payment_success, name='payment_success'),

    path("subscribe/", subscribe, name="subscribe"),

    #Privacy and Terms
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),
    
    
]