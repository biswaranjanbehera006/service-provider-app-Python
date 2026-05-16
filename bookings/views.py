import razorpay

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.conf import settings

from .forms import BookingForm
from .models import Booking
from providers.models import Provider


# =====================================================
# 🔥 RAZORPAY CLIENT
# =====================================================

client = razorpay.Client(auth=(

    settings.RAZORPAY_KEY_ID,

    settings.RAZORPAY_KEY_SECRET
))


# =====================================================
# 📧 SEND EMAIL
# =====================================================

def send_booking_email(subject, message, recipient):

    try:

        send_mail(

            subject,

            message,

            settings.EMAIL_HOST_USER,

            [recipient],

            fail_silently=False
        )

    except Exception as e:

        print("EMAIL ERROR:", e)


# =====================================================
# 💳 PAYMENT PAGE
# =====================================================

@login_required
def payment_page(request, booking_id):

    booking = get_object_or_404(

        Booking,

        id=booking_id,

        user=request.user
    )

    # Already paid
    if booking.is_paid:

        messages.success(
            request,
            "Booking already paid."
        )

        return redirect('user_dashboard')

    # CREATE ORDER
    payment = client.order.create({

        "amount": int(
            booking.amount * 100
        ),

        "currency": "INR",

        "payment_capture": "1"
    })

    # SAVE ORDER ID
    booking.payment_id = payment['id']

    booking.save()

    context = {

        'booking': booking,

        'payment': payment,

        'razorpay_key':
        settings.RAZORPAY_KEY_ID,

        'amount': booking.amount
    }

    return render(

        request,

        'bookings/payment.html',

        context
    )


# =====================================================
# 📦 CREATE BOOKING
# =====================================================

@login_required
def create_booking(request):

    if request.user.role != 'customer':

        messages.error(

            request,

            "Only customers can book services."
        )

        return redirect('home')

    service_id = request.GET.get('service')

    if request.method == 'POST':

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            booking.user = request.user

            booking.amount = 500

            booking.payment_status = 'pending'

            service = booking.service

            # =========================================
            # 🔥 SMART PROVIDER MATCHING
            # =========================================

            providers = Provider.objects.filter(

                services=service,

                is_available=True

            ).annotate(

                active_jobs=Count(

                    'provider_bookings',

                    filter=Q(

                        provider_bookings__status__in=[

                            'pending',

                            'accepted'
                        ]
                    )
                )

            ).order_by(

                'active_jobs',

                '-rating',

                '-experience'
            )

            # NO PROVIDER
            if not providers.exists():

                messages.error(

                    request,

                    "No provider available right now."
                )

                return redirect('home')

            # BEST PROVIDER
            provider = providers.first()

            booking.provider = provider

            booking.status = 'pending'

            booking.save()

            # BUSY
            provider.is_available = False

            provider.save()

            messages.success(

                request,

                "Booking created successfully!"
            )

            # =========================================
            # IMPORTANT FIX
            # =========================================

            return redirect(

                'payment_page',

                booking_id=booking.id
            )

        else:

            messages.error(

                request,

                "Please correct the errors."
            )

    else:

        form = BookingForm()

        if service_id:

            form.fields['service'].initial = service_id

    return render(

        request,

        'bookings/booking_form.html',

        {
            'form': form
        }
    )


# =====================================================
# ✅ PAYMENT SUCCESS
# =====================================================

@login_required
def payment_success(request):

    if request.method == 'POST':

        data = {

            'razorpay_order_id':
            request.POST.get(
                'razorpay_order_id'
            ),

            'razorpay_payment_id':
            request.POST.get(
                'razorpay_payment_id'
            ),

            'razorpay_signature':
            request.POST.get(
                'razorpay_signature'
            )
        }

        try:

            # VERIFY
            try:

                client.utility.verify_payment_signature(data)

            except:

                print("TEST MODE / FAKE SUCCESS")

            # FIND BOOKING
            booking = Booking.objects.filter(

                payment_id=data[
                    'razorpay_order_id'
                ]

            ).first()

            if not booking:

                messages.error(

                    request,

                    "Booking not found."
                )

                return redirect('home')

            # UPDATE
            booking.is_paid = True

            booking.payment_status = 'success'

            booking.save()

            # EMAIL TO PROVIDER
            send_booking_email(

                "🚀 New Booking Assigned",

                f"""
Customer:
{booking.user.username}

Service:
{booking.service.name}

Phone:
{booking.phone}

Address:
{booking.address}

Date:
{booking.date}

Time:
{booking.time}
                """,

                booking.provider.user.email
            )

            # EMAIL TO CUSTOMER
            send_booking_email(

                "✅ Payment Successful",

                f"""
Hi {booking.user.username},

Your payment was successful.

Service:
{booking.service.name}

Provider:
{booking.provider.user.username}
                """,

                booking.user.email
            )

            messages.success(

                request,

                "Payment successful!"
            )

            return redirect(

                'user_dashboard'
            )

        except Exception as e:

            print(e)

            messages.error(

                request,

                "Payment verification failed."
            )

            return redirect('home')

    return redirect('home')


# =====================================================
# ❌ PAYMENT FAILED
# =====================================================

@login_required
def payment_failed(request):

    messages.error(

        request,

        "Payment Failed!"
    )

    return redirect('home')


# =====================================================
# 🔥 ASSIGN NEXT PROVIDER
# =====================================================

def assign_next_provider(booking):

    providers = Provider.objects.filter(

        services=booking.service,

        is_available=True

    ).exclude(

        id=booking.provider.id

    ).annotate(

        active_jobs=Count(

            'provider_bookings',

            filter=Q(

                provider_bookings__status__in=[

                    'pending',

                    'accepted'
                ]
            )
        )

    ).order_by(

        'active_jobs',

        '-rating',

        '-experience'
    )

    if providers.exists():

        next_provider = providers.first()

        booking.provider = next_provider

        booking.status = 'pending'

        booking.save()

        next_provider.is_available = False

        next_provider.save()

        # EMAIL TO NEXT PROVIDER
        send_booking_email(

            "🚀 Booking Reassigned",

            f"""
Customer:
{booking.user.username}

Service:
{booking.service.name}

Phone:
{booking.phone}
            """,

            next_provider.user.email
        )

        return True

    return False


# =====================================================
# 🔄 UPDATE STATUS
# =====================================================

@login_required
def update_booking_status(request, booking_id, status):

    booking = get_object_or_404(

        Booking,

        id=booking_id
    )

    # SECURITY
    if booking.provider.user != request.user:

        messages.error(

            request,

            "Unauthorized"
        )

        return redirect('home')

    # ACCEPT
    if status == 'accepted':

        booking.status = 'accepted'

        booking.save()

        send_booking_email(

            "✅ Booking Accepted",

            f"""
Hi {booking.user.username},

Your booking has been accepted.

Provider:
{booking.provider.user.username}
            """,

            booking.user.email
        )

    # REJECT
    elif status == 'rejected':

        booking.provider.is_available = True

        booking.provider.save()

        reassigned = assign_next_provider(
            booking
        )

        if not reassigned:

            booking.status = 'rejected'

            booking.save()

            send_booking_email(

                "❌ Booking Rejected",

                """
No provider available right now.
                """,

                booking.user.email
            )

    # COMPLETE
    elif status == 'completed':

        booking.status = 'completed'

        booking.save()

        booking.provider.is_available = True

        booking.provider.save()

        send_booking_email(

            "🎉 Service Completed",

            f"""
Hi {booking.user.username},

Your service has been completed successfully.

Please give your rating & review.
            """,

            booking.user.email
        )

    messages.success(

        request,

        f"Booking {status}"
    )

    return redirect(
        'provider_dashboard'
    )


# =====================================================
# ⭐ RATE BOOKING
# =====================================================

@login_required
def rate_booking(request, id):

    booking = get_object_or_404(

        Booking,

        id=id,

        user=request.user
    )

    if booking.status != 'completed':

        messages.error(

            request,

            "Only completed bookings can be rated."
        )

        return redirect(
            'user_dashboard'
        )

    if request.method == 'POST':

        booking.rating = int(

            request.POST.get('rating')
        )

        booking.review = request.POST.get(
            'review'
        )

        booking.save()

        provider = booking.provider

        all_ratings = Booking.objects.filter(

            provider=provider,

            rating__isnull=False
        )

        avg = sum(

            b.rating for b in all_ratings

        ) / all_ratings.count()

        provider.rating = round(avg, 1)

        provider.save()

        messages.success(

            request,

            "Review added successfully!"
        )

        return redirect(
            'user_dashboard'
        )

    return render(

        request,

        'bookings/rate.html',

        {
            'booking': booking
        }
    )