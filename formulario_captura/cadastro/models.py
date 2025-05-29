from django.db import models
from django.core.validators import EmailValidator
import json
from datetime import datetime


class Condominio(models.Model):

    condominionome = models.CharField(verbose_name="Nome do Condominio",  max_length=100, blank=True)
    condominionomecomercial = models.CharField(verbose_name="Nome Comercial do Condominio",  max_length=100, null=True, blank=True)
    condominionomepropriedade = models.CharField(verbose_name="Nome da Propriedade",  max_length=100, null=True, blank=True)
    condominiocnpj = models.CharField(verbose_name="CNPJ", max_length=20, null=True, default='')
    condominiomatricula = models.CharField(verbose_name="IPTU", max_length=30, null=True, default='')
    condominioendereco = models.CharField(verbose_name="Endereço", max_length=120, null=True, default='')

    def __str__(self):
        return self.condominionome
    
class Consultor(models.Model):
    AtivoInativoConsultor = (
        ('A', 'Ativo(a)'),
        ('I', 'Inativo(a)')
    )
    consultorNome = models.CharField(verbose_name='Nome', max_length=120, blank=True)
    consultorEmail = models.EmailField(verbose_name="E-mail",
                                    max_length=255,
                                    unique=True,  # Opcional: para garantir emails únicos
                                    validators=[EmailValidator(message="Digite um e-mail válido")],
                                    help_text="Exemplo: usuario@provedor.com")
    consultorTelefone = models.CharField(verbose_name='Telefone', null=True, blank=True)
    consultorDataInicio = models.DateField(verbose_name='Data de Início', null=True, blank=True)
    consultorAtivoInativo = models.CharField(verbose_name='Ativo/Inativo', max_length=1,choices=AtivoInativoConsultor, null=True, default='A')

    def __str__(self):
        return self.consultorNome

class Apartamento(models.Model):
    vaga = (
        ('0', 'Nenhuma'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    )

    Condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE)
    apartamentonro = models.CharField(verbose_name="Apto", null=True, blank=True)
    apartamentovagas =  models.CharField(verbose_name="Vaga(s)", max_length=1, choices=vaga, null=True, default='0')
    apartamentoiptu = models.CharField(verbose_name="Número IPTU", max_length=20, null=True, default='')
    apartamentovrunidade = models.DecimalField(verbose_name="Valor", max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return self.apartamentonro
    
class PreCliente(models.Model):
    AvaliacaoAutomatica = (('A', 'Apto'),('N', 'Não Apto'))

    preclienteNome = models.CharField(verbose_name="Nome",  max_length=100,null=True, blank=True)
    preclienteCpf = models.CharField(verbose_name="CPF", max_length=14, unique=True)
    precoclienteEmail = models.EmailField(verbose_name="E-mail",
                                    max_length=255,
                                    unique=True,  # Opcional: para garantir emails únicos
                                    validators=[EmailValidator(message="Digite um e-mail válido")],
                                    help_text="Exemplo: usuario@provedor.com",
                                    null=True, blank=True)
    preclienteDataCadastro = models.DateTimeField(verbose_name="Data de cadastro", auto_now_add=True)
    preclienteScore = models.CharField(verbose_name='Score', null=True, blank=True, default='0')
    preclienteApontamentos = models.CharField(verbose_name='Apontamentos', null=True, blank=True)
    preclienteRendaPresumida = models.DecimalField(verbose_name="Renda Presumida", max_digits=10, decimal_places=2, null=True, blank=True)
    preclienteRendaFamiliar = models.DecimalField(verbose_name="Renda Familiar", max_digits=10, decimal_places=2, null=True, blank=True)
    preclienteAvalAuto = models.CharField(verbose_name='Avaliação Automática', max_length=1, null=True, blank=True)
    preclienteAvaliacao = models.CharField(verbose_name='Avaliação', max_length=1, null=True, blank=True)
    preclienteJson = models.TextField(verbose_name='Json', null=True, blank=True)
    preclienteDataVisita = models.DateField(verbose_name="Data da visita", null=True, blank=True)
    preclienteCondominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, verbose_name='Condominio', null=True, blank=True)
    Consultor = models.ForeignKey(Consultor, on_delete=models.CASCADE, verbose_name='Consultor', null=True, blank=True)

    def pode_ser_convertido(self):
        aprovado = 'N'
        score = int(self.preclienteScore) if self.preclienteScore else 0
        obs = len(self.preclienteApontamentos) if self.preclienteApontamentos else 0
        if score >= 700 and obs == 0:
            aprovado = 'A'

        return aprovado == 'A'  # Só converte se estiver aprovado
    
    def converter_para_cliente(self, consultor=None, condominio=None, apartamento=None):
        if not self.pode_ser_convertido():
            raise ValueError("Pré-cliente não está aprovado para conversão")
        
        nome = self.preclienteNome
        preclienteJson = json.loads(self.preclienteJson)
        dataISO = preclienteJson['Data']['BirthDate']
        # Converter para objeto date
        data_convertida = datetime.strptime(dataISO, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        primeiroEndereco = preclienteJson['Data']['Addresses'][0]
        print(primeiroEndereco)
        endereco = primeiroEndereco['Alias'] #street + ', ' +  ' - ' +  ' - ' + ' - ' + city + ' - ' + state
        phones = preclienteJson.get('Data', {}).get('Phones', [])
        if isinstance(phones, list) and len(phones) > 0:
            nrfone = phones[0]["FormattedNumber"]
            # Aqui você pode acessar phone_0 com segurança
            print(nrfone)
        else:
            print("Nenhum telefone encontrado")
            nrfone = ''
        
        cliente = Cliente(
            nome=nome,
            cpf=self.preclienteCpf,
            email=self.precoclienteEmail,
            score=self.preclienteScore,
            PreCliente=self,
            telefone = nrfone,
            endereco = endereco,
            data_nascimento = data_convertida,
            Condominio = self.preclienteCondominio,
            Consultor = self.Consultor 
        )
        
        cliente.save()
        return cliente

    def __str__(self):
        return self.preclienteNome
    
    
class Cliente(models.Model):
    unidades = (
        ("VMD", "Vila Madalena"), 
        ("BEL", "Bela Vista"), 
        ("PAR", "Paraiso"),
        ("VMR", "Vila Mariana"),
        ("FRE", "Frei Caneca"),
        ("PIN", "Pinheiros"), 
        ("ITU", "Alameda Itu"),
        ("CAP", "Capote Valente"),
        ("MEL", "Melo Alves"),
    )
    estadocivil = (
        ('Solteiro(a)', 'Solteiro(a)'),
        ('Casado(a)', 'Casado(a)'),
        ('Divorciado(a)', 'Divorciado(a)'),
        ('Viúvo(a)', 'Viúvo(a)'),
        ('Separado(a) judicialmente', 'Separado(a) judicialmente')
    )
    vaga = (
        ('0', 'Nenhuma'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    )

    nome = models.CharField(verbose_name="Nome",  max_length=100)
    cpf = models.CharField(verbose_name="CPF", max_length=14)
    profissao = models.CharField(verbose_name="Profissão", max_length=40, null=True, default='')
    estcivil = models.CharField(verbose_name="Estado Civil", max_length=30, choices=estadocivil, null=True, default='Solteiro(a)')
    rgrne = models.CharField(verbose_name="RG/RNE", max_length=20, null=True, default='')
    email = models.EmailField(verbose_name="Email", null=True, default='')
    telefone = models.CharField(verbose_name="Celular", max_length=20, null=True, default='', blank=True)
    endereco = models.CharField(verbose_name="Endereço", max_length=120, null=True, default='')
    data_nascimento = models.DateField(verbose_name="Data de nascimento", null=True, blank=True)
    observacoes = models.TextField(verbose_name="Observações", blank=True)
    data_cadastro = models.DateTimeField(verbose_name="Data de cadastro", auto_now_add=True)
    nomeresidente = models.CharField(verbose_name="Nome do residente", max_length=100, null=True, default='', blank=True)
    cpfresidente = models.CharField(verbose_name="CPF do residente", max_length=14, null=True, default='', blank=True)
    rgresidente = models.CharField(verbose_name="RG do residente", max_length=20, null=True, default='', blank=True)
    enderecoresidente = models.CharField(verbose_name="Endereço do residente", max_length=120, null=True, blank=True)
    profissaoresidente = models.CharField(verbose_name="Profissão do residente", max_length=30, null=True, blank=True)
    estadocivilresidente = models.CharField(verbose_name="Estado civil do residente", max_length=30, choices=estadocivil, null=True, default='Solteiro(a)')
    celularresidente = models.CharField(verbose_name='Celular residente', max_length=20, null=True, blank=True)
    emailresidente = models.EmailField(verbose_name="E-mail do residente",
                                    max_length=255,
                                    unique=True,  # Opcional: para garantir emails únicos
                                    validators=[EmailValidator(message="Digite um e-mail válido")],
                                    help_text="Exemplo: usuario@provedor.com",
                                    null=True,
                                    blank=True)
    score = models.CharField(verbose_name="Score", max_length=5, null=True, default="0", blank=True)
    unidade = models.CharField(verbose_name="Unidade", max_length=3, choices=unidades, null=True, default='BEL')
    apto = models.CharField(verbose_name="Apto", max_length=4, default=0)
    nomeunidade = models.CharField(verbose_name="Nome do condomínio", max_length=50, null=True, default='', blank=True)
    cnpjunidade = models.CharField(verbose_name="CNPJ condomínio", max_length=14, null=True, default='', blank=True)
    matriculaunidade = models.CharField(verbose_name="Número da matrícula", max_length=30, null=True, default='', blank=True)
    vagaunidade = models.CharField(verbose_name="Vaga(s)", max_length=1, choices=vaga, null=True, default='0', blank=True)
    enderecounidade = models.CharField(verbose_name="Endereço da unidade", max_length=120, null=True, default='', blank=True)
    nriptuunidade = models.CharField(verbose_name="Número IPTU", max_length=20, null=True, default='', blank=True)
    vrunidade = models.DecimalField(verbose_name="Valor", max_digits=10, decimal_places=2, null=True, blank=True)
    prazocontrato = models.IntegerField(verbose_name="Prazo do Contrato", null=True, default=0, blank=True)
    iniciocontrato = models.DateField(verbose_name="Início do contrato", null=True, blank=True)
    terminocontrato = models.DateField(verbose_name="Término do contrato", null=True, blank=True)
    imagem = models.ImageField(verbose_name="Imagem CNH", upload_to='imagens/', default=None, null=True, blank=True)
    visitarealizada = models.BooleanField(verbose_name="Visita realizado", default=False, null=True)
    documentacaoenviada = models.FileField(verbose_name="Pré-Contrato", default=None, null=True)
    Condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, null=True, blank=True)
    Apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE, null=True, blank=True)
    Consultor = models.ForeignKey(Consultor, on_delete=models.CASCADE, null=True, blank=True)
    PreCliente = models.ForeignKey(PreCliente, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    percentualdesconto = models.DecimalField(verbose_name='Percentual de desconto', max_digits=8, decimal_places=4,
                                           null=True, blank=True)
    datainiciodesconto = models.DateField(verbose_name="Data de início do desconto", null=True, blank=True)
    dataterminodesconto = models.DateField(verbose_name="Data de término do desconto", null=True, blank=True)
    isencaomulta = models.BooleanField(verbose_name='Isenção de contrato',  default=False, null=True, blank=True)
    processoassinaturaid = models.IntegerField(verbose_name='ID do processo de assinatura', null=True, blank=True)
    enderecowebhook = models.TextField(verbose_name='Endereço Webhook', max_length=255, null=True, blank=True)
    documentacaoassinada = models.BooleanField(verbose_name='Documentação assinada', default=False, null=True, blank=True)  
    datahoraassinatura = models.DateTimeField(verbose_name='Data e hora da assinatura', null=True, blank=True)
    statusassinatura = models.CharField(verbose_name='Status da assinatura', max_length=30, null=True, blank=True, default='Pendente')  

    def __str__(self):
        return self.nome

    
class Notificacao(models.Model):
    TipoNotificacao = (
        ('A', 'Alerta'),
        ('I', 'Informação'),
        ('E', 'Erro')
    )   

    NotificacaoTitulo = models.CharField(verbose_name='Título', max_length=100, null=True, blank=True)
    NotificacaoDescricao = models.CharField(verbose_name='Descrição', max_length=300, null=True, blank=True)
    NotificacaoData = models.DateTimeField(verbose_name='Data', auto_now_add=True)
    NotificacaoTipo = models.CharField(verbose_name='Tipo', max_length=1, choices=TipoNotificacao, null=True, blank=True)
    NotificacaoLido = models.BooleanField(verbose_name='Lido', default=False, null=True, blank=True)
    Consultor = models.ForeignKey(Consultor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.NotificacaoTitulo