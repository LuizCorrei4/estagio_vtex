from typing import Annotated, Any, Dict, List, Optional, TypedDict
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    Esquema de estado compartilhado entre os nós do grafo agêntico VTEX CX.
    """
    messages: Annotated[List[BaseMessage], operator.add]
    user_query: str
    is_toxic: bool
    toxic_reason: Optional[str]
    detected_intent: Optional[str]
    chosen_class_id: Optional[str]
    retrieved_policy: Optional[str]
    tool_action: Optional[str]
    tool_output: Optional[Dict[str, Any]]
    final_response: Optional[str]
    execution_mode: str
