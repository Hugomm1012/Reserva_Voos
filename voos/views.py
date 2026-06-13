"""
views.py — Lógica de negócio e controlo de páginas
====================================================
Cada classe View corresponde a uma URL definida em urls.py.
Herança usada:
  - ListView / DetailView / CreateView / UpdateView / DeleteView — CRUD genérico
  - TemplateView — páginas que só mostram dados, sem formulário de modelo
  - View        — lógica personalizada com GET e POST separados
  - LoginRequiredMixin  — redireciona para login se não autenticado
  - UserPassesTestMixin — restringe acesso com base numa condição (ex: is_staff)
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Voo, Passageiro, Reserva
from .forms import VooForm, PassageiroForm, ReservaForm, RegisterForm


# ---------------------------------------------------------------------------
# HOMEPAGE
# ---------------------------------------------------------------------------

class IndexView(TemplateView):
    """Página inicial com o formulário de pesquisa de voos."""
    template_name = 'Voos/index.html'


# ---------------------------------------------------------------------------
# VOO — CRUD completo
# ---------------------------------------------------------------------------

class VooListView(ListView):
    """Lista de voos disponíveis, com filtros por origem, destino e data.

    Os parâmetros GET (origin, destination, date) são aplicados ao queryset
    com Q objects para suportar pesquisa por cidade OU código IATA.
    Só mostra voos com lugares disponíveis (lugares_disponiveis > 0).
    """
    model               = Voo
    template_name       = 'Voos/flights.html'
    context_object_name = 'voos'
    paginate_by         = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('companhia', 'origem', 'destino')
        origin      = self.request.GET.get('origin', '').strip()
        destination = self.request.GET.get('destination', '').strip()
        date        = self.request.GET.get('date', '').strip()

        if origin:
            # Pesquisa por cidade OU código do aeroporto (case-insensitive)
            qs = qs.filter(
                Q(origem__cidade__icontains=origin) | Q(origem__codigo__icontains=origin)
            )
        if destination:
            qs = qs.filter(
                Q(destino__cidade__icontains=destination) | Q(destino__codigo__icontains=destination)
            )
        if date:
            qs = qs.filter(data_partida__date=date)

        return qs.filter(lugares_disponiveis__gt=0)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['origin']      = self.request.GET.get('origin', '')
        ctx['destination'] = self.request.GET.get('destination', '')
        ctx['date']        = self.request.GET.get('date', '')
        ctx['passengers']  = self.request.GET.get('passengers', '1')
        # Preserva os filtros ativos nos links de paginação (ex: ?origin=Lisboa&destination=Paris)
        params = self.request.GET.copy()
        params.pop('page', None)
        ctx['query_string'] = params.urlencode()
        return ctx


class VooDetailView(DetailView):
    """Detalhe de um voo específico, identificado pelo número (ex: TP123)."""
    model               = Voo
    template_name       = 'Voos/voo_detail.html'
    context_object_name = 'voo'
    slug_field          = 'numero'      # Campo do modelo usado como identificador na URL
    slug_url_kwarg      = 'numero'      # Nome do parâmetro na URL: voos/<str:numero>/


class VooCreateView(LoginRequiredMixin, CreateView):
    """Criar um novo voo (requer login)."""
    model        = Voo
    form_class   = VooForm
    template_name = 'Voos/voo_form.html'
    success_url  = reverse_lazy('voos:flights')
    login_url    = reverse_lazy('voos:login')


class VooUpdateView(LoginRequiredMixin, UpdateView):
    """Editar um voo existente (requer login)."""
    model          = Voo
    form_class     = VooForm
    template_name  = 'Voos/voo_form.html'
    slug_field     = 'numero'
    slug_url_kwarg = 'numero'
    success_url    = reverse_lazy('voos:flights')
    login_url      = reverse_lazy('voos:login')


class VooDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar um voo (requer login). Mostra página de confirmação antes de apagar."""
    model          = Voo
    template_name  = 'Voos/voo_confirm_delete.html'
    slug_field     = 'numero'
    slug_url_kwarg = 'numero'
    success_url    = reverse_lazy('voos:flights')
    login_url      = reverse_lazy('voos:login')


# ---------------------------------------------------------------------------
# PASSAGEIRO — CRUD completo
# ---------------------------------------------------------------------------

class PassageiroListView(LoginRequiredMixin, ListView):
    """Lista todos os passageiros registados (requer autenticação)."""
    model               = Passageiro
    template_name       = 'Voos/passageiro_list.html'
    context_object_name = 'passageiros'
    paginate_by         = 20
    login_url           = reverse_lazy('voos:login')


class PassageiroDetailView(LoginRequiredMixin, DetailView):
    """Detalhe de um passageiro."""
    model               = Passageiro
    template_name       = 'Voos/passageiro_detail.html'
    context_object_name = 'passageiro'
    login_url           = reverse_lazy('voos:login')


class PassageiroCreateView(LoginRequiredMixin, CreateView):
    """Criar um novo passageiro."""
    model         = Passageiro
    form_class    = PassageiroForm
    template_name = 'Voos/passageiro_form.html'
    success_url   = reverse_lazy('voos:passageiro-list')
    login_url     = reverse_lazy('voos:login')


class PassageiroUpdateView(LoginRequiredMixin, UpdateView):
    """Editar um passageiro existente."""
    model         = Passageiro
    form_class    = PassageiroForm
    template_name = 'Voos/passageiro_form.html'
    success_url   = reverse_lazy('voos:passageiro-list')
    login_url     = reverse_lazy('voos:login')


class PassageiroDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar um passageiro."""
    model         = Passageiro
    template_name = 'Voos/passageiro_confirm_delete.html'
    success_url   = reverse_lazy('voos:passageiro-list')
    login_url     = reverse_lazy('voos:login')


# ---------------------------------------------------------------------------
# RESERVA — CRUD completo
# ---------------------------------------------------------------------------

class ReservaListView(LoginRequiredMixin, ListView):
    """Lista todas as reservas (admin)."""
    model               = Reserva
    template_name       = 'Voos/reserva_list.html'
    context_object_name = 'reservas'
    paginate_by         = 20
    login_url           = reverse_lazy('voos:login')


class ReservaDetailView(LoginRequiredMixin, DetailView):
    """Detalhe de uma reserva."""
    model               = Reserva
    template_name       = 'Voos/reserva_detail.html'
    context_object_name = 'reserva'
    login_url           = reverse_lazy('voos:login')


class ReservaCreateView(LoginRequiredMixin, CreateView):
    """Criar uma reserva manualmente (admin)."""
    model         = Reserva
    form_class    = ReservaForm
    template_name = 'Voos/reserva_form.html'
    success_url   = reverse_lazy('voos:reserva-list')
    login_url     = reverse_lazy('voos:login')


class ReservaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar uma reserva existente (admin)."""
    model         = Reserva
    form_class    = ReservaForm
    template_name = 'Voos/reserva_form.html'
    success_url   = reverse_lazy('voos:reserva-list')
    login_url     = reverse_lazy('voos:login')


class ReservaDeleteView(LoginRequiredMixin, DeleteView):
    """Cancelar/eliminar uma reserva. Devolve o lugar ao voo e redireciona para a conta."""
    model         = Reserva
    template_name = 'Voos/reserva_confirm_delete.html'
    success_url   = reverse_lazy('voos:account')
    login_url     = reverse_lazy('voos:login')

    def form_valid(self, form):
        reserva = self.get_object()
        if reserva.status != 'cancelada':
            voo = reserva.voo
            voo.lugares_disponiveis += 1
            voo.save()
        return super().form_valid(form)


class ReservaConfirmView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Confirma uma reserva — exclusivo para gestores.

    Recebe POST com o pk da reserva, muda o status para 'confirmada'
    e redireciona para o painel admin.
    """
    login_url = reverse_lazy('voos:login')

    def test_func(self):
        u = self.request.user
        return u.is_superuser or u.groups.filter(name='gestor').exists()

    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        reserva.status = 'confirmada'
        reserva.save()
        return redirect('voos:admin-panel')


class ReservaCancelView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Cancela uma reserva — exclusivo para gestores."""
    login_url = reverse_lazy('voos:login')

    def test_func(self):
        u = self.request.user
        return u.is_superuser or u.groups.filter(name='gestor').exists()

    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        if reserva.status != 'cancelada':
            voo = reserva.voo
            voo.lugares_disponiveis += 1
            voo.save()
        reserva.status = 'cancelada'
        reserva.save()
        return redirect('voos:admin-panel')


# ---------------------------------------------------------------------------
# AUTENTICAÇÃO
# ---------------------------------------------------------------------------

class VoosLoginView(LoginView):
    """Página de login. Passa também o RegisterForm para o mesmo template
    para que login e registo apareçam lado a lado.
    """
    template_name            = 'Voos/login.html'
    redirect_authenticated_user = True  # Se já estiver autenticado, redireciona direto

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Aplica classe CSS a todos os campos do formulário de autenticação
        for field in form.fields.values():
            field.widget.attrs['class'] = 'input'
        return form

    def get_success_url(self):
        return reverse_lazy('voos:account')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['register_form'] = RegisterForm()  # Formulário de registo no mesmo template
        return ctx


class RegisterView(View):
    """Processa o formulário de registo de nova conta.

    POST: valida RegisterForm, cria User, faz login automático e redireciona para /conta/.
    Se a validação falhar, volta ao login.html com os erros e show_register=True
    para que o painel de registo fique visível.
    """
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('voos:account')

        # Validação falhou — volta ao template com o formulário de login também
        from django.contrib.auth.forms import AuthenticationForm
        login_form = AuthenticationForm()
        for field in login_form.fields.values():
            field.widget.attrs['class'] = 'input'
        return render(request, 'Voos/login.html', {
            'form':          login_form,
            'register_form': form,
            'show_register': True,  # Abre o painel de registo em vez do de login
        })


class VoosLogoutView(LogoutView):
    """Termina a sessão e redireciona para a homepage."""
    next_page = reverse_lazy('voos:index')


# ---------------------------------------------------------------------------
# ÁREA DO CLIENTE
# ---------------------------------------------------------------------------

class AccountView(LoginRequiredMixin, TemplateView):
    """Página pessoal do cliente: mostra as suas reservas.

    Liga o utilizador Django (request.user) ao Passageiro pelo email.
    Se não existir Passageiro com esse email, mostra lista vazia.
    """
    template_name = 'Voos/account.html'
    login_url     = reverse_lazy('voos:login')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            # Encontra o Passageiro cujo email corresponde ao utilizador autenticado
            passageiro = Passageiro.objects.get(email=self.request.user.email)
            reservas   = Reserva.objects.filter(passageiro=passageiro).select_related(
                'voo', 'voo__origem', 'voo__destino', 'voo__companhia'
            ).order_by('-data_reserva')
        except Passageiro.DoesNotExist:
            reservas = Reserva.objects.none()
        ctx['reservas'] = reservas
        return ctx


# ---------------------------------------------------------------------------
# RESERVAR UM VOO ESPECÍFICO
# ---------------------------------------------------------------------------

class BookingView(LoginRequiredMixin, View):
    """Página e lógica de reserva de um voo.

    GET:  mostra o formulário com os detalhes do voo.
    POST: valida os dados do passageiro, cria Passageiro (se não existir),
          cria Reserva, decrementa lugares_disponiveis e redireciona para /conta/.
    """
    template_name = 'Voos/booking.html'
    login_url     = reverse_lazy('voos:login')

    def get(self, request, numero):
        voo = get_object_or_404(Voo, numero=numero)
        return render(request, self.template_name, {
            'voo':   voo,
            'email': request.user.email,  # Pré-preenche o email com o do utilizador
        })

    def post(self, request, numero):
        voo = get_object_or_404(Voo, numero=numero)

        nome           = request.POST.get('nome', '').strip()
        email          = request.POST.get('email', '').strip() or request.user.email
        telefone       = request.POST.get('telefone', '').strip()
        documento      = request.POST.get('documento', '').strip()
        numero_assento = request.POST.get('numero_assento', '').strip()

        # Validação manual (campos obrigatórios + assento disponível)
        errors = []
        if not nome:           errors.append('O nome completo é obrigatório.')
        if not documento:      errors.append('O número de documento é obrigatório.')
        if not telefone:       errors.append('O telemóvel é obrigatório.')
        if not numero_assento: errors.append('O número do assento é obrigatório.')
        if voo.lugares_disponiveis <= 0:
            errors.append('Este voo não tem lugares disponíveis.')
        if numero_assento and Reserva.objects.filter(voo=voo, numero_assento=numero_assento).exists():
            errors.append(f'O assento {numero_assento} já está ocupado. Escolha outro.')

        if errors:
            return render(request, self.template_name, {
                'voo': voo, 'errors': errors,
                'nome': nome, 'email': email,
                'telefone': telefone, 'documento': documento,
                'numero_assento': numero_assento,
            })

        # Cria o Passageiro se ainda não existir (identifica pelo email)
        try:
            passageiro = Passageiro.objects.get(email=email)
        except Passageiro.DoesNotExist:
            try:
                passageiro = Passageiro.objects.create(
                    email=email, nome=nome, telefone=telefone, documento=documento,
                )
            except Exception:
                return render(request, self.template_name, {
                    'voo': voo,
                    'errors': ['Erro ao criar o passageiro. O número de documento pode já estar registado.'],
                    'nome': nome, 'email': email, 'telefone': telefone,
                    'documento': documento, 'numero_assento': numero_assento,
                })

        # Cria a reserva e reduz os lugares disponíveis
        Reserva.objects.create(
            voo=voo,
            passageiro=passageiro,
            numero_assento=numero_assento,
            status='pendente',
        )
        voo.lugares_disponiveis -= 1
        voo.save()

        return redirect('voos:account')


# ---------------------------------------------------------------------------
# PAINEL DE ADMINISTRAÇÃO PERSONALIZADO
# ---------------------------------------------------------------------------

class AdminPanelView(UserPassesTestMixin, TemplateView):
    """Dashboard para gestores: estatísticas, reservas e lista de todos os voos.

    Só acessível a utilizadores do grupo "gestor" ou superusers.
    Passa ao template:
      - voos_hoje          — número de voos que partem hoje
      - reservas_ativas    — reservas pendentes + confirmadas
      - checkin_pendente   — reservas ainda por confirmar
      - reservas_pendentes — queryset com detalhes
      - reservas_confirmadas — queryset com detalhes
      - todos_voos         — todos os voos para a tabela de gestão
      - total_passageiros  — contagem total de passageiros registados
    """
    template_name = 'Voos/admin.html'
    login_url     = reverse_lazy('voos:login')

    def test_func(self):
        u = self.request.user
        return u.is_superuser or u.groups.filter(name='gestor').exists()

    def get_context_data(self, **kwargs):
        ctx   = super().get_context_data(**kwargs)
        today = timezone.now().date()

        ctx['voos_hoje']           = Voo.objects.filter(data_partida__date=today).count()
        ctx['reservas_ativas']     = Reserva.objects.filter(status__in=['pendente', 'confirmada']).count()
        ctx['checkin_pendente']    = Reserva.objects.filter(status='pendente').count()
        ctx['reservas_pendentes']  = Reserva.objects.filter(status='pendente').select_related(
            'passageiro', 'voo', 'voo__origem', 'voo__destino'
        )
        ctx['reservas_confirmadas'] = Reserva.objects.filter(status='confirmada').select_related(
            'passageiro', 'voo', 'voo__origem', 'voo__destino'
        )
        ctx['todos_voos']         = Voo.objects.select_related('companhia', 'origem', 'destino').all()
        ctx['total_passageiros']  = Passageiro.objects.count()
        return ctx


# ---------------------------------------------------------------------------
# ERROS
# ---------------------------------------------------------------------------

def pagina_nao_encontrada(request, exception):
    """Handler para erros 404 — mostra uma página personalizada."""
    return render(request, 'Voos/404.html', status=404)
