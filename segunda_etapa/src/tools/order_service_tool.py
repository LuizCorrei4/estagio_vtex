from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

class VTEXOrderServiceMock:
    """
    Mock transacional do Order Management System (OMS) da VTEX.
    """
    ORDERS_DATABASE: Dict[str, Dict[str, Any]] = {
        "VTEX-10492": {
            "order_id": "VTEX-10492",
            "client_name": "Ana Beatriz Ferreira",
            "status": "entregue",
            "delivery_date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "days_since_delivery": 3,
            "carrier": "Total Express",
            "tracking_code": "TEX-99827361BR",
            "items": [{"sku": "SKU-TENIS-001", "name": "Tênis Running Performance Pro", "size": "38", "price": 449.90}],
            "invoice_key": "35260901234567890123550010000104921000104920",
            "invoice_url": "https://invoice.vtexcommerce.com.br/download/VTEX-10492.pdf"
        },
        "VTEX-20381": {
            "order_id": "VTEX-20381",
            "client_name": "Carlos Eduardo Lima",
            "status": "em_transporte",
            "delivery_date": None,
            "days_since_delivery": None,
            "estimated_delivery": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "carrier": "Loggi Express",
            "tracking_code": "LOG-10293847BR",
            "items": [{"sku": "SKU-JAQUETA-002", "name": "Jaqueta Corta-Vento Impermeável", "size": "G", "price": 289.00}],
            "invoice_key": "35260901234567890123550010000203811000203814",
            "invoice_url": "https://invoice.vtexcommerce.com.br/download/VTEX-20381.pdf"
        }
    }

    @classmethod
    def normalizar_order_id(cls, order_id_input: str) -> str:
        limpo = order_id_input.strip().upper().replace("#", "")
        if not limpo.startswith("VTEX-"):
            limpo = f"VTEX-{limpo}"
        return limpo

    @classmethod
    def consultar_pedido(cls, order_id: str) -> Dict[str, Any]:
        id_norm = cls.normalizar_order_id(order_id)
        pedido = cls.ORDERS_DATABASE.get(id_norm)
        if not pedido:
            return {"success": False, "error": "PEDIDO_NAO_ENCONTRADO", "message": f"Pedido {order_id} não localizado."}
        return {"success": True, **pedido}

    @classmethod
    def solicitar_troca(cls, order_id: str, motivo: str) -> Dict[str, Any]:
        consulta = cls.consultar_pedido(order_id)
        if not consulta.get("success"):
            return consulta
        if consulta["status"] != "entregue":
            return {"success": False, "error": "NAO_ENTREGUE", "message": "O pedido ainda não foi entregue."}

        protocolo = f"LOGREV-{datetime.now().strftime('%Y%m%d%H%M')}-{consulta['order_id'].split('-')[-1]}"
        codigo_postagem = f"POST-BR-{datetime.now().strftime('%H%M%S')}"
        return {
            "success": True,
            "action": "SOLICITACAO_TROCA_APROVADA",
            "protocol": protocolo,
            "order_id": consulta["order_id"],
            "return_postage_code": codigo_postagem,
            "carrier": "Correios (Logística Reversa Express)",
            "deadline_postage_days": 7
        }

    @classmethod
    def emitir_segunda_via_nf(cls, order_id: str) -> Dict[str, Any]:
        id_norm = cls.normalizar_order_id(order_id)
        pedido = cls.ORDERS_DATABASE.get(id_norm)
        if not pedido:
            return {"success": False, "error": "PEDIDO_NAO_ENCONTRADO"}
        return {
            "success": True,
            "order_id": pedido["order_id"],
            "invoice_key": pedido["invoice_key"],
            "download_url": pedido["invoice_url"]
        }
