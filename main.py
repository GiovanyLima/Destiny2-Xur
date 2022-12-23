from typing import List

import requests

from aplicacao.api import (
    bungoKey,
    buscar_informacoes_do_xur,
    buscar_informacoes_do_inventario_de_xur,
    buscar_informacoes_dos_itens,
    notificar_no_discord,
)
from entidades.informacao_xur import InformacaoXur
from entidades.item import Item
from entidades.lista_de_ids import ListaDeIds

if __name__ == "__main__":
    with requests.Session() as sessao:
        sessao.headers.update(
            {
                "X-API-Key": bungoKey,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        xur: InformacaoXur = buscar_informacoes_do_xur(sessao=sessao)
        id_dos_itens: ListaDeIds = buscar_informacoes_do_inventario_de_xur(
            sessao=sessao
        )
        itens: List[Item] = buscar_informacoes_dos_itens(
            id_dos_itens=id_dos_itens.ids, sessao=sessao
        )
        xur.adicionar_itens(itens=itens)
        notificar_no_discord(xur=xur, sessao=sessao)
