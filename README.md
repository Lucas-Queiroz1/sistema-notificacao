# Sistema de Notificação — Factory Method + Strategy

Trabalho de UML Avançada e Padrões de Projeto (Aulas 9 a 15).

Módulo de notificação com canais E-mail, SMS e Push. O padrão **Factory Method**
(criacional) é implementado na classe `NotificacaoFactory`; os canais seguem o
padrão **Strategy** (comportamental) por meio da interface `Notificacao`.

## Arquivos
- `main.py` — todo o código (modelos, canais, fábrica, notificador e demonstração)
- `test_notificacoes.py` — testes automatizados

## Como executar
```bash
python main.py
python -m unittest test_notificacoes -v
```
Requer Python 3.9+. Sem dependências externas.
