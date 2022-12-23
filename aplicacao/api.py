import os
from pathlib import Path
from typing import Dict, List
from urllib.parse import quote_plus

from dotenv import load_dotenv
from loguru import logger
from requests import Session, Response

from const import (
	API_XUR,
	BASE_URI_BUNGO,
	ID_XUR,
	ITEM_URI,
	NOMES_DOS_LUGARES,
	LUGARES_QUE_XUR_PODE_APARECER,
	CIFRA_E_ENGRAMA,
	LIGHTGG_URI,
	AVATAR_DO_XUR,
	COR_PARA_ENVIAR_NO_DISCORD,
)
from entidades.informacao_xur import InformacaoXur
from entidades.item import Item
from entidades.lista_de_ids import ListaDeIds
from log.logs import setup_logging

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
bungoKey = os.getenv("API_BUNGIE_KEY")
discordWebhookUrl = os.getenv("DISCORD_WEBHOOK_URL")
setup_logging()


@logger.catch
def buscar_informacoes_do_xur(sessao: Session) -> InformacaoXur | None:
	resposta: Response = sessao.get(API_XUR)
	data: Dict = resposta.json()

	if not data:
		logger.error(
			f"Não foi possível buscar as informações do Xur \nCodigo -> {resposta.status_code} \nResposta -> {resposta.json()}"
		)
		return InformacaoXur()

	logger.success("Informações do Xur obtidas com sucesso!")
	return InformacaoXur(
		localizacao={
			"localizacao": LUGARES_QUE_XUR_PODE_APARECER[data["location"]],
			"nome_do_local": NOMES_DOS_LUGARES[data["bubbleName"]],
		}
	)


@logger.catch
def buscar_informacoes_do_inventario_de_xur(sessao: Session) -> ListaDeIds:
	url: str = f"{BASE_URI_BUNGO}{ID_XUR}"
	resposta: Response = sessao.get(url)
	todos_os_itens: Dict = resposta.json()
	todos_os_ids: ListaDeIds = ListaDeIds()

	if not todos_os_itens:
		logger.error(
			f"Não foi possível buscar as informações do inventário do Xur"
			f"\nCodigo -> {resposta.status_code} \nResposta -> {resposta.json()}"
		)
		return todos_os_ids

	itens_vendidos: Dict = todos_os_itens["Response"]["sales"]["data"]["2190858386"][
		"saleItems"
	]

	for item in itens_vendidos.values():
		id_item: int = item["itemHash"]
		if id_item in CIFRA_E_ENGRAMA:
			continue
		todos_os_ids.adicionar_id(id_item)

	logger.success("Informações do inventário do Xur obtidas com sucesso!")
	return todos_os_ids


@logger.catch
def buscar_informacoes_dos_itens(
	id_dos_itens: List[str], sessao: Session
) -> List[Item]:
	url_base: str = f"{BASE_URI_BUNGO}{ITEM_URI}"
	informacoes_dos_itens: List = []

	for id_item in id_dos_itens:
		url: str = f"{url_base}{id_item}"
		resposta: Response = sessao.get(url)
		logger.info(f"Buscando informações do item {id_item}")
		item_validado = Item.transformar_em_dataclass(resposta.json())
		informacoes_dos_itens.append(item_validado) if item_validado else None
	return informacoes_dos_itens


@logger.catch
def notificar_no_discord(xur: InformacaoXur, sessao: Session) -> None:
	lista_de_embeddeds: List[Dict] = []
	for item in xur.itens:
		logger.info(f"Buscando informações do item {item.nome}")
		pesquisa: str = f"{LIGHTGG_URI}?q={quote_plus(item.nome)}"
		embedded_do_discord: Dict = {
			"author": {
				"name": item.tipo_e_raridade,
				"url": pesquisa,
				"icon_url": item.icone,
			},
			"title": item.nome,
			"url": pesquisa,
			"description": item.descricao,
			"color": COR_PARA_ENVIAR_NO_DISCORD,
			"thumbnail": {"url": item.icone},
		}
		lista_de_embeddeds.append(embedded_do_discord)
		logger.success(f"Informações do item {item.nome} obtidas com sucesso!")

	json: Dict = {
		"username": "Xur, Agente dos Noves",
		"avatar_url": AVATAR_DO_XUR,
		"embeds": lista_de_embeddeds,
	}

	sessao.post(discordWebhookUrl, json=json)
	logger.success("Notificação para o Discord enviada com sucesso!")
