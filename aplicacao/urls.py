from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.home, name='cadastro'),
    path('inicial/', views.inicial, name='inicial'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cadastrarMotorista/', views.cadastrarMotorista, name='cadastrarMotorista'),
    path('visulizarMotorista', views.visualizarMotoristas, name='visualizarMotoristas'),
    path('buscar_motoristas/', views.buscar_motoristas, name='buscarMotoristas'),
    path('editarMotorista/<int:id>', views.editarMotorista, name='editarMotorista'),
    path('updateMotorista/<int:id>', views.updateMotorista, name='updateMotorista'),
    path('informarAbastecimento/', views.informarAbastecimento, name='informarAbastecimento'),
    path('visualizarAbastecimento', views.visualizarAbastecimento, name='visualizarAbastecimento'),
    path('buscarAbastecimento/', views.buscarAbastecimento, name='buscarAbastecimento'),
    path('editarAbastecimento/<int:id>', views.editarAbastecimento, name='editarAbastecimento'),
    path('updateAbastecimento/<int:id>', views.updateAbastecimento, name='updateAbastecimento'),
    path('cadastroManutencao/', views.cadastroManutencao, name='cadastroManutencao'),
    path('visualizarTipoManutencao', views.visualizarTipoManutencao, name='visualizarTipoManutencao'),
    path('buscarTipoManutencao/', views.buscarTipoManutencao, name='buscarTipoManutencao'),
    path('editarTipoManutencao/<int:id>', views.editarTipoManutencao, name='editarTipoManutencao'),
    path('updateTipoManutencao/<int:id>', views.updateTipoManutencao, name='updateTipoManutencao'),
    path('informarManutencao/', views.informarManutencao, name='informarManutencao'),
    path('visualizarManutencao', views.visualizarManutencao, name='visualizarManutencao'),
    path('buscarManutencao/', views.buscarManutencao, name='buscarManutencao'),
    path('editarManutencao/<int:id>', views.editarManutencao, name='editarManutencao'),
    path('updateManutencao/<int:id>', views.updateManutencao, name='updateManutencao'), 
    path('gerarRelatorio/', views.gerarRelatorio, name='gerarRelatorio'),
    path('acessarVeiculo/', views.acessarVeiculo, name='acessarVeiculo'),
    path('cadastroVeiculo/', views.cadastroVeiculo, name='cadastroVeiculo'),
    path('visualizarVeiculo', views.visualizarVeiculo, name='visualizarVeiculo'),
    path('buscarVeiculo/', views.buscarVeiculo, name='buscarVeiculo'),
    path('editarVeiculo/<int:id>', views.editarVeiculo, name='editarVeiculo'),
    path('updateVeiculo/<int:id>', views.updateVeiculo, name='updateVeiculo'),
    path('relatorio/', views.relatorioVeiculo, name='relatorio'),
    path('generate-pdf/', views.GeneratePDF.as_view(), name='generate_pdf'),
    path('teste/' , views.teste , name="teste")
    ]