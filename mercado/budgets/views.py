from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Budget
from products.models import Cart, Order
import io
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

@login_required
def generate_budget_pdf(request):
    if request.method == 'POST':
        user = request.user
        
        try:
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.all()
        except Cart.DoesNotExist:
            cart_items = []
        
        if not cart_items:
            return JsonResponse({"error": "El carrito esta vacio"}, status=400)

        productos = []
        total = 0

        for item in cart_items:
            subtotal = float(item.product.price) * item.quantity
            productos.append({
                'nombre': item.product.name,
                'cantidad': item.quantity,
                'precio_unitario': float(item.product.price),
                'subtotal': subtotal
            })
            total += subtotal

        # Generar PDF en memoria
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        p.setFont("Helvetica", 12)

        #Titulo
        p.drawString(50, height - 50, "Presupuesto - Michi Mercado")
        p.drawString(50, height - 70, f"Cliente: {user.get_full_name() or user.username}")
        p.drawString(50, height - 90, f"Fecha: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
        p.line(50, height - 100, width - 50, height - 100)  # Línea divisoria

        # Encabezados
        p.drawString(50, height - 120, "Producto")
        p.drawString(250, height - 120, "Cant.")
        p.drawString(300, height - 120, "Precio")
        p.drawString(400, height - 120, "Subtotal")

        y = height - 140
        for prod in productos:
            p.drawString(50, y, prod['nombre'])
            p.drawString(250, y, str(prod['cantidad']))
            p.drawString(300, y, f"${prod['precio_unitario']:.2f}")
            p.drawString(400, y, f"${prod['subtotal']:.2f}")
            y -= 20
            if y < 150: 
                p.showPage()
                y = height - 50

        p.drawString(400, y - 20, f"Total: ${total:.2f}")
        p.showPage()
        p.save()

        buffer.seek(0)
        os.makedirs("budgets/pdfs/", exist_ok=True)
        file_name = f"Presupuesto_{user.id}_{int(buffer.tell())}.pdf"
        file_path = f"budgets/pdfs/{file_name}"

        with open(file_path, 'wb') as f:
            f.write(buffer.read())

        # Guardar en base de datos
        Budget.objects.create(
            user=user,
            file_name=file_name,
            file_path=file_path,
            total=total
        )

        buffer.seek(0)
        try:
            enviar_pdf_por_correo(user.email, buffer)
        except Exception as e:
            print(f"Error al enviar correo: {e}")
        # Devolver PDF para descarga
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

def enviar_pdf_por_correo(destinatario, archivo_pdf):
    msg = MIMEMultipart()
    msg['Subject'] = "Tu presupuesto generado"
    msg['From'] = 'tuapp@gmail.com'
    msg['To'] = destinatario

    adjunto = MIMEBase('application', 'octet-stream')
    adjunto.set_payload(archivo_pdf.read())
    encoders.encode_base64(adjunto)
    adjunto.add_header(
        'Content-Disposition',
        f'attachment; filename="presupuesto.pdf"'
    )
    msg.attach(adjunto)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('deasisnatalia@gmail.com', 'gtth qpbi gzvi wkau')
    server.send_message(msg)
    server.quit()

@login_required
def historial_presupuestos(request):
    user = request.user
    # Presupuestos
    presupuestos = Budget.objects.filter(user=user).order_by('-created_at')
    # Compras
    compras = Order.objects.filter(user=user).order_by('-created_at')
    # Ventas
    ventas = Order.objects.filter(items__product__user=user).distinct().order_by('-created_at')
    
    paginator_p = Paginator(presupuestos, 5)
    paginator_c = Paginator(compras, 5)
    paginator_v = Paginator(ventas, 5)

    page_p = request.GET.get('page_p')
    page_c = request.GET.get('page_c')
    page_v = request.GET.get('page_v')

    page_obj_p = paginator_p.get_page(page_p)
    page_obj_c = paginator_c.get_page(page_c)
    page_obj_v = paginator_v.get_page(page_v)

    return render(request, 'budgets/historial.html', {
        'page_obj_p': page_obj_p,
        'page_obj_c': page_obj_c,
        'page_obj_v': page_obj_v,
    })

@login_required
def descargar_presupuesto(request, presupuesto_id):
    presupuesto = get_object_or_404(Budget, id=presupuesto_id, user=request.user)

    file_path = presupuesto.file_path
    if not os.path.exists(file_path):
        raise Http404("Archivo no encontrado")

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{presupuesto.file_name}"'
        return response