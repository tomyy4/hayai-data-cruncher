import { useEffect, useState } from 'react';
import { type DashboardResponse } from './types';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { DollarSign, ShoppingBag, Receipt, Activity, RefreshCw } from 'lucide-react';

function App() {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [storeId, setStoreId] = useState<string>(''); //Multitenand filter
  const [fetchTime, setFetchTime] = useState<number>(0);

  const fetchData = async () => {
    setLoading(true);
    const startTime = performance.now(); // Cronometer
    
    try {
      const url = storeId 
        ? `http://127.0.0.1:8000/api/dashboard/?store_id=${storeId}`
        : 'http://127.0.0.1:8000/api/dashboard/';
        
      const response = await fetch(url);
      const json: DashboardResponse = await response.json();
      
      const endTime = performance.now();
      setFetchTime(Math.round(endTime - startTime));
      setData(json);
    } catch (error) {
      console.error("Error fetching analytics:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [storeId]);

  if (loading || !data) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-slate-50">
        <div className="text-center">
          <RefreshCw className="mx-auto h-10 w-10 animate-spin text-indigo-600" />
          <p className="mt-4 text-slate-600 font-medium">Procesando métricas masivas...</p>
        </div>
      </div>
    );
  }

  const { kpis, monthly_trends, top_products } = data.data;

  return (
    <div className="min-h-screen p-8 bg-slate-50">
      {/* HEADER */}
      <header className="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Hayai Data Cruncher ⚡</h1>
          <p className="text-slate-500 mt-1">Dashboard de Analítica Multi-tenant en Tiempo Real</p>
        </div>
        
        {/* Filters and performance monitoring */}
        <div className="flex items-center gap-4 self-start md:self-center">
          <div className="bg-white px-4 py-2 rounded-lg shadow-sm border border-slate-200 text-sm">
            Velocidad API: <span className={`font-bold ${fetchTime < 15 ? 'text-green-600' : 'text-amber-500'}`}>{fetchTime}ms</span> 
            <span className="text-xs text-slate-400 ml-2">({data.source === 'cache' ? '⚡ Redis' : '🗄️ Postgres'})</span>
          </div>
          
          <select 
            value={storeId} 
            onChange={(e) => setStoreId(e.target.value)}
            className="rounded-lg border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm border focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">Todas las Tiendas (Global)</option>
            <option value="1">Tienda ID: 1</option>
            <option value="2">Tienda ID: 2</option>
            <option value="3">Tienda ID: 3</option>
          </select>
        </div>
      </header>

      {/* KPI CARDS */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">Ingresos Totales</p>
            <h3 className="text-2xl font-bold mt-1 text-slate-900">${kpis.total_revenue.toLocaleString()}</h3>
          </div>
          <div className="p-3 bg-indigo-50 rounded-lg text-indigo-600"><DollarSign className="h-6 w-6" /></div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">Unidades Vendidas</p>
            <h3 className="text-2xl font-bold mt-1 text-slate-900">{kpis.total_units_sold.toLocaleString()}</h3>
          </div>
          <div className="p-3 bg-emerald-50 rounded-lg text-emerald-600"><ShoppingBag className="h-6 w-6" /></div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">Ticket Medio</p>
            <h3 className="text-2xl font-bold mt-1 text-slate-900">${kpis.average_ticket}</h3>
          </div>
          <div className="p-3 bg-amber-50 rounded-lg text-amber-600"><Receipt className="h-6 w-6" /></div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">Transacciones</p>
            <h3 className="text-2xl font-bold mt-1 text-slate-900">{kpis.total_transactions.toLocaleString()}</h3>
          </div>
          <div className="p-3 bg-rose-50 rounded-lg text-rose-600"><Activity className="h-6 w-6" /></div>
        </div>
      </div>

<div className="grid gap-6 md:grid-cols-2 mt-8">  
  <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
    <div className="mb-4">
      <h3 className="text-lg font-bold text-slate-900">Tendencia de Ingresos Mensuales</h3>
      <p className="text-xs text-slate-400">Facturación acumulada del último año</p>
    </div>
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={monthly_trends} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis dataKey="month" stroke="#94a3b8" fontSize={11} tickLine={false} />
          <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} tickFormatter={(value) => `$${(value / 1000)}k`} />
          <Tooltip 
            formatter={(value: any) => [`$${Number(value).toLocaleString()}`, 'Ingresos']}
            contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', borderColor: '#e2e8f0', boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1)' }}
          />
          <Line type="monotone" dataKey="revenue" stroke="#4f46e5" strokeWidth={3} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  </div>

  <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
    <div className="mb-4">
      <h3 className="text-lg font-bold text-slate-900">Top 5 Productos más Vendidos</h3>
      <p className="text-xs text-slate-400">Rendimiento por ingresos generados</p>
    </div>
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={top_products} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis 
            dataKey="name" 
            stroke="#94a3b8" 
            fontSize={10} 
            tickLine={false}
            tickFormatter={(value) => value.length > 12 ? `${value.substring(0, 12)}...` : value} 
          />
          <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} tickFormatter={(value) => `$${value.toLocaleString()}`} />
          <Tooltip 
            formatter={(value: any) => [`$${Number(value).toLocaleString()}`, 'Ingresos Generados']}
            contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', borderColor: '#e2e8f0', boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1)' }}
          />
          <Bar dataKey="total_revenue" fill="#10b981" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      </div>
    </div>

</div>
    </div>
  );
}

export default App;