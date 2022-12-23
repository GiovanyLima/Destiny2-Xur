from dataclasses import dataclass
from typing import Dict, Self

from dataclass_type_validator import dataclass_validate
from loguru import logger

from const import BUNGO_URI


@dataclass_validate
@dataclass
class Item:
    nome: str = ""
    descricao: str = ""
    icone: str = ""
    tipo_e_raridade: str = ""

    def __repr__(self) -> str:
        return f"{self.nome} - {self.descricao} - {self.tipo_e_raridade} - {self.icone}"

    @staticmethod
    def transformar_em_dataclass(item: Dict) -> Self | None:
        raridade: str = "Exotic"

        if (
            not isinstance(item, Dict)
            or raridade not in item["Response"]["itemTypeAndTierDisplayName"]
        ):
            """
            Validação necessária para filtrar apenas itens exóticos
            por causa do limite no embeddeds webhooks do Discord
            """
            return None

        informacao_do_item: Dict = {
            "nome": item["Response"]["displayProperties"]["name"],
            "descricao": item["Response"]["flavorText"],
            "icone": f'{BUNGO_URI}{item["Response"]["displayProperties"]["icon"]}',
            "tipo_e_raridade": item["Response"]["itemTypeAndTierDisplayName"],
        }
        logger.debug(f"\nItem: {informacao_do_item}")

        return Item(**informacao_do_item)
