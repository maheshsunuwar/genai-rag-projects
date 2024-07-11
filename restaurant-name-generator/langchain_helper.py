import os
import pandas as pd
import numpy as np

# import streamlit as st
#langchain imports
from langchain_core.output_parsers import StrOutputParser
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

llm = Ollama(
    model='llama3',
    keep_alive='3h',
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler])
)

def generate_restaurant_name_and_items(cuisine):
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template='I want to open a restaurant for {cuisine} food. Suggest me a fancy name for it,just one. Just the name and nothing else'
        )
    name_chain = prompt_template_name | llm
    
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest some 10 menu items for {restaurant_name}. Return the menu items as comma separated values and nothing else."
    )

    items_chain = prompt_template_items | llm | StrOutputParser()

    # Combine the chains
    combined_chain = RunnableParallel(
        {
            "restaurant_name": name_chain,
            "cuisine": RunnablePassthrough(),
        }
    ).assign(
        menu_items=lambda x: items_chain.invoke(x)
    )
    
    # Run the combined chain
    input_data = {"cuisine": cuisine}
    result = combined_chain.invoke(input_data)
    
    return {
        'restaurant_name': result['restaurant_name'],
        'menu_items': result['menu_items']
    }