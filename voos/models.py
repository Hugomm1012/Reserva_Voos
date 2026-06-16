from django.db import models
from django.urls import reverse_lazy

# Companhia e Aeroporto são só tabelas de apoio (dados que o Voo precisa).
# A relação principal é: Voo <- Reserva -> Passageiro.


class Companhia(models.Model):
    nome = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Companhias"


class Aeroporto(models.Model):
    """
    Aeroporto. 
    O 'codigo' é o código IATA.
    """
    codigo = models.CharField(max_length=3, unique=True)
    nome   = models.CharField(max_length=150, blank=True)
    cidade = models.CharField(max_length=100)
    pais   = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.cidade}"


class Voo(models.Model):
    """
    Um voo. Tem 2 FKs para Aeroporto (origem/destino), por isso preciso
    de related_name diferente em cada uma — senão o Django não sabe separar
    'voos que partem daqui' de 'voos que chegam aqui'.
    """
    numero               = models.CharField(max_length=10, unique=True)  # ex: TP123
    companhia            = models.ForeignKey(Companhia, on_delete=models.CASCADE)
    origem               = models.ForeignKey(Aeroporto, on_delete=models.CASCADE, related_name='saidas')
    destino              = models.ForeignKey(Aeroporto, on_delete=models.CASCADE, related_name='chegadas')
    data_partida         = models.DateTimeField()
    data_chegada         = models.DateTimeField()
    lugares_disponiveis  = models.IntegerField()
    preco                = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.numero}"

    def get_absolute_url(self):
        return reverse_lazy('voos:voo-detail', kwargs={'numero': self.numero})


class Passageiro(models.Model):
    """
    A pessoa que viaja — separado do User (login) porque um gestor pode
    criar uma reserva para alguém sem conta no site. 
    Liga-se à área de conta do cliente pelo email (ver AccountView).
    """
    nome         = models.CharField(max_length=100)
    email        = models.EmailField(unique=True)
    telefone     = models.CharField(max_length=15)
    documento    = models.CharField(max_length=20, unique=True) 
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse_lazy('voos:passageiro-detail', kwargs={'pk': self.pk})


class Reserva(models.Model):
    """
    Liga um Passageiro a um Voo (e a um lugar específico).

    unique_together garante que ninguém reserva o mesmo lugar duas vezes.
    """
    STATUS = [
        ('pendente',   'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada',  'Cancelada'),
    ]
    CLASSE = [
        ('económica', 'Económica'),
        ('executiva', 'Executiva'),
    ]
    voo            = models.ForeignKey(Voo, on_delete=models.CASCADE)
    passageiro     = models.ForeignKey(Passageiro, on_delete=models.CASCADE)
    data_reserva   = models.DateTimeField(auto_now_add=True)
    status         = models.CharField(max_length=20, choices=STATUS, default='pendente')
    numero_assento = models.CharField(max_length=5)  # ex: 12A
    classe_voo     = models.CharField(max_length=20, choices=CLASSE, default='económica')

    def __str__(self):
        return f"{self.passageiro.nome} - {self.voo.numero}"

    def get_absolute_url(self):
        return reverse_lazy('voos:reserva-detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('voo', 'numero_assento')
