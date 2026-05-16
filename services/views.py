from django.shortcuts import render

from .models import Service, Category

from bookings.models import Booking

from users.models import User


# =========================
# 🚀 HOME PAGE
# =========================
def home(request):

    # 🔥 ALL ACTIVE SERVICES
    services = Service.objects.filter(
        is_active=True
    )

    # 📂 ALL CATEGORIES
    categories = Category.objects.all()

    # 🔍 SEARCH QUERY
    query = request.GET.get('q')

    # 📂 CATEGORY FILTER
    category_id = request.GET.get('category')

    # 🔍 SEARCH FILTER
    if query:

        services = services.filter(
            name__icontains=query
        )

    # 📂 CATEGORY FILTER
    if category_id:

        services = services.filter(
            category_id=category_id
        )

    # =========================
    # 📊 DYNAMIC STATISTICS
    # =========================

    total_services = Service.objects.count()

    total_bookings = Booking.objects.count()

    total_providers = User.objects.filter(
        role='provider'
    ).count()

    total_customers = User.objects.filter(
        role='customer'
    ).count()

    # =========================
    # 🚀 CONTEXT
    # =========================

    context = {

        'services': services,

        'categories': categories,

        'total_services': total_services,

        'total_bookings': total_bookings,

        'total_providers': total_providers,

        'total_customers': total_customers,

    }

    # =========================
    # 🚀 RENDER PAGE
    # =========================

    return render(
        request,
        'services/home.html',
        context
    )





from .models import Service


def services_page(request):

    services = Service.objects.all()

    context = {

        'services': services
    }

    return render(
        request,
        'services/services.html',
        context
    )




def about_page(request):

    context = {

        'total_customers': 1200,

        'total_providers': 150,

        'total_services': 40,

        'total_bookings': 5000,
    }

    return render(
        request,
        'services/about.html',
        context
    )


def contact_page(request):

    return render(
        request,
        'services/contact.html'
    )