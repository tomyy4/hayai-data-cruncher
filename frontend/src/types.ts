export interface KPIValues {
  total_revenue: number;
  total_units_sold: number;
  average_ticket: number;
  total_transactions: number;
}

export interface MonthlyTrend {
  month: string;
  revenue: number;
  orders: number;
}

export interface TopProduct {
  id: number;
  name: string;
  sku: string;
  total_revenue: number;
  units_sold: number;
}

export interface DashboardResponse {
  source: 'database' | 'cache';
  time_ms?: number;
  data: {
    kpis: KPIValues;
    monthly_trends: MonthlyTrend[];
    top_products: TopProduct[];
  };
}