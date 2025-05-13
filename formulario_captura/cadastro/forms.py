from django import forms
from .models import Cliente, Condominio, Apartamento, Consultor, PreCliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cpf', 'nome', 'score','profissao', 'estcivil', 'rgrne', 'email', 'telefone', 
                  'endereco', 'data_nascimento', 'nomeresidente', 'cpfresidente', 'rgresidente', 
                  'Consultor', 'Condominio', 'Apartamento',
                  'cnpjunidade', 'matriculaunidade', 'vagaunidade',
                  'enderecounidade', 'nriptuunidade', 'vrunidade', 
                  'iniciocontrato', 'prazocontrato',
                  'observacoes'] #'__all__' #['imagem', 'nome', 'cpf', 'score', 'email', 'telefone', 'data_nascimento',  'unidade', 'apto', 'observacoes']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'iniciocontrato': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Deixa o campo Apartamento vazio inicialmente
            self.fields['Apartamento'].queryset = Apartamento.objects.none()
            # Adiciona classe JS para manipulação
            self.fields['Condominio'].widget.attrs.update({'class': 'condominio-select'})
            self.fields['Apartamento'].widget.attrs.update({'class': 'apartamento-select'})
            self.fields['Consultor'].widget.attrs.update({'class': 'consultor-select'})

class CondominioForm(forms.ModelForm):
    class Meta:
        model = Condominio
        fields = '__all__' 

class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamento
        fields = '__all__' 

class ConsultorForm(forms.ModelForm):
    class Meta:
        model = Consultor
        fields = '__all__'
        widgets = {
            'consultorDataInicio': forms.DateInput(attrs={'type': 'date'}),
        }

class PreClienteForm(forms.ModelForm):
    class Meta:
        model = PreCliente
        fields = '__all__'
        widgets = {
            'preclienteDataCadastro': forms.DateInput(attrs={'type': 'date'}),
            'preclienteJson': forms.Textarea(attrs={'rows': 10}),
        }