from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm  # Importa el formulario

def inicio(request):
    return render(request, 'principal/inicio.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(
                subject,
                f"De: {name} <{email}>\n\n{message}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.hdrdisweb@gmail.com],  # Reemplaza con tu dirección de correo
                fail_silently=False,
            )
            return redirect('contact_success')  # Redirige a una página de éxito
    else:
        form = ContactForm()

    return render(request, 'principal/seccion_contacto.html', {'form': form})

def contact_success(request):
    return render(request, 'principal/contact_success.html') # Crea esta plantilla