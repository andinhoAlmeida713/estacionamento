import os
import pymysql
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_wtf.csrf import CSRFProtect

# Criptografia segura do Core para manter compatibilidade total com o FastAPI
from app.core import SecurityManager

# Serviço de integração para consumir a API do FastAPI via Requests
from services import EstacionamentoService

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__, static_url_path='/static')
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Ativa a proteção contra ataques CSRF nos formulários
csrf = CSRFProtect(app)

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")

if not app.config["SECRET_KEY"] or app.config["SECRET_KEY"].startswith("SUBSTITUA"):
    raise RuntimeError("Configure uma SECRET_KEY segura no arquivo .env")


def conectar_banco():
    """
    Conexão temporária nativa para o Flask-Login carregar a sessão do banco.
    As operações complexas de negócio ocorrem através do FastAPI.
    """
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "aluno25"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )


# Configuração do Gerenciador de Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Faça login para acessar o sistema."
login_manager.login_message_category = "aviso"


class Usuario(UserMixin):
    def __init__(self, dados):
        self.id = str(dados["id"])
        self.estacionamento_id = dados["estacionamento_id"]
        self.nome = dados["nome"]
        self.login = dados["login"]
        self.perfil = dados["perfil"]
        self.ativo = dados["ativo"]


@login_manager.user_loader
def carregar_usuario(usuario_id):
    conexao = conectar_banco()
    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, estacionamento_id, nome, login, perfil, ativo
                FROM usuarios
                WHERE id = %s AND ativo = 1
                """,
                (usuario_id,),
            )
            dados = cursor.fetchone()
            if dados:
                return Usuario(dados)
            return None
    except Exception:
        return None
    finally:
        conexao.close()


@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.perfil == "administrador":
            return redirect(url_for("admin"))
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        usuario_login = request.form.get("login", "").strip()
        senha = request.form.get("senha", "")

        if not usuario_login or not senha:
            flash("Informe o usuário e a senha.", "erro")
            return render_template("login.html")

        conexao = conectar_banco()
        dados = None
        try:
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, estacionamento_id, nome, login,
                           senha_hash, perfil, ativo
                    FROM usuarios
                    WHERE login = %s
                    LIMIT 1
                    """,
                    (usuario_login,),
                )
                dados = cursor.fetchone()
        except Exception as e:
            flash("Erro de conexão com o banco de dados.", "erro")
            return render_template("login.html")
        finally:
            conexao.close()

        # Validação cruzada da senha usando o hash Bcrypt gerado no Core/FastAPI
        if (
            dados
            and dados["ativo"]
            and SecurityManager.verificar_senha(senha, dados["senha_hash"])
        ):
            usuario = Usuario(dados)
            login_user(usuario)

            # Registra o timestamp do último acesso na tabela usuarios
            conexao = conectar_banco()
            try:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        "UPDATE usuarios SET ultimo_acesso = CURRENT_TIMESTAMP WHERE id = %s",
                        (dados["id"],),
                    )
                conexao.commit()
            except Exception:
                pass
            finally:
                conexao.close()

            if usuario.perfil == "administrador":
                return redirect(url_for("admin"))
            return redirect(url_for("dashboard"))

        flash("Usuário ou senha inválidos.", "erro")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    estacionamento_id = current_user.estacionamento_id
    veiculos = EstacionamentoService.buscar_veiculos(estacionamento_id)
    movimentacoes = EstacionamentoService.buscar_movimentacoes_ativas(estacionamento_id)
    
    return render_template(
        "dashboard.html",
        area_admin=False,
        veiculos=veiculos,
        movimentacoes=movimentacoes
    )


@app.route("/movimentacoes/checkout/<int:movimentacao_id>", methods=["GET", "POST"])
@login_required
def checkout(movimentacao_id):
    # Dicionários simulados temporários para renderização segura
    movimentacao_mock = {
        "id": movimentacao_id,
        "placa": "ABC1234",
        "entrada_em": "29/10/2026 14:00:00",
        "valor_calculado": "15.00",
        "valor_cobrado": "15.00"
    }
    veiculo_mock = {
        "marca": "Chevrolet",
        "modelo": "Onix",
        "cor": "Preto",
        "tipo": "carro"
    }

    if request.method == "POST":
        desconto = request.form.get("desconto", "0.00")
        forma_pagamento = request.form.get("forma_pagamento")
        
        # Futura integração: EstacionamentoService.registrar_saida(movimentacao_id, desconto)
        flash("Pagamento processado e movimentação finalizada com sucesso!", "sucesso")
        return redirect(url_for("dashboard"))

    return render_template(
        "checkout.html",
        movimentacao=movimentacao_mock,
        veiculo=veiculo_mock,
        horario_saida_atual="29/10/2026 15:15:00",
        tempo_decorrido_formatado="01h 15min"
    )


# ==========================================================================
# ROTA ADICIONADA: Tela de Cadastro Operacional de Veículos e Clientes
# ==========================================================================
@app.route("/veiculos/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_veiculo_tela():
    if request.method == "POST":
        placa = request.form.get("placa")
        
        # Futura integração com o endpoint POST do FastAPI que criamos
        flash(f"Veículo de placa {placa} cadastrado com sucesso!", "sucesso")
        return redirect(url_for("dashboard"))

    return render_template("cadastro_veiculo.html")


# ==========================================================================
# ROTA ADICIONADA: Painel Gerencial de Faturamento e Fechamento de Caixa
# ==========================================================================
@app.route("/gerencial/faturamento", methods=["GET"])
@login_required
def faturamento_tela():
    # Proteção de Perfil: Apenas administradores acessam o faturamento bruto
    if current_user.perfil != "administrador":
        flash("Você não tem permissão para acessar essa área.", "erro")
        return redirect(url_for("dashboard"))

    # Dicionários estruturados simulados para alimentar os KPIs do HTML
    resumo_mock = {
        "total": "1.450,00",
        "pix": "820,00",
        "dinheiro": "380,00",
        "cartao": "250,00"
    }
    
    return render_template(
        "faturamento.html",
        resumo=resumo_mock,
        historico=[]  # Carrega dados do bloco "else" do HTML para fins de teste
    )


@app.route("/admin")
@login_required
def admin():
    if current_user.perfil != "administrador":
        flash("Você não tem permissão para acessar essa área.", "erro")
        return redirect(url_for("dashboard"))

    estacionamento_id = current_user.estacionamento_id
    veiculos = EstacionamentoService.buscar_veiculos(estacionamento_id)
    movimentacoes = EstacionamentoService.buscar_movimentacoes_ativas(estacionamento_id)

    return render_template(
        "dashboard.html",
        area_admin=True,
        veiculos=veiculos,
        movimentacoes=movimentacoes
    )


@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash("Você saiu do sistema.", "sucesso")
    return redirect(url_for("login"))


if __name__ == "__main__":
    porta = int(os.getenv("FLASK_PORT", 5000))
    app.run(debug=True, port=porta)
