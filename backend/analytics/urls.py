from django.urls import path
from analytics.views import GlobalDashboardAnalyticsView, hello_world

urlpatterns = [
    path("hello/", hello_world, name='hello_world'),
    path('dashboard/', GlobalDashboardAnalyticsView.as_view(), name='global-dashboard-analytics'),
]