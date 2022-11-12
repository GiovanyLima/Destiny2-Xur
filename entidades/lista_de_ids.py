from dataclasses import dataclass, field

from dataclass_type_validator import dataclass_validate


@dataclass_validate
@dataclass
class ListaDeIds:

    ids: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"{self.ids}"

    def adicionar_id(self, item_id) -> None:
        if not isinstance(item_id, str):
            item_id = str(item_id)
        self.ids.append(item_id)

    def remover_id(self, item_id) -> None:
        self.ids.remove(item_id)
