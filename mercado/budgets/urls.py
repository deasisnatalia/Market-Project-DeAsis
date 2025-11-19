from django.urls import path
from . import views

app_name = 'budgets'

urlpatterns = [
    path('generar-presupuesto/', views.generate_budget_pdf, name='generar_presupuesto'),
    path('historial/', views.historial_presupuestos, name='historial_presupuestos'),
    path('descargar/<int:presupuesto_id>/', views.descargar_presupuesto, name='descargar_presupuesto'),
]