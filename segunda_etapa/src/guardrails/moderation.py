from typing import Optional, Tuple
import re
import unicodedata

class ModerationGuardrail:
    """
    Guardrail determinístico de contenção de toxicidade e ofensas (S1).
    """
    TOXIC_PATTERNS = [
        r"\bmerda\b", r"\blixo\b", r"\bporcaria\b", r"\bbosta\b",
        r"\bidiota\b", r"\bburr[oa]s?\b", r"\bincompetente\b",
        r"\bv[aá] se foder\b", r"\bfdp\b", r"\bcaralh[oa]\b"
    ]
    COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in TOXIC_PATTERNS]

    @classmethod
    def normalizar_texto(cls, texto: str) -> str:
        nfkd = unicodedata.normalize("NFKD", texto)
        return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()

    @classmethod
    def verificar_toxicidade(cls, query: str) -> Tuple[bool, Optional[str]]:
        texto_norm = cls.normalizar_texto(query)
        for regex in cls.COMPILED_PATTERNS:
            if regex.search(texto_norm) or regex.search(query):
                return True, "Linguagem hostil detectada (Violação de Segurança S1)"
        return False, None

    @classmethod
    def gerar_resposta_moderacao(cls) -> str:
        return (
            "Compreendemos a sua insatisfação e lamentamos qualquer inconveniente ocorrido. "
            "Contudo, para mantermos um ambiente construtivo, solicitamos a gentileza de prosseguirmos "
            "o atendimento de forma respeitosa. Por favor, compartilhe o número do seu pedido ou detalhe "
            "sua dúvida operacional para que possamos auxiliá-lo prontamente."
        )

class IntentRouter:
    """
    Roteador semântico de escopo e categorização de intenções (N1, P1, A1).
    """
    OUT_OF_SCOPE_KEYWORDS = [
        "fundou", "fundador", "amazon", "mercado livre", "capital da", "presidente",
        "receita de", "fazer bolo", "cotação do dolar", "bitcoin", "clima amanhã"
    ]
    TRANSACTIONAL_KEYWORDS = [
        "vtex-", "pedido", "rastreio", "rastrear", "onde esta", "trocar meu pedido",
        "solicitar troca", "nota fiscal", "segunda via"
    ]

    @classmethod
    def classificar_intencao(cls, query: str, is_toxic: bool) -> Tuple[str, str]:
        if is_toxic:
            return "refusal_toxic_behavior", "S1"
        query_lower = query.lower()
        if any(kw in query_lower for kw in cls.OUT_OF_SCOPE_KEYWORDS):
            return "refusal_input", "N1"
        if any(kw in query_lower for kw in cls.TRANSACTIONAL_KEYWORDS) or re.search(r"\b\d{5}\b", query_lower):
            return "classification", "A1"
        return "text_generation", "P1"

    @classmethod
    def gerar_resposta_fora_escopo(cls) -> str:
        return (
            "Sou o assistente virtual da VTEX CX Platform especializado exclusivamente no suporte "
            "às operações desta loja (consultas de pedidos, políticas de troca, devoluções, prazos e reembolsos). "
            "Não possuo informações sobre temas externos ou de conhecimentos gerais. "
            "Como posso auxiliá-lo em relação às suas compras ou pedidos?"
        )
