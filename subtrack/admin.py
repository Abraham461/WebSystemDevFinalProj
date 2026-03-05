from django.contrib import admin

from .models import Category, Notification, Subscription, SubscriptionUsage

admin.site.register(Category)
admin.site.register(Subscription)
admin.site.register(Notification)
admin.site.register(SubscriptionUsage)
