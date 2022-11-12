from dataclasses import dataclass

from dataclass_type_validator import dataclass_validate

ItemOuNone = ["Item", None]


@dataclass_validate
@dataclass
class Item:
    nome: str = ""
    tipo: str = ""
    tipo_e_raridade: str = ""
    descricao: str = ""
    icone: str = ""
    imagem: str = ""

    def __repr__(self) -> str:
        return f"{self.nome} - {self.tipo} - {self.tipo_e_raridade} - {self.descricao} - {self.icone} - {self.imagem}"

    @staticmethod
    def transformar_em_dataclass(item: dict) -> ItemOuNone:
        if not isinstance(item, dict):
            return None

        informacao_do_item = {
            "nome": item["Response"]["displayProperties"]["name"],
            "descricao": item["Response"]["flavorText"],
            "icone": item["Response"]["displayProperties"]["icon"],
            "tipo_e_raridade": item["Response"]["itemTypeAndTierDisplayName"],
            "imagem": item["Response"]["screenshot"],
            "tipo": "weapon" if item["Response"]["itemType"] == 3 else "armor",
        }

        return Item(**informacao_do_item)
