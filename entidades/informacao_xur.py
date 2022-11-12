from dataclasses import dataclass, field
from typing import List

from dataclass_type_validator import dataclass_validate

from entidades.item import Item


@dataclass_validate
@dataclass
class InformacaoXur:
    localizacao: dict = field(
        default_factory=lambda: {
            "localizacao": "Sem localização",
            "nome_do_local": "Sem nome do local",
        }
    )
    itens: List[Item] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"{self.localizacao} - {self.itens}"

    def adicionar_itens(self, itens: List[Item]) -> None:
        if not isinstance(itens, list):
            return None

        self.itens.extend(itens)
