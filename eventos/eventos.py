from collections import defaultdict

eventos = defaultdict(list)


def registrar_evento(evento, funcao):
    eventos[evento].append(funcao)


def emitir_evento(evento, data):
    if evento in eventos:
        for funcao in eventos[evento]:
            funcao(data)


# def setup_eventos() -> None:
#     from eventos.eventos_xur import atualizar_xur
#
#     registrar_evento("atualizar_informacoes_do_xur", atualizar_xur)
