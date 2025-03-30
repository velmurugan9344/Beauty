from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Canceled", "Canceled"),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    service = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Scheduled")  # ✅ New field

    def __str__(self):
        return f"{self.name} - {self.service} ({self.status})"



class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),  # Default before payment is completed
        ("Paid", "Paid"),        # After successful payment
        ("Cancelled", "Cancelled"),  # Admin can mark as cancelled
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ❌ No NULL users allowed
    plan = models.CharField(max_length=100)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan} ({self.payment_status})"


class Subscription(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email