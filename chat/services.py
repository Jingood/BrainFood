from typing import List, Dict
from functools import lru_cache

from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from django.conf import settings

SYSTEM_PROMPT = settings.SYSTEM_PROMPT

@lru_cache(maxsize=1)
def _build_chain() -> ConversationChain:
    llm = ChatOpenAI(
        model='gpt-3.5-turbo',
        temperature=0.7,
        openai_api_key=settings.OPENAI_API_KEY,
    )

    memory = ConversationBufferMemory(return_messages=True)
    chain = ConversationChain(llm=llm, memory=memory, verbose=False)
    return chain

def generate_reply(thread: List[Dict[str, str]]) -> str:
    chain = _build_chain()
    chain.memory.clear()

    chain.memory.chat_memory.add_message(SystemMessage(content=SYSTEM_PROMPT))

    for m in thread[-10:]:
        if m['role'] == 'user':
            chain.memory.chat_memory.add_message(HumanMessage(content=m['content']))
        elif m['role'] == 'assistant':
            chain.memory.chat_memory.add_message(AIMessage(content=m['content']))
        else:
            chain.memory.chat_memory.add_message(SystemMessage(content=m['content']))
    
    user_text = thread[-1]['content']
    assistant_text: str = chain.predict(input=user_text)

    return assistant_text