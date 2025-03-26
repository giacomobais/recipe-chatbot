from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
from langchain_core.documents import Document
import pandas as pd

# load the HuuggingFace Embeddings on GPU
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs = {'device': 'cuda'})

# Load the df
data_path = "data/raw-KB/RecipeNLG.csv"
df = pd.read_csv(data_path)

# extract the first 40000 recipes
recipes = []
for i, row in enumerate(df.iterrows()):
    if i < 1:
        recipe = {"title": row[1]['title'], "ingredients": row[1]['ingredients'], "directions": row[1]['directions']}
        recipes.append(recipe)
    else:
        break

# create structured text for each recipe
text_recipes = []
for recipe in recipes:
    tmp_recipe = ""
    for section in ["Title", "Ingredients", "Directions"]:
        text = recipe[section.lower()]
        # remove all square brackets and "
        tmp_recipe += f"{section}:\n {recipe[section.lower()]}\n"
    text_recipes.append(tmp_recipe)

# initialize Chromadb vector store
vector_store = Chroma(
    collection_name="Recipes",
    embedding_function=embeddings,
    persist_directory="data/recipes-vector-store",
)

# create a langchain Document for each recipe
documents = []
for i, recipe in enumerate(text_recipes):
    document = Document(page_content=recipe, metadata={"id": str(i)}, id = i)
    documents.append(document)

# create unique ids for each document
uuids = [str(uuid4()) for _ in range(len(documents))]

# add the documents to the vector store
vector_store.add_documents(documents, ids = uuids)