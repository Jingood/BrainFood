from typing import List, Dict
from functools import lru_cache

from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from django.conf import settings

SYSTEM_PROMPT = (

)

@lru_cache(maxsize=1)
def _build_chain() -> ConversationChain:
    llm = ChatOpenAI(
        model='gpt-4o-mini-search-preview',
        temperature=0.7,
        openai_api_key=settings.OPENAI_API_KEY,
        openai_kwargs={
            'tools': [{
                'type': 'web_search_preview',
                'search_context_size': 'low',
            }],
            'tool_choice': {'type': 'web_search_preview'},
        },
    )

    memory = ConversationBufferMemory(return_messages=True)

    return ConversationChain(
        llm=llm,
        memory=memory,
        system_message=SystemMessage(content=SYSTEM_PROMPT),
        verbose=False,
    )

def generate_reply(thread: List[Dict[str, str]]) -> str:
    chain = _build_chain()
    chain.memory.clear()

    for m in thread[-10:]:
        if m['role'] == 'user':
            chain.memort.chat_memory.add_message(HumanMessage(content=m['content']))
        elif m['role'] == 'assistant':
            chain.memory.chat_memory.add_message(AIMessage(content=m['content']))
        else:
            chain.memory.chat_memory.add_message(SystemMessage(content=m['content']))
    
    user_text = thread[-1]['content']
    assistant_text: str = chain.predict(input=user_text)

    return assistant_text