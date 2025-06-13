from rest_framework import serializers
from .models import Consultor, Cliente, Notificacao

class ConsultorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultor
        fields = ['id', 'consultorNome', 'consultorEmail']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'cpf', 'email', 'Condominio', 'apto', 'score', 'Consultor', 
                  'processoassinaturaid', 'enderecowebhook']  
        
class ClienteCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        
class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = '__all__' 