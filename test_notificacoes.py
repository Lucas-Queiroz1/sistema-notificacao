import unittest

from main import (
    EmailNotificacao, SmsNotificacao, PushNotificacao, NotificacaoFactory,
    Notificador, Usuario, Mensagem, StatusEnvio,
)


class TestFactory(unittest.TestCase):
    def test_cria_canais(self):
        self.assertIsInstance(NotificacaoFactory.criar("email"), EmailNotificacao)
        self.assertIsInstance(NotificacaoFactory.criar("SMS"), SmsNotificacao)
        self.assertIsInstance(NotificacaoFactory.criar("push"), PushNotificacao)

    def test_canal_invalido(self):
        with self.assertRaises(ValueError):
            NotificacaoFactory.criar("fax")

    def test_status_apos_envio(self):
        m = Mensagem("t", "c")
        self.assertEqual(m.status, StatusEnvio.PENDENTE)
        Notificador().notificar(Usuario("A", "a@a.com", "email"), m)
        self.assertEqual(m.status, StatusEnvio.ENVIADA)

    def test_status_falha(self):
        m = Mensagem("t", "c")
        Notificador().notificar(Usuario("A", "x", "fax"), m)
        self.assertEqual(m.status, StatusEnvio.FALHA)


if __name__ == "__main__":
    unittest.main()
