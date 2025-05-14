import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.chains import LLMChain
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
import gradio as gr
import torch
from src.templates import load_template

# load api keys from environment
load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")

# load the HuggingFace Embeddings on GPU
if torch.backends.mps.is_available():
    device = 'mps'
elif torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs = {'device': device})

# Load the pre-saved Chroma vector store with the recipes
vector_store = Chroma(
    collection_name="Recipes",  # Change to your actual collection name
    embedding_function=embeddings,
    persist_directory="data/recipes-vector-store")

# create a retriever object that looks for the top 15 matches
retriever = vector_store.as_retriever(search_kwargs={"k": 15})

# Load the LLM model
llm = ChatAnthropic(model_name = "claude-3-haiku-20240307" , anthropic_api_key=anthropic_api_key)

# Create a memory object to store the conversation history, also specifies that user text has the key "text", so that it is distinguishable from the knowledge base
memory = ConversationBufferMemory(memory_key="history",input_key="text", return_messages=True)
# same, but a summary of the conversation for the query rewriting to send to the retriever
summary_memory = ConversationSummaryBufferMemory(llm=llm,input_key="query", memory_key="summary_history", return_messages=True)

# Load the templates and initialize the prompt objects
rewrite_prompt_text = load_template("rewrite_prompt.txt")
chat_prompt_text = load_template("chat_prompt.txt")

rewrite_prompt = PromptTemplate(input_variables=["query"], template=rewrite_prompt_text)
prompt_template = PromptTemplate(input_variables=["text", "kb"], template = chat_prompt_text)

# Create the chat and query-retrieval rewrite chains
chat_chain = LLMChain(llm=llm,prompt=prompt_template,memory=memory)
rewrite_chain = LLMChain(llm=llm,prompt=rewrite_prompt,memory=summary_memory)

# Chatbot function
def chat_gradio(user_input, gradio_history):
    # use the rewrite chain to formulate the user input into a query for the retriever that accounts for the conversation history
    rewrite_response = rewrite_chain.invoke({"query":user_input})
    # only use the knowledge base if the llm model says it is needed
    if rewrite_response['text'] != "RetrieverNotNeeded":
        # retrieve the top 15 documents
        docs = retriever.invoke(rewrite_response['text'])
        kb = "\n".join([doc.page_content for doc in docs])
    else:
        kb = ""
    # the llm uses the conversation history and the knowledge base to generate a response
    response = chat_chain.invoke({"text":user_input, "kb":kb})
    yield response['text']

# chatbot interface logic
chatbot = gr.ChatInterface(chat_gradio, textbox=gr.Textbox(placeholder="Ask me for a recipe...",
container=False,
autoscroll=True,
scale=7),
)

if __name__ == "__main__":
    chatbot.launch()