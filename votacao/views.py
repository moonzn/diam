from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from .models import Questao, Opcao


def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html', context)


def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {'questao': questao, 'error_message': "Não escolheu uma opção"})
    else:
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
    return HttpResponseRedirect(reverse('votacao:resultados', args=(questao.id,)))


def criar_questao(request):
    return render(request, 'votacao/criarquestao.html')


def gravar_questao(request):
    if request.POST['nova_questao']:
        texto_questao = request.POST['nova_questao']
        q = Questao(questao_texto=texto_questao, pub_data=timezone.now())
        q.save()
        return HttpResponseRedirect(reverse('votacao:index'))
    else:
        # Apresenta de novo o form para criar questão
        return render(request, 'votacao/criarquestao.html', {'error_message': "Não escreveu uma nova questão"})


def criar_opcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/criaropcao.html', {'questao': questao})


def gravar_opcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    if request.POST['nova_opcao']:
        texto_opcao = request.POST['nova_opcao']
        o = Opcao(opcao_texto=texto_opcao, votos=0, questao_id=questao_id)
        o.save()
        return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
    else:
        # Apresenta de novo o form para criar opção
        return render(request, 'votacao/criaropcao.html', {'questao': questao, 'error_message': "Não escreveu uma opção"})
