"""
models.py — Modelos da base de dados
=====================================
Define as tabelas (entidades) do projeto.
Django cria as tabelas automaticamente no SQLite com base nestas classes.

Relações:
  Companhia  ←──┐
  Aeroporto  ←──┤── Voo ──→ Reserva ←── Passageiro
"""

from django.db import models
from django.urls import reverse_lazy


class Companhia(models.Model):
    """Companhia aérea que opera os voos (ex: TAP, Ryanair)."""
    nome = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Companhias"


class Aeroporto(models.Model):
    """Aeroporto de origem ou destino de um voo.

    O campo 'codigo' segue o padrão IATA de 3 letras (ex: LIS, LHR, CDG).
    """
    codigo = models.CharField(max_length=3, unique=True)  # Código IATA: LIS, LHR, CDG...
    nome   = models.CharField(max_length=150, blank=True) # Nome completo (opcional)
    cidade = models.CharField(max_length=100)
    pais   = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.cidade}"


class Voo(models.Model):
    """Voo disponível para reserva.

    Um voo tem uma companhia, uma origem e um destino (ambos Aeroportos).
    O campo 'lugares_disponiveis' é decrementado cada vez que uma reserva é criada.
    """
    numero               = models.CharField(max_length=10, unique=True)     # Ex: TP123
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
    """Pessoa que faz reservas.

    O email é único e é usado para ligar o Passageiro à conta do utilizador Django.
    Ver AccountView e BookingView em views.py.
    """
    nome         = models.CharField(max_length=100)
    email        = models.EmailField(unique=True)        # Chave de ligação ao User do Django
    telefone     = models.CharField(max_length=15)
    documento    = models.CharField(max_length=20, unique=True)  # Passaporte ou BI
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse_lazy('voos:passageiro-detail', kwargs={'pk': self.pk})


class Reserva(models.Model):
    """Reserva de um assento num voo por um passageiro.

    O status começa em 'pendente' e pode ser confirmado ou cancelado pelo staff.
    A combinação (voo, numero_assento) é única — dois passageiros não podem ter o mesmo assento.
    """
    STATUS = [
        ('pendente',   'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada',  'Cancelada'),
    ]
    voo            = models.ForeignKey(Voo, on_delete=models.CASCADE)
    passageiro     = models.ForeignKey(Passageiro, on_delete=models.CASCADE)
    data_reserva   = models.DateTimeField(auto_now_add=True)
    status         = models.CharField(max_length=20, choices=STATUS, default='pendente')
    numero_assento = models.CharField(max_length=5)  # Ex: 12A

    def __str__(self):
        return f"{self.passageiro.nome} - {self.voo.numero}"

    def get_absolute_url(self):
        return reverse_lazy('voos:reserva-detail', kwargs={'pk': self.pk})

    class Meta:
        # Garante que um assento só pode ser reservado uma vez por voo
        unique_together = ('voo', 'numero_assento')
