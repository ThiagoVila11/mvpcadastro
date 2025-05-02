from django.db import models

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

    def __str__(self):
        return self.nome