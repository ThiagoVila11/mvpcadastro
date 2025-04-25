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
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    score = models.CharField(max_length=5, null=True, default="0")
    unidade = models.CharField(max_length=3, choices=unidades, null=True, default='BEL')
    apto = models.CharField(max_length=4, default=0)
    imagem = models.ImageField(upload_to='imagens/', default=None, null=True)
    visitarealizada = models.BooleanField(default=False, null=True)
    documentacaoenviada = models.FileField(default=None, null=True)


    def __str__(self):
        return self.nome