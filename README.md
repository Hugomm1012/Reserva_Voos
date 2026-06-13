# FlyMaster Airlines ✈️

Sistema de reserva de voos desenvolvido em Django, como projeto académico da unidade curricular de Programação 2.

**Autores:** Hugo Moreira · Tomás Belo

---

## Funcionalidades

- Pesquisa de voos por origem, destino e data
- Reserva de voos com seleção de assento
- Área de conta com histórico de reservas
- Painel de administração para gestores (confirmar/cancelar reservas, gerir voos)
- Separação de permissões por grupos (`gestor` / utilizador normal)
- Paginação nas listas de voos, passageiros e reservas
- Página 404 personalizada

## Tecnologias

- Python 3.12
- Django 5.2
- SQLite
- HTML5 · CSS3

## Estrutura do projeto

```
Reserva_Voos/
├── reserva_voos/        # Configurações Django (settings, urls)
├── voos/                # Aplicação principal
│   ├── models.py        # Companhia, Aeroporto, Voo, Passageiro, Reserva
│   ├── views.py         # Class-based views
│   ├── forms.py         # Formulários
│   ├── urls.py          # Rotas da aplicação
│   ├── context_processors.py
│   └── templates/Voos/  # Templates HTML
├── static/              # CSS e JS
├── requirements.txt
└── manage.py
```

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/Hugomm1012/Reserva_Voos.git
cd Reserva_Voos

# Criar e ativar ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar superutilizador
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

## Modelos

| Modelo | Descrição |
|---|---|
| `Companhia` | Companhia aérea (ex: TAP, Ryanair) |
| `Aeroporto` | Aeroporto com código IATA |
| `Voo` | Voo com origem, destino, preço e lugares disponíveis |
| `Passageiro` | Passageiro identificado por email e documento |
| `Reserva` | Reserva de um assento num voo por um passageiro |

## Permissões

| Grupo | Acesso |
|---|---|
| Superuser | Django admin (`/admin/`) |
| `gestor` | Painel HTML (`/admin-painel/`) — confirmar/cancelar reservas, gerir voos |
| Utilizador normal | Pesquisa de voos e área de conta (`/conta/`) |
