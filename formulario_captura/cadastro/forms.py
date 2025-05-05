from django import forms
from .models import Cliente, Condominio, Apartamento

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cpf', 'nome', 'score','profissao', 'estcivil', 'rgrne', 'email', 'telefone', 
                  'endereco', 'data_nascimento', 'nomeresidente', 'cpfresidente', 'rgresidente', 
                  'Condominio', 'Apartamento',
                  'cnpjunidade', 'matriculaunidade', 'vagaunidade',
                  'enderecounidade', 'nriptuunidade', 'vrunidade', 
                  'iniciocontrato', 'prazocontrato',
                  'terminocontrato', 'observacoes'] #'__all__' #['imagem', 'nome', 'cpf', 'score', 'email', 'telefone', 'data_nascimento',  'unidade', 'apto', 'observacoes']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Deixa o campo Apartamento vazio inicialmente
            self.fields['Apartamento'].queryset = Apartamento.objects.none()
            # Adiciona classe JS para manipulação
            self.fields['Condominio'].widget.attrs.update({'class': 'condominio-select'})
            self.fields['Apartamento'].widget.attrs.update({'class': 'apartamento-select'})

class CondominioForm(forms.ModelForm):
    class Meta:
        model = Condominio
        fields = '__all__' 

class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamento
        fields = '__all__' 