from django.db import models
from django.core.validators import EmailValidator

class Condominio(models.Model):

    condominionome = models.CharField(verbose_name="Nome do Condominio",  max_length=100, blank=True)
    condominionomecomercial = models.CharField(verbose_name="Nome Comercial do Condominio",  max_length=100, null=True, blank=True)
    condominionomepropriedade = models.CharField(verbose_name="Nome da Propriedade",  max_length=100, null=True, blank=True)
    condominiocnpj = models.CharField(verbose_name="CNPJ", max_length=14, null=True, default='')
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

    preclienteNome = models.CharField(verbose_name="Nome",  max_length=100)
    preclienteCpf = models.CharField(verbose_name="CPF", max_length=14, unique=True)
    precoclienteEmail = models.EmailField(verbose_name="E-mail",
                                    max_length=255,
                                    unique=True,  # Opcional: para garantir emails únicos
                                    validators=[EmailValidator(message="Digite um e-mail válido")],
                                    help_text="Exemplo: usuario@provedor.com")
    preclienteDataCadastro = models.DateTimeField(verbose_name="Data de cadastro", auto_now_add=True)
    preclienteScore = models.CharField(verbose_name='Score', null=True, blank=True, default='0')
    preclienteApontamentos = models.CharField(verbose_name='Apontamentos', null=True, blank=True)
    preclienteRendaPresumida = models.DecimalField(verbose_name="Renda Presumida", max_digits=10, decimal_places=2, null=True, blank=True)
    preclienteRendaFamiliar = models.DecimalField(verbose_name="Renda Familiar", max_digits=10, decimal_places=2, null=True, blank=True)
    preclienteAvalAuto = models.CharField(verbose_name='Avaliação Automática', max_length=1, null=True, blank=True)
    preclienteAvaliacao = models.CharField(verbose_name='Avaliação', max_length=1, null=True, blank=True)
    preclienteJson = models.TextField(verbose_name='Json', null=True, blank=True)

    def pode_ser_convertido(self):
        aprovado = 'N'
        score = int(self.preclienteScore) if self.preclienteScore else 0
        obs = len(self.preclienteApontamentos) if self.preclienteApontamentos else 0
        print(obs)
        if score >= 700 and obs == 0:
            aprovado = 'A'

        return aprovado == 'A'  # Só converte se estiver aprovado
    
    def converter_para_cliente(self, consultor=None, condominio=None, apartamento=None):
        """
        Converte um Pré-Cliente em Cliente
        """
        if not self.pode_ser_convertido():
            raise ValueError("Pré-cliente não está aprovado para conversão")
        
        cliente = Cliente(
            nome=self.preclienteNome,
            cpf=self.preclienteCpf,
            email=self.precoclienteEmail,
            score=self.preclienteScore,
            # Mapeie outros campos conforme necessário
            #Consultor=consultor,
            #Condominio=condominio,
            #Apartamento=apartamento,
            PreCliente=self,
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
    telefone = models.CharField(verbose_name="Celular", max_length=15, null=True, default='')
    endereco = models.CharField(verbose_name="Endereço", max_length=120, null=True, default='')
    data_nascimento = models.DateField(verbose_name="Data de nascimento", null=True, blank=True)
    observacoes = models.TextField(verbose_name="Observações", blank=True)
    data_cadastro = models.DateTimeField(verbose_name="Data de cadastro", auto_now_add=True)
    nomeresidente = models.CharField(verbose_name="Nome do residente", max_length=100, null=True, default='')
    cpfresidente = models.CharField(verbose_name="CPF do residente", max_length=14, null=True, default='')
    rgresidente = models.CharField(verbose_name="RG do residente", max_length=20, null=True, default='')
    score = models.CharField(verbose_name="Score", max_length=5, null=True, default="0")
    unidade = models.CharField(verbose_name="Unidade", max_length=3, choices=unidades, null=True, default='BEL')
    apto = models.CharField(verbose_name="Apto", max_length=4, default=0)
    nomeunidade = models.CharField(verbose_name="Nome do condomínio", max_length=50, null=True, default='')
    cnpjunidade = models.CharField(verbose_name="CNPJ condomínio", max_length=14, null=True, default='')
    matriculaunidade = models.CharField(verbose_name="Número da matrícula", max_length=30, null=True, default='')
    vagaunidade = models.CharField(verbose_name="Vaga(s)", max_length=1, choices=vaga, null=True, default='0')
    enderecounidade = models.CharField(verbose_name="Endereço da unidade", max_length=120, null=True, default='')
    nriptuunidade = models.CharField(verbose_name="Número IPTU", max_length=20, null=True, default='')
    vrunidade = models.DecimalField(verbose_name="Valor", max_digits=10, decimal_places=2, null=True, blank=True)
    prazocontrato = models.IntegerField(verbose_name="Prazo do Contrato", null=True, default=0)
    iniciocontrato = models.DateField(verbose_name="Início do contrato", null=True, blank=True)
    terminocontrato = models.DateField(verbose_name="Término do contrato", null=True, blank=True)
    imagem = models.ImageField(verbose_name="Imagem CNH", upload_to='imagens/', default=None, null=True)
    visitarealizada = models.BooleanField(verbose_name="Visita realizado", default=False, null=True)
    documentacaoenviada = models.FileField(verbose_name="Pré-Contrato", default=None, null=True)
    Condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, null=True, blank=True)
    Apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE, null=True, blank=True)
    Consultor = models.ForeignKey(Consultor, on_delete=models.CASCADE, null=True, blank=True)
    PreCliente = models.ForeignKey(PreCliente, on_delete=models.CASCADE, null=True, blank=True, unique=True)

    def __str__(self):
        return self.nome
    
