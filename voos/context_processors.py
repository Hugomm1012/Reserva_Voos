"""
context_processors.py
Adiciona variáveis globais a todos os templates sem precisar de as passar
manualmente em cada view. Registado em settings.py > TEMPLATES > context_processors.

is_gestor — True se o utilizador pertence ao grupo "gestor" OU é superuser.
            Usado nos templates para mostrar/esconder o link "Admin".
"""

def gestor_status(request):
    is_gestor = (
        request.user.is_authenticated and (
            request.user.is_superuser or
            request.user.groups.filter(name='gestor').exists()
        )
    )
    return {'is_gestor': is_gestor}
