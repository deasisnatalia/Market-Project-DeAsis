from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages

from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Usuario {user.username} creado exitosamente!")
            return redirect('products:home')  # Asegúrate de que este nombre de URL exista
        else:
            # Mostrar errores para depurar
            messages.error(request, "Errores en el formulario. Revisa los datos ingresados.")
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {' '.join(errors)}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        if '__all__' in form.errors:
            del form.errors['__all__']
        form.add_error(None, "Usuario o contraseña incorrectos. Asegúrate de que ambos campos sean correctos.")
        return self.render_to_response(self.get_context_data(form=form))