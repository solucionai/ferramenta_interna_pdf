from django.shortcuts import render, redirect
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.views.decorators.csrf import csrf_protect

def render_page(request, page):
    template_name = f'{page}.html'
    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        raise Http404(f'Template {template_name} does not exist')

@csrf_protect
def process_form(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        celular = request.POST.get('celular')
        problema = request.POST.get('problema')
        print(nome)
        return redirect('home')
    return redirect('home')
