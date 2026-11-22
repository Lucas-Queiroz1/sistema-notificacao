"""Sistema de Notificação — Factory Method (criacional) + Strategy (comportamental).

Trabalho de UML Avançada e Padrões de Projeto (Aulas 9 a 15).
Execute com:  python main.py
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


# ===== Modelos =====
class StatusEnvio(Enum):
    PENDENTE = "pendente"
    ENVIADA = "enviada"
    FALHA = "falha"


@dataclass
class Usuario:
    nome: str
    contato: str
    canal_preferido: str


@dataclass
class Mensagem:
    titulo: str
    corpo: str
    status: StatusEnvio = field(default=StatusEnvio.PENDENTE)


# ===== Produto abstrato e canais concretos =====
class Notificacao(ABC):
    """Produto abstrato do Factory Method (e interface da Strategy)."""

    @abstractmethod
    def enviar(self, destinatario: str, titulo: str, msg: str) -> bool:
        ...


class EmailNotificacao(Notificacao):
    def enviar(self, destinatario: str, titulo: str, msg: str) -> bool:
        print(f"[EMAIL] Para {destinatario} | Assunto: {titulo} | {msg}")
        return True


class SmsNotificacao(Notificacao):
    def enviar(self, destinatario: str, titulo: str, msg: str) -> bool:
        print(f"[SMS]   Para {destinatario} | {msg}")
        return True


class PushNotificacao(Notificacao):
    def enviar(self, destinatario: str, titulo: str, msg: str) -> bool:
        print(f"[PUSH]  Para {destinatario} | {titulo}: {msg}")
        return True


# ===== Fábrica (Factory Method) =====
class NotificacaoFactory:
    """Factory Method: decide qual canal instanciar a partir de um nome."""

    _canais: dict[str, type[Notificacao]] = {
        "email": EmailNotificacao,
        "sms": SmsNotificacao,
        "push": PushNotificacao,
    }

    @classmethod
    def criar(cls, canal: str) -> Notificacao:
        try:
            return cls._canais[canal.lower()]()
        except KeyError:
            raise ValueError(f"Canal desconhecido: {canal!r}") from None

    @classmethod
    def registrar(cls, nome: str, classe: type[Notificacao]) -> None:
        """Permite adicionar um novo canal sem alterar o código existente (RF05)."""
        cls._canais[nome.lower()] = classe


# ===== Cliente (Notificador) =====
class Notificador:
    """Cliente: não conhece as classes concretas dos canais."""

    def __init__(self, factory: type[NotificacaoFactory] = NotificacaoFactory):
        self._factory = factory

    def notificar(self, usuario: Usuario, mensagem: Mensagem) -> bool:
        try:
            canal = self._factory.criar(usuario.canal_preferido)
            ok = canal.enviar(usuario.contato, mensagem.titulo, mensagem.corpo)
        except ValueError as erro:
            print(f"[ERRO] {erro}")
            ok = False
        mensagem.status = StatusEnvio.ENVIADA if ok else StatusEnvio.FALHA
        return ok


# ===== Demonstração =====
# Novo canal adicionado sem mexer no código existente (RF05)
class WhatsAppNotificacao(Notificacao):
    def enviar(self, destinatario: str, titulo: str, msg: str) -> bool:
        print(f"[WHATS] Para {destinatario} | {msg}")
        return True


def main() -> None:
    notificador = Notificador()
    msg = Mensagem("Pedido enviado", "Seu pedido saiu para entrega")

    usuarios = [
        Usuario("Ana", "ana@email.com", "email"),
        Usuario("Bruno", "+55 88 99999-0000", "sms"),
        Usuario("Carla", "device-token-123", "push"),
        Usuario("Davi", "x", "fax"),  # canal inexistente -> FALHA
    ]
    for u in usuarios:
        m = Mensagem(msg.titulo, msg.corpo)
        notificador.notificar(u, m)
        print(f"   -> {u.nome}: {m.status.name}\n")

    NotificacaoFactory.registrar("whatsapp", WhatsAppNotificacao)
    m = Mensagem(msg.titulo, msg.corpo)
    notificador.notificar(Usuario("Eva", "+55 85 98888-0000", "whatsapp"), m)
    print(f"   -> Eva: {m.status.name}")


if __name__ == "__main__":
    main()
