from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, SignUpForm, SubscriptionForm, UsageForm
from .models import Notification, Subscription


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard(request):
    subscriptions = request.user.subscriptions.filter(is_active=True).select_related('category')
    monthly_total = sum((s.monthly_cost_equivalent() for s in subscriptions), Decimal('0.00'))
    annual_projection = (monthly_total * Decimal('12')).quantize(Decimal('0.01'))
    five_year_projection = (annual_projection * Decimal('5')).quantize(Decimal('0.01'))

    today = date.today()
    upcoming = subscriptions.filter(billing_date__gte=today).order_by('billing_date')[:5]
    trials = subscriptions.filter(status=Subscription.STATUS_TRIAL).exclude(trial_end_date=None).order_by('trial_end_date')[:5]

    month_start = today.replace(day=1)
    wasted_qs = request.user.subscriptions.filter(usage_entries__month=month_start, usage_entries__used=False)
    wasted_spend = wasted_qs.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    context = {
        'subscriptions': subscriptions,
        'monthly_total': monthly_total,
        'annual_projection': annual_projection,
        'five_year_projection': five_year_projection,
        'upcoming': upcoming,
        'trials': trials,
        'wasted_spend': wasted_spend,
    }
    return render(request, 'subscriptions/dashboard.html', context)


@login_required
def subscription_list(request):
    cycle = request.GET.get('cycle')
    category = request.GET.get('category')
    subs = request.user.subscriptions.select_related('category')
    if cycle:
        subs = subs.filter(billing_cycle=cycle)
    if category:
        subs = subs.filter(category_id=category)
    return render(
        request,
        'subscriptions/subscription_list.html',
        {'subscriptions': subs, 'categories': request.user.categories.all()},
    )


@login_required
def subscription_create(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        form.fields['category'].queryset = request.user.categories.all()
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            messages.success(request, 'Subscription added successfully.')
            return redirect('subscription_list')
    else:
        form = SubscriptionForm()
        form.fields['category'].queryset = request.user.categories.all()
    return render(request, 'subscriptions/subscription_form.html', {'form': form, 'title': 'Add Subscription'})


@login_required
def subscription_update(request, pk):
    sub = get_object_or_404(Subscription, pk=pk)
    if sub.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=sub)
        form.fields['category'].queryset = request.user.categories.all()
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription updated.')
            return redirect('subscription_list')
    else:
        form = SubscriptionForm(instance=sub)
        form.fields['category'].queryset = request.user.categories.all()
    return render(request, 'subscriptions/subscription_form.html', {'form': form, 'title': 'Edit Subscription'})


@login_required
def subscription_delete(request, pk):
    sub = get_object_or_404(Subscription, pk=pk)
    if sub.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        sub.delete()
        messages.success(request, 'Subscription deleted.')
        return redirect('subscription_list')
    return render(request, 'subscriptions/subscription_delete.html', {'subscription': sub})


@login_required
def category_list(request):
    return render(request, 'subscriptions/category_list.html', {'categories': request.user.categories.all()})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'subscriptions/category_form.html', {'form': form})


@login_required
def analytics(request):
    subscriptions = request.user.subscriptions.filter(is_active=True)
    labels = [sub.service_name for sub in subscriptions]
    amounts = [float(sub.amount) for sub in subscriptions]
    return render(request, 'subscriptions/analytics.html', {'labels': labels, 'amounts': amounts})


@login_required
def usage_entry(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        form = UsageForm(request.POST)
        if form.is_valid():
            usage = form.save(commit=False)
            usage.subscription = subscription
            usage.month = usage.month.replace(day=1)
            usage.save()
            messages.success(request, 'Usage entry recorded.')
            return redirect('dashboard')
    else:
        form = UsageForm(initial={'month': date.today().replace(day=1), 'used': True})
    return render(request, 'subscriptions/usage_form.html', {'form': form, 'subscription': subscription})


@login_required
def run_reminders(request):
    due_subscriptions = [s for s in request.user.subscriptions.filter(is_active=True) if s.is_due_for_reminder()]
    for subscription in due_subscriptions:
        message = (
            f'Reminder: {subscription.service_name} will renew on '
            f'{subscription.billing_date:%Y-%m-%d} for ${subscription.amount}.'
        )
        send_mail(
            subject='SubTrack Billing Reminder',
            message=message,
            from_email='no-reply@subtrack.local',
            recipient_list=[request.user.email or 'user@example.com'],
            fail_silently=True,
        )
        Notification.objects.create(subscription=subscription, message=message)

    messages.success(request, f'{len(due_subscriptions)} reminder(s) processed.')
    return redirect('dashboard')
