from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count, F
from django.db.models.functions import TruncMonth
from analytics.models import OrderLine, Product
from rest_framework import status
from django.core.cache import cache


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello world"})




class GlobalDashboardAnalyticsView(APIView):
    def get(self, request):
        store_id = request.query_params.get('store_id') or "global"
        
        cache_key = f"dashboard_analytics_{store_id}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(
                {"source": "cache", "data": cached_data}, 
                status=status.HTTP_200_OK
            )

        # --- Cache Miss, execute heavy computation ] ---
        
        queryset = OrderLine.objects.all()
        if store_id != "global":
            queryset = queryset.filter(product__store_id=store_id)
        
        queryset = queryset.select_related('product')

        # KPIs
        kpis = queryset.annotate(
            line_total=F('quantity') * F('price_at_purchase')
        ).aggregate(
            total_revenue=Sum('line_total'),
            total_units_sold=Sum('quantity'),
            average_ticket=Avg('line_total'),
            total_orders=Count('id')
        )

        # Monthly sales block
        monthly_sales = (
            queryset.annotate(
                month=TruncMonth('purchased_at'),
                line_total=F('quantity') * F('price_at_purchase')
            )
            .values('month')
            .annotate(revenue=Sum('line_total'), orders=Count('id'))
            .order_by('month')
        )

        # Top Products
        db_product_filter = Product.objects.all() if store_id == "global" else Product.objects.filter(store_id=store_id)
        top_products = db_product_filter.annotate(
            total_generated=Sum(F('order_lines__quantity') * F('order_lines__price_at_purchase')),
            units_sold=Sum('order_lines__quantity')
        ).order_by('-total_generated')[:5]

        analytics_payload = {
            "kpis": {
                "total_revenue": round(kpis["total_revenue"] or 0, 2),
                "total_units_sold": kpis["total_units_sold"] or 0,
                "average_ticket": round(kpis["average_ticket"] or 0, 2),
                "total_transactions": kpis["total_orders"] or 0
            },
            "monthly_trends": [
                {
                    "month": item["month"].strftime("%Y-%m"),
                    "revenue": round(item["revenue"] or 0, 2),
                    "orders": item["orders"]
                }
                for item in monthly_sales if item["month"] is not None
            ],
            "top_products": [
                {
                    "id": prod.id,
                    "name": prod.name,
                    "sku": prod.sku,
                    "total_revenue": round(prod.total_generated or 0, 2),
                    "units_sold": prod.units_sold or 0
                }
                for prod in top_products
            ]
        }

        # 4. Store in redis: 15 minutes payload
        cache.set(cache_key, analytics_payload, timeout=900)

        return Response(
            {"source": "database", "data": analytics_payload}, 
            status=status.HTTP_200_OK
        )