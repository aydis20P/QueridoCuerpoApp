from django.shortcuts import render

def principal(request):
    return render(request, 'queridocuerpo_pro/principal.html')

def resumen_usuario(request):
    return render (request, 'queridocuerpo_pro/index.html')
