from passlib.context import CryptContext

# Configura o contexto de criptografia utilizando o algoritmo bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityManager:
    @staticmethod
    def gerar_senha_hash(senha_pura: str) -> str:
        """
        Transforma uma senha em texto puro em um hash seguro 
        para ser armazenado no banco de dados.
        """
        return pwd_context.hash(senha_pura)

    @staticmethod
    def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
        """
        Compara uma senha em texto puro com o hash armazenado 
        para validar a autenticação do usuário.
        """
        return pwd_context.verify(senha_pura, senha_hash)
