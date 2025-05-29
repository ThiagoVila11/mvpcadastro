from django import forms
from .models import Cliente, Condominio, Apartamento, Consultor, PreCliente

class ClienteForm(forms.ModelForm):
    isencaomulta = forms.BooleanField(
        required=False,
        label="Isenção de multa",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    class Meta:
        model = Cliente
        fields = ['cpf', 'nome', 'score','profissao', 'estcivil', 'rgrne', 'email', 'telefone', 
                  'endereco', 'data_nascimento', 'nomeresidente', 'cpfresidente', 'rgresidente', 
                  'enderecoresidente', 'profissaoresidente', 'estadocivilresidente', 'celularresidente',
                  'emailresidente', 
                  'Consultor', 'Condominio', 'apto',
                  'cnpjunidade', 'matriculaunidade', 'vagaunidade',
                  'enderecounidade', 'nriptuunidade', 'vrunidade', 
                  'iniciocontrato', 'prazocontrato', 'isencaomulta','percentualdesconto', 
                  'datainiciodesconto', 'dataterminodesconto', 
                  'observacoes', 'imagem'] #'__all__' #['imagem', 'nome', 'cpf', 'score', 'email', 'telefone', 'data_nascimento',  'unidade', 'apto', 'observacoes']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'iniciocontrato': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
            'datainiciodesconto': forms.DateInput(attrs={'type': 'date'}),
            'dataterminodesconto': forms.DateInput(attrs={'type': 'date'}),
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Campos que não devem ser editáveis
        campos_nao_editaveis = ['preclienteNome', 'precoclienteEmail', 'preclienteRendaFamiliar', 'preclienteRendaPresumida',
                                'preclienteScore', 'preclienteApontamentos', 'Consultor']

        for campo in campos_nao_editaveis:
            if campo in self.fields:
                #self.fields[campo].readonly = True
                self.fields[campo].widget.attrs['readonly'] = True  # Opcional: adiciona readonly também
                self.fields[campo].widget.attrs['class'] = 'form-control bg-light'  # Estilo visual

    class Meta:
        model = PreCliente
        fields = '__all__'
        widgets = {
            'preclienteDataCadastro': forms.DateInput(attrs={'type': 'date'}),
            'preclienteJson': forms.Textarea(attrs={'rows': 10}),
            'preclienteDataVisita': forms.DateInput(attrs={'type': 'date'}),
        }