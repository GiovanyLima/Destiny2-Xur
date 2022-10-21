import os
from pathlib import Path
from typing import List, Dict

import requests
from dotenv import load_dotenv
from requests import Session, Response

from const import API_XUR, BASE_URI_BUNGO, ID_XUR, ITEM_URI

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
bungoKey = os.getenv("API_BUNGIE_KEY")

requisicao: Session = requests.Session()
requisicao.headers.update({"x-api-key": bungoKey})


def buscar_informacoes_do_xur() -> Dict | None:
    """Busca informações do Xur."""
    resposta: Response = requisicao.get(API_XUR)
    data: None | Dict = resposta.json()
    if data:
        localizacao: Dict = {
            "planeta": data["placeName"],
            "local": data["locationName"],
        }
        return localizacao
    return None


def buscar_informacoes_do_inventario_de_xur() -> Dict | None:
    """Busca os códigos dos os itens vendidos pelo Xur."""
    url: str = f"{BASE_URI_BUNGO}{ID_XUR}"
    resposta: Response = requisicao.get(url)
    return resposta.json()


def buscar_informacoes_dos_itens(codigos_dos_itens) -> List:
    """Busca informações dos itens."""
    url_base: str = f"{BASE_URI_BUNGO}{ITEM_URI}"
    informacoes_dos_itens: List = []
    for codigo in codigos_dos_itens:
        url: str = f"{url_base}{str(codigo)}"
        resposta: Response = requisicao.get(url)
        informacoes_dos_itens.append(resposta.json())
    return informacoes_dos_itens


def parsear_informacoes_dos_itens(informacoes_dos_itens) -> List[Dict]:
    """Parseia as informações dos itens."""
    itens: List = []
    for item in informacoes_dos_itens:
        info_itens: Dict = {
            "name": item["Response"]["displayProperties"]["name"],
            "flavor": item["Response"]["flavorText"],
            "icon": item["Response"]["displayProperties"]["icon"],
            "typeAndTier": item["Response"]["itemTypeAndTierDisplayName"],
            "screenshot": item["Response"]["screenshot"],
            "type": "weapon" if item["Response"]["itemType"] == 3 else "armor",
        }
        itens.append(info_itens)
    return itens
