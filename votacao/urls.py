from django.urls import include, path
from django.contrib import admin
from . import views
# (. significa que importa views da mesma directoria)

app_name = 'votacao'
urlpatterns = [
 # ex: votacao/
 path("", views.index, name='index'),
 # ex: votacao/1
 path('<int:questao_id>', views.detalhe, name='detalhe'),
 # ex: votacao/3/resultados
 path('<int:questao_id>/resultados', views.resultados, name='resultados'),
 # ex: votacao/5/voto
 path('<int:questao_id>/voto', views.voto, name='voto'),
 # ex: votacao/criarquestao
 path('criarquestao', views.criar_questao, name='criar_questao'),
 # votacao/criarquestao/gravarquestao
 path('gravarquestao', views.gravar_questao, name='gravar_questao'),
 # votacao/7/criaropcao
 path('<int:questao_id>/criaropcao', views.criar_opcao, name='criar_opcao'),
 # votacao/5/criaropcao/gravaropcao
 path('<int:questao_id>/gravaropcao', views.gravar_opcao, name='gravar_opcao')
]
