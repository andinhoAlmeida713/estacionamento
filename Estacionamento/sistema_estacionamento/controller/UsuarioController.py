from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.entidades.models import Usuario
from app.core import SecurityManager

class UsuarioController:
    @staticmethod
    def criar_usuario(usuario: Usuario, senha_pura: str, db: Session) -> Usuario:
        """
        Garante as regras de negócio para a criação de um usuário:
        1. Valida se o login fornecido já está em uso no sistema.
        2. Intercepta a senha em texto limpo e aplica a criptografia (hash) segura.
        3. Persiste o registro na tabela de 'usuarios' do MySQL de forma estável.
        """
        # Regra de negócio: impede logins idênticos no banco de dados
        statement = select(Usuario).where(Usuario.login == usuario.login)
        usuario_existente = db.exec(statement).first()
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este login já está sendo utilizado por outro usuário."
            )
        
        # Validação de segurança básica para impedir senhas vazias
        if not senha_pura or len(senha_pura.strip()) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha fornecida deve conter no mínimo 6 caracteres."
            )
        
        # Criptografa a senha pura usando o algoritmo seguro configurado no core
        usuario.senha_hash = SecurityManager.gerar_senha_hash(senha_pura)
        
        # Persiste o usuário de forma atômica no banco de dados
        try:
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
            return usuario
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno ao persistir o usuário no banco: {str(e)}"
            )

    @staticmethod
    def buscar_por_id(usuario_id: int, db: Session) -> Usuario:
        """
        Busca as informações cadastrais de um usuário específico pelo ID.
        """
        usuario = db.get(Usuario, usuario_id)
        if not usuario or not usuario.ativo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário ativo não encontrado."
            )
        return usuario
