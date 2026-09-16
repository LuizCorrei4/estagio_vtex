from typing import Any, Dict, List, Optional
import re

class PolicyKnowledgeBaseMock:
    """
    Subsistema de RAG para consulta documental às políticas comerciais da loja.
    Modelado a partir dos fragmentos de chunks_big do WeniEval.
    """
    POLICIES_DATABASE: List[Dict[str, Any]] = [
        {
            "id": "POL-ARREPENDIMENTO-01",
            "topic": "devolucao_arrependimento",
            "keywords": ["arrependimento", "devolver", "devolucao", "desistir", "prazo devolver", "7 dias", "cancelamento"],
            "title": "Política de Arrependimento e Devolução (CDC Art. 49)",
            "content": (
                "Conforme o Artigo 49 do Código de Defesa do Consumidor (CDC), o cliente tem até "
                "7 (sete) dias corridos a partir da data de entrega do pedido para solicitar a devolução "
                "por arrependimento. O frete de logística reversa é 100% gratuito por conta da loja parceira VTEX. "
                "O produto deve ser enviado em embalagem original, sem marcas de uso, acompanhado da nota fiscal."
            ),
            "relevance_score": 3,
        },
        {
            "id": "POL-TROCA-MODA-02",
            "topic": "troca_vestuario_calcados",
            "keywords": ["troca", "trocar", "tamanho", "cor", "roupa", "vestuario", "tenis", "calcado", "30 dias"],
            "title": "Política de Troca por Tamanho ou Cor (Vestuário e Calçados)",
            "content": (
                "Para itens de vestuário e calçados, disponibilizamos um prazo estendido de cortesia de até "
                "30 (trinta) dias corridos após o recebimento para troca de numeração, tamanho ou cor. "
                "A primeira troca é inteiramente gratuita com código de autorização de postagem dos Correios. "
                "O item não pode ter sido lavado ou apresentar odores, devendo conter a etiqueta afixada."
            ),
            "relevance_score": 3,
        },
        {
            "id": "POL-GARANTIA-VICIO-03",
            "topic": "defeito_garantia_vicio",
            "keywords": ["defeito", "quebrado", "danificado", "garantia", "vicio", "estragou", "assistencia", "90 dias"],
            "title": "Garantia Legal por Vício ou Defeito de Fabricação (CDC Art. 26)",
            "content": (
                "Para produtos com defeito aparente ou vício de fabricação, o prazo de garantia legal é de "
                "30 (trinta) dias para produtos não duráveis e 90 (noventa) dias para produtos duráveis (eletrônicos, "
                "calçados). O cliente tem direito a reparo em até 30 dias pela assistência técnica autorizada, ou "
                "à substituição do produto ou restituição integral do valor pago."
            ),
            "relevance_score": 3,
        },
        {
            "id": "POL-REEMBOLSO-ESTORNO-04",
            "topic": "estorno_reembolso_financeiro",
            "keywords": ["estorno", "reembolso", "dinheiro", "pix", "cartao", "fatura", "prazo estorno", "pagamento"],
            "title": "Prazos e Métodos de Estorno e Reembolso",
            "content": (
                "O reembolso é processado após a chegada do produto ao centro de distribuição e conclusão da perícia (até 3 dias úteis). "
                "Para compras via PIX ou Boleto, o crédito é realizado via transferência bancária em até 3 dias úteis. "
                "Para pagamentos com Cartão de Crédito, o estorno é solicitado em até 48h, sendo lançado na fatura atual ou subsequente."
            ),
            "relevance_score": 3,
        },
    ]

    @classmethod
    def buscar_politica(cls, query: str) -> Dict[str, Any]:
        query_normalized = re.sub(r"[^\w\s]", " ", query.lower())
        tokens = set(query_normalized.split())

        melhor_politica: Optional[Dict[str, Any]] = None
        maior_pontuacao: int = 0

        for pol in cls.POLICIES_DATABASE:
            pontos = 0
            for kw in pol["keywords"]:
                if kw in query_normalized or any(kw in token for token in tokens):
                    pontos += 2
            if pontos > maior_pontuacao:
                maior_pontuacao = pontos
                melhor_politica = pol

        if not melhor_politica or maior_pontuacao == 0:
            melhor_politica = cls.POLICIES_DATABASE[0]
            score = 1
        else:
            score = min(3, max(2, maior_pontuacao))

        return {
            "policy_id": melhor_politica["id"],
            "topic": melhor_politica["topic"],
            "title": melhor_politica["title"],
            "content": melhor_politica["content"],
            "score": score,
            "source": "VTEX CX Knowledge Base / Store Policies",
        }
