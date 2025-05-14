# Recipe Chatbot

This project is an AI-powered chatbot that helps users find and generate cooking recipes based on their preferences. The chatbot leverages a retrieval-augmented generation (RAG) pipeline using a vector database and an LLM to provide relevant recipe suggestions. The project is built with LangChain, Gradio, and ChromaDB, using the RecipeNLG dataset as the primary knowledge base.

## Features
- Uses [Claude 3 Haiku](https://www.anthropic.com/) for natural language understanding and response generation.
- Retrieves relevant recipes from a Chroma vector database using `sentence-transformers/all-MiniLM-L6-v2` embeddings.
- Reformulates user queries for more context aware retrieval using a query rewriter.
- Stores conversation history to provide more robust responses.
- The chatbot draws from the knowledge base to suggest recipes, but can also use its original training data to look for recipes when prompted to do so.
- Provides a basic interactive chat interface using Gradio.

## Dataset: RecipeNLG
This project uses the [RecipeNLG](https://www.aclweb.org/anthology/2020.inlg-1.4) dataset for retrieval-based recipe recommendations. The dataset is a collection of structured cooking recipes designed for text generation tasks.

### Citation
If you use this project or the dataset, please cite RecipeNLG as follows:
```bibtex
@inproceedings{bien-etal-2020-recipenlg,
title = "{R}ecipe{NLG}: A Cooking Recipes Dataset for Semi-Structured Text Generation",
author = "Bie{\'n}, Micha{\l}  and
  Gilski, Micha{\l}  and
  Maciejewska, Martyna  and
  Taisner, Wojciech  and
  Wisniewski, Dawid  and
  Lawrynowicz, Agnieszka",
booktitle = "Proceedings of the 13th International Conference on Natural Language Generation",
month = dec,
year = "2020",
address = "Dublin, Ireland",
publisher = "Association for Computational Linguistics",
url = "https://www.aclweb.org/anthology/2020.inlg-1.4",
pages = "22--28"
}
```

**Credit:**
> The RecipeNLG dataset is published by researchers from Stanford NLP. If you use this project, please ensure that you acknowledge their work appropriately.

## Installation and Setup

two setup files are included that setup the virtual environment and install requirements. One file is for Windows and the other for Linux/MacOS. To run the files, use
```bash
.\setup.bat
```
on Windows, and 
```bash
chmod +x setup.sh
./setup.sh
```
For linux and MacOS.

After the setup, activate the recipes_venv virtual environment.

### Setting Up API Keys
This project requires API keys for Anthropic's Claude model and LangSmith (optional, for tracking API calls). Create a `.env` file in the root directory:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
```
### Running the vector-store generation
Download the RecipeNLG dataset and insert it into the project this way:
```
📂 recipe-chatbot
├── 📂 data
│   ├── 📂 raw-KB  # ChromaDB storage for recipes
        ├── RecipeNLG.csv
```
Then, launch the script that generates the vector store this way:
```bash
python -m src.retriever
```

### Running the Chatbot
```bash
python -m src.chatbot
```
This will launch a Gradio web interface where you can interact with the chatbot.

