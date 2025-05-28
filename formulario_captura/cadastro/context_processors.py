from .models import Notificacao

def notificacoes_nao_lidas(request):
    if request.user.is_authenticated:
        count = Notificacao.objects.filter(NotificacaoLido=False).count()
    else:
        count = 0
    return {'notificacoes_nao_lidas': count}
