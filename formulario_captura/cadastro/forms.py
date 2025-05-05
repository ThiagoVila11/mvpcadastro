from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cpf', 'nome', 'score','profissao', 'estcivil', 'rgrne', 'email', 'telefone', 
                  'endereco', 'data_nascimento', 'nomeresidente', 'cpfresidente', 'rgresidente', 
                  'unidade', 'apto', 'nomeunidade', 'cnpjunidade', 'matriculaunidade', 'vagaunidade',
                  'enderecounidade', 'nriptuunidade', 'vrunidade', 'iniciocontrato', 'prazocontrato',
                  'terminocontrato', 'observacoes'] #'__all__' #['imagem', 'nome', 'cpf', 'score', 'email', 'telefone', 'data_nascimento',  'unidade', 'apto', 'observacoes']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
