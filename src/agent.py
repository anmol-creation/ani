import os
from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Configuration
VECTOR_DB_DIR = "./data/vector_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
# Default to a lightweight model, user can change this
LLM_MODEL_NAME = "qwen2.5:1.5b"

class ACAgent:
    def __init__(self):
        print(f"🤖 Initializing .ac Agent with model: {LLM_MODEL_NAME}")
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

        # Load Vector DB
        if os.path.exists(VECTOR_DB_DIR) and os.listdir(VECTOR_DB_DIR):
            self.vector_db = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=self.embeddings)
            self.retriever = self.vector_db.as_retriever(search_kwargs={"k": 3})
            self.has_knowledge = True
        else:
            self.has_knowledge = False
            self.retriever = None

        # Initialize LLM via local Ollama instance
        try:
             self.llm = Ollama(model=LLM_MODEL_NAME)
        except Exception as e:
            print(f"⚠️ Error connecting to Ollama: {e}. Is Ollama running?")
            self.llm = None

        # Setup custom prompt to make the AI aware of its role
        prompt_template = """
You are the central intelligence of the '.ac' ecosystem, a personalized AI assistant.
You have access to the user's local projects and knowledge base.
You understand both Hindi and English.
Always be helpful, precise, and prioritize the user's private data context if relevant.

Context from knowledge base:
{context}

Question: {question}

Helpful Answer:"""
        self.PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        if self.has_knowledge and self.llm:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": self.PROMPT}
            )
        else:
            self.qa_chain = None

    def ask(self, query: str) -> dict:
        if not self.llm:
             return {"answer": "Error: Cannot connect to local LLM (Ollama). Please ensure it is running.", "sources": []}

        if not self.has_knowledge or not self.qa_chain:
            # Fallback to direct LLM query if no local knowledge base exists yet
            response = self.llm.invoke(query)
            return {"answer": response, "sources": ["Direct LLM (No local context found)"]}

        # Query using RAG
        result = self.qa_chain.invoke({"query": query})

        sources = []
        if 'source_documents' in result:
             for doc in result['source_documents']:
                  source_file = doc.metadata.get('source', 'Unknown source')
                  if source_file not in sources:
                       sources.append(source_file)

        return {
            "answer": result.get("result", ""),
            "sources": sources
        }

# For manual testing
if __name__ == "__main__":
    agent = ACAgent()
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        response = agent.ask(user_input)
        print(f"\n.ac Agent: {response['answer']}")
        if response['sources']:
             print(f"\n(Sources: {', '.join(response['sources'])})")
