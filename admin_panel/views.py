from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from users.models import User
from providers.models import Provider, ProviderApplication
from bookings.models import Booking
from services.models import Service
from services.forms import ServiceForm


# =====================================================
# 🔐 ADMIN CHECK
# =====================================================
def is_admin(user):

    return user.is_authenticated and (
        user.is_superuser or user.role == 'admin'
    )


# =====================================================
# 🚫 NOT AUTHORIZED
# =====================================================
def not_authorized(request):

    return render(
        request,
        'admin_panel/not_authorized.html',
        {
            'message': "Access Denied 🚫",
            'reason': "You do not have admin privileges."
        }
    )


# =====================================================
# 📊 ADMIN DASHBOARD
# =====================================================
@login_required
def admin_dashboard(request):

    if not is_admin(request.user):

        return not_authorized(request)

    # =========================================
    # MAIN COUNTS
    # =========================================
    total_users = User.objects.count()

    total_providers = Provider.objects.count()

    total_bookings = Booking.objects.count()

    pending_providers = ProviderApplication.objects.filter(
        status='pending'
    ).count()

    # =========================================
    # COMPLETED BOOKINGS
    # =========================================
    completed_jobs = Booking.objects.filter(
        status='completed'
    ).count()

    # =========================================
    # ACTIVE PROVIDERS
    # =========================================
    active_providers = Provider.objects.filter(
        user__is_active=True
    ).count()

    # =========================================
    # TOTAL REVENUE
    # =========================================
    successful_payments = Booking.objects.filter(
        payment_status='success'
    ).count()

    total_revenue = successful_payments * 500

    # =========================================
    # WEEKLY ANALYTICS
    # =========================================
    today = timezone.now().date()

    labels = []
    booking_data = []

    for i in range(6, -1, -1):

        day = today - timedelta(days=i)

        count = Booking.objects.filter(
            created_at__date=day
        ).count()

        labels.append(day.strftime('%a'))

        booking_data.append(count)

    # =========================================
    # RECENT BOOKINGS
    # =========================================
    recent_bookings = Booking.objects.select_related(
        'user',
        'service'
    ).order_by('-created_at')[:5]

    # =========================================
    # CONTEXT
    # =========================================
    context = {

        # COUNTS
        'total_users': total_users,
        'total_providers': total_providers,
        'total_bookings': total_bookings,
        'pending_providers': pending_providers,

        # ANALYTICS
        'completed_jobs': completed_jobs,
        'active_providers': active_providers,
        'total_revenue': total_revenue,

        # CHART
        'chart_labels': labels,
        'chart_data': booking_data,

        # RECENT
        'recent_bookings': recent_bookings,
    }

    return render(
        request,
        'admin_panel/dashboard.html',
        context
    )


# =====================================================
# 📋 PROVIDER REQUESTS
# =====================================================
@login_required
def provider_requests(request):

    if not is_admin(request.user):

        return not_authorized(request)

    applications = ProviderApplication.objects.all().order_by(
        '-created_at'
    )

    # SEARCH
    search_query = request.GET.get('q')

    if search_query:

        applications = applications.filter(

            Q(user__username__icontains=search_query) |

            Q(user__email__icontains=search_query)
        )

    # FILTER
    status = request.GET.get('status')

    if status in ['pending', 'approved', 'rejected']:

        applications = applications.filter(
            status=status
        )

    return render(
        request,
        'admin_panel/provider_requests.html',
        {
            'applications': applications,
            'search_query': search_query,
            'status': status
        }
    )


# =====================================================
# ✅ APPROVE PROVIDER
# =====================================================
@login_required
def approve_provider(request, id):

    if not is_admin(request.user):

        return not_authorized(request)

    application = get_object_or_404(
        ProviderApplication,
        id=id
    )

    if application.status == 'approved':

        messages.warning(
            request,
            "Already approved."
        )

        return redirect('provider_requests')

    application.status = 'approved'

    application.save()

    provider, created = Provider.objects.get_or_create(
        user=application.user
    )

    provider.services.set(
        application.services.all()
    )

    messages.success(
        request,
        f"✅ {application.user.username} approved"
    )

    return redirect('provider_requests')


# =====================================================
# ❌ REJECT PROVIDER
# =====================================================
@login_required
def reject_provider(request, id):

    if not is_admin(request.user):

        return not_authorized(request)

    application = get_object_or_404(
        ProviderApplication,
        id=id
    )

    if application.status == 'rejected':

        messages.warning(
            request,
            "Already rejected."
        )

        return redirect('provider_requests')

    application.status = 'rejected'

    application.save()

    messages.error(
        request,
        f"❌ {application.user.username} rejected"
    )

    return redirect('provider_requests')


# =====================================================
# 👤 MANAGE USERS
# =====================================================
@login_required
def manage_users(request):

    if not is_admin(request.user):

        return not_authorized(request)

    users = User.objects.all().order_by('-id')

    query = request.GET.get('q')

    if query:

        users = users.filter(

            Q(username__icontains=query) |

            Q(email__icontains=query)
        )

    return render(
        request,
        'admin_panel/users.html',
        {
            'users': users
        }
    )


# =====================================================
# 🔄 TOGGLE USER
# =====================================================
@login_required
def toggle_user(request, id):

    if not is_admin(request.user):

        return not_authorized(request)

    user = get_object_or_404(
        User,
        id=id
    )

    if user == request.user:

        messages.warning(
            request,
            "⚠️ You cannot block yourself."
        )

        return redirect('manage_users')

    user.is_active = not user.is_active

    user.save()

    messages.success(
        request,
        "User status updated ✅"
    )

    return redirect('manage_users')


# =====================================================
# ❌ DELETE USER
# =====================================================
@login_required
def delete_user(request, id):

    if not is_admin(request.user):

        return not_authorized(request)

    user = get_object_or_404(
        User,
        id=id
    )

    if user == request.user:

        messages.error(
            request,
            "❌ Cannot delete yourself."
        )

        return redirect('manage_users')

    user.delete()

    messages.error(
        request,
        "User deleted ❌"
    )

    return redirect('manage_users')


# =====================================================
# 👨‍🔧 MANAGE PROVIDERS
# =====================================================
@login_required
def manage_providers(request):

    if not is_admin(request.user):

        return not_authorized(request)

    providers = Provider.objects.select_related(
        'user'
    ).all().order_by('-rating')

    query = request.GET.get('q')

    if query:

        providers = providers.filter(

            Q(user__username__icontains=query) |

            Q(user__email__icontains=query)
        )

    return render(
        request,
        'admin_panel/providers.html',
        {
            'providers': providers
        }
    )


# =====================================================
# 🔄 TOGGLE PROVIDER
# =====================================================
@login_required
def toggle_provider(request, id):

    if not is_admin(request.user):

        return not_authorized(request)

    provider = get_object_or_404(
        Provider,
        id=id
    )

    provider.user.is_active = not provider.user.is_active

    provider.user.save()

    messages.success(
        request,
        "Provider status updated ✅"
    )

    return redirect('manage_providers')


# =====================================================
# ❌ DELETE PROVIDER
# =====================================================
@login_required
def delete_provider(request, id):

    if not is_admin(request.user):

        return not_authorized(request)

    provider = get_object_or_404(
        Provider,
        id=id
    )

    provider.user.delete()

    provider.delete()

    messages.error(
        request,
        "Provider deleted ❌"
    )

    return redirect('manage_providers')


# =====================================================
# ⭐ PROVIDER REVIEWS
# =====================================================
@login_required
def provider_reviews(request, id):

    if not is_admin(request.user):

        return not_authorized(request)

    provider = get_object_or_404(
        Provider,
        id=id
    )

    reviews = Booking.objects.filter(

        provider=provider,

        rating__isnull=False

    ).order_by('-created_at')

    return render(

        request,

        'admin_panel/provider_reviews.html',

        {
            'provider': provider,
            'reviews': reviews
        }
    )


# =====================================================
# 🛠 MANAGE SERVICES
# =====================================================
@login_required
def manage_services(request):

    if not is_admin(request.user):

        return not_authorized(request)

    services = Service.objects.all()

    return render(
        request,
        'admin_panel/services.html',
        {
            'services': services
        }
    )


# =====================================================
# ➕ ADD SERVICE
# =====================================================
@login_required
def add_service(request):

    if not is_admin(request.user):

        return not_authorized(request)

    if request.method == 'POST':

        form = ServiceForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "✅ Service added successfully!"
            )

            return redirect('manage_services')

        else:

            messages.error(
                request,
                "⚠️ Please fix the errors below."
            )

    else:

        form = ServiceForm()

    return render(
        request,
        'admin_panel/add_service.html',
        {
            'form': form
        }
    )


# =====================================================
# ❌ DELETE SERVICE
# =====================================================
@login_required
def delete_service(request, id):

    if not is_admin(request.user):

        return not_authorized(request)

    service = get_object_or_404(
        Service,
        id=id
    )

    service.delete()

    messages.error(
        request,
        "Service deleted ❌"
    )

    return redirect('manage_services')