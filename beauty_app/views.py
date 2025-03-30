from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from .models import Appointment
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
import razorpay
import json
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm


# Create your views here.


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect logged-in users to home

    form = RegisterForm(request.POST or None)  
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            
            # ✅ NO SUCCESS MESSAGE ADDED TO PREVENT IT FROM SHOWING IN APPOINTMENTS
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please check the form.")

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect logged-in users to home

    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next', 'home')  # Get 'next' param (default: home)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect(next_url)  # ✅ Redirects to the intended page
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'login.html', {'form': form})
# User Logout View

def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def appointment(request):
    return render(request,'appointment.html')

def opening(request):
    return render(request,'opening.html')

def price(request):
    return render(request,'price.html')

def service(request):
    return render(request,'service.html')

def team(request):
    return render(request,'team.html')

def testimonial(request):
    return render(request,'testimonial.html')



from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from .models import Appointment

def book_appointment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        date = request.POST.get("date")  # Example: "03/11/2025"
        time_str = request.POST.get("time")  # Example: "3:45 PM"
        service = request.POST.get("service")

        # Check if date or time is missing
        if not date or not time_str:
            messages.error(request, "Date and time are required.")
            return redirect("book_appointment")

        try:
            # Convert date to YYYY-MM-DD format
            formatted_date = datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")

            # Convert time to 24-hour format (HH:MM:SS)
            formatted_time = datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M:%S")

            # Save appointment
            appointment = Appointment.objects.create(
                name=name, email=email, date=formatted_date, time=formatted_time, service=service
            )

            # Send email with cancel link
            cancel_url = request.build_absolute_uri(f"/cancel-appointment/{appointment.id}/")
            email_body = f"""
            Hi {name},

            Your appointment for {service} on {formatted_date} at {formatted_time} is confirmed.

            If you want to cancel, click below:
            {cancel_url}

            Regards,
            Your Team
            """
            send_mail(
                "Appointment Confirmation",
                email_body,
                "murugangv555@gmail.com",
                [email],
                fail_silently=False,
            )

            messages.success(request, "Appointment booked successfully!")
            return redirect("book_appointment")

        except ValueError as e:
            messages.error(request, f"Invalid date or time format: {str(e)}")
            return redirect("book_appointment")

    return render(request, "appointment.html")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login') 
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "Canceled"  # ✅ Just update status
    appointment.save()

    return render(request, "cancel_success.html")


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if name and email and subject and message:
            Contact.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, "Your message has been sent successfully!")
        else:
            messages.error(request, "Please fill all fields!")

    # Fetch all messages for displaying in a table
    messages_list = Contact.objects.all().order_by("-created_at")

    return render(request, "contact.html", {"messages_list": messages_list})







import razorpay
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Disable CSRF for debugging
from .models import Order
from django.conf import settings

@csrf_exempt  # Remove this once CSRF is properly handled
def create_order(request):
    try:
        if not request.user.is_authenticated:  # 🚨 Ensure the user is logged in
            return JsonResponse({"error": "User must be logged in to place an order"}, status=403)

        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method"}, status=400)

        plan = request.POST.get("plan", "Unknown Plan")
        amount = request.POST.get("amount")

        if not amount:
            return JsonResponse({"error": "Amount is required"}, status=400)

        try:
            amount = float(amount)
        except ValueError:
            return JsonResponse({"error": "Invalid amount"}, status=400)

        if amount < 10 or amount > 500000:
            return JsonResponse({"error": "Amount must be between ₹10 and ₹5,00,000"}, status=400)

        amount_in_paise = int(amount * 100)  # Convert ₹ to paise

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        razorpay_order = client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": "1"
        })

        # ✅ Ensure the user is correctly assigned
        order = Order.objects.create(
            user=request.user,  # Ensure the authenticated user is assigned
            plan=plan,
            amount=amount,
            razorpay_order_id=razorpay_order["id"],
            payment_status="Pending"
        )

        return JsonResponse({
            "order_id": razorpay_order["id"],
            "amount": amount_in_paise
        })

    except Exception as e:
        print("❌ Server Error:", str(e))  # Log in the terminal
        return JsonResponse({"error": str(e)}, status=500)


from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import razorpay
from django.conf import settings
from django.core.mail import send_mail
from .models import Order  # Ensure you import your Order model

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            data = request.POST
            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")

            if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
                return JsonResponse({"error": "Missing payment details"}, status=400)

            # Fetch the order
            try:
                order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            except Order.DoesNotExist:
                return JsonResponse({"error": "Order not found"}, status=404)

            # Verify Razorpay signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            }

            try:
                client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError:
                return JsonResponse({"error": "Payment verification failed"}, status=400)

            # ✅ Update Order
            order.payment_status = "Paid"
            order.save()

            # ✅ Store payment details in session
            request.session["payment_data"] = {
                "user": order.user.username if order.user else "Guest",
                "plan": order.plan,
                "amount": order.amount,
                "order_id": order.razorpay_order_id,
                "payment_id": razorpay_payment_id,
                "email": order.user.email if order.user else "Not Available",
            }

            # ✅ Send Email Confirmation to User
            subject = "Payment Successful"
            message = f"Dear {order.user.username},\n\nYour payment of ₹{order.amount} for {order.plan} was successful.\nOrder ID: {order.razorpay_order_id}\nPayment ID: {razorpay_payment_id}\n\nThank you for choosing us!"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email])

            # ✅ Send Admin Notification
            admin_email = getattr(settings, "ADMIN_EMAIL", "murugangv555@gmail.com")
            send_mail("New Payment Received", f"Payment of ₹{order.amount} received for {order.plan}.", settings.DEFAULT_FROM_EMAIL, [admin_email])

            return JsonResponse({"success": True})  # JavaScript will handle the redirection

        except Exception as e:
            print("❌ Error in payment_success:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == "GET":
        # ✅ Retrieve payment data from session
        payment_data = request.session.get("payment_data", {})

        if not payment_data:
            return render(request, "payment_failed.html")  # Show error page if no data

        return render(request, "payment_success.html", {"payment_data": payment_data})

    return JsonResponse({"error": "Invalid request"}, status=400)


from .models import Subscription  # Create this model if needed

@csrf_exempt
def subscribe(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"message": "Please enter a valid email.", "status": "error"})

            # ✅ Check if email is already subscribed
            if Subscription.objects.filter(email=email).exists():
                return JsonResponse({"message": "You are already subscribed!", "status": "error"})

            # ✅ Save email to database
            Subscription.objects.create(email=email)

            # ✅ Send Thank You Email
            subject = "Thank You for Subscribing!"
            message = f"Hello,\n\nThank you for subscribing to our newsletter! Stay tuned for updates.\n\nBest Regards,\nBeauty Team"
            send_mail(subject, message, "your_email@example.com", [email])

            return JsonResponse({"message": "Subscription successful! Check your email.", "status": "success"})

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({"message": "An error occurred.", "status": "error"})

    return JsonResponse({"message": "Invalid request.", "status": "error"})

def privacy(request):
    return render(request,'privacy.html')

def terms(request):
    return render(request,'terms.html')








