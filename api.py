import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict

from dataclass_type_validator import dataclass_validate
from dotenv import load_dotenv
from requests import Session, Response

from const import (
    API_XUR,
    BASE_URI_BUNGO,
    ID_XUR,
    ITEM_URI,
    NOMES_DOS_LUGARES,
    LUGARES_QUE_XUR_PODE_APARECER,
    CIFRA_E_ENGRAMA,
)
from entidades.informacao_xur import InformacaoXur
from entidades.item import Item
from entidades.lista_de_ids import ListaDeIds

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
bungoKey = os.getenv("API_BUNGIE_KEY")


def buscar_informacoes_do_xur(sessao: Session) -> InformacaoXur | None:
    resposta: Response = sessao.get(API_XUR)
    data: Dict = resposta.json()

    if data:
        return InformacaoXur(
            localizacao={
                "localizacao": LUGARES_QUE_XUR_PODE_APARECER[data["location"]],
                "nome_do_local": NOMES_DOS_LUGARES[data["bubbleName"]],
            }
        )

    return InformacaoXur()


def buscar_informacoes_do_inventario_de_xur(sessao: Session) -> ListaDeIds:
    url: str = f"{BASE_URI_BUNGO}{ID_XUR}"
    resposta: Response = sessao.get(url)
    todos_os_itens = resposta.json()
    todos_os_ids = ListaDeIds()

    if not todos_os_itens:
        return todos_os_ids

    itens_vendidos = todos_os_itens["Response"]["sales"]["data"]["2190858386"][
        "saleItems"
    ]

    for item in itens_vendidos.values():
        id_item = item["itemHash"]
        if id_item in CIFRA_E_ENGRAMA:
            continue
        todos_os_ids.adicionar_id(id_item)

    return todos_os_ids


def buscar_informacoes_dos_itens(id_dos_itens: List, sessao: Session) -> List:
    url_base: str = f"{BASE_URI_BUNGO}{ITEM_URI}"
    informacoes_dos_itens: List = []
    item = Item()

    for id_item in id_dos_itens:
        url: str = f"{url_base}{id_item}"
        resposta: Response = sessao.get(url)
        informacoes_dos_itens.append(
            item.transformar_em_dataclass(item=resposta.json())
        )

    return informacoes_dos_itens
