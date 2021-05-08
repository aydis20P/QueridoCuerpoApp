from django.shortcuts import render

def principal(request):
    return render(request, 'queridocuerpo_pro/principal.html')

def resumen_usuario(request):
    return render(request, 'queridocuerpo_pro/index.html')

def perfil_profesional(request):
    return render(request, 'queridocuerpo_pro/perfil-profesional.html')

def perfil_miembro(request):
    return render(request, 'queridocuerpo_pro/perfil-miembro.html')

def plan_alimenticio_miembro(request):
    return render(request, 'queridocuerpo_pro/plan-alimenticio-miembro.html')

def resumen_usuario_administrativo(request):
    return render(request, 'queridocuerpo_pro/index-administrativo.html')
