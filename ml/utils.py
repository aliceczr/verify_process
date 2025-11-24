
from langchain_groq import ChatGroq 
from config import GROQ_API_KEY
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer
from rag_ingest import load_vector_store
from typing import Any
from functools import lru_cache
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents.stuff import create_stuff_documents_chain


@lru_cache()
def get_embedding_function()-> HuggingFaceEmbeddings:
   model_name="sentence-transformers/all-MiniLM-L6-v2"
   
   return HuggingFaceEmbeddings(model_name=model_name)

@lru_cache()
def get_vector_store() -> Any:
    embeddings= get_embedding_function()
    return load_vector_store(embeddings=embeddings, save_path="vector_store/faiss_index")

@lru_cache()
def get_llm() -> ChatGroq:
    return ChatGroq(api_key=GROQ_API_KEY, model="groq/compound", temperature=0)
@lru_cache()
def get_retriever():
    vector_store = get_vector_store()
    return vector_store.as_retriever()

@lru_cache()
def get_query_prompt() -> PromptTemplate:
     return PromptTemplate(
        input_variables=["context", "input"],
       template = """
            You will act as a legal advisor responsible for classifying a case based exclusively on the documents provided.

            Your objective is:

            1. Carefully read the context/documents.

            2. Identify all relevant information.

            3. Classify the case into one of the three allowed values: "approved", "rejected", or "incomplete".


            
            Mandatory rules:

            - The response must be EXCLUSIVELY the final JSON.

            - The sent JSON must returned exactly the same information sent by the user.

            - All new content must be in Portuguese.

            - The only allowed values ​​for "result" are: "approved", "rejected", "incomplete".

            - The policies must be cited as references in the field "citacoes", ex:[POL-1, POL-2]

            - The cited POLS must be only the ones that confirm the decision.

            - The justification must explain, objectively, why the result was assigned.

            - If any essential document for completion is missing, classify it as "incomplete".
            
            - The JSON must be well formatted and valid.

            - The response must contain only a valid JSON object.

            

            Input:

            - {context}

            - {input}

            The format of the JSON will be like this:

            class Documento(BaseModel):
                id: str
                dataHoraJuntada: datetime
                nome: str
                texto: str


            class Movimento(BaseModel):
                dataHora: datetime
                descricao: str


            class Processo(BaseModel):
                numeroProcesso: str
                classe: str
                orgaoJulgador: str
                ultimaDistribuicao: datetime
                assunto: str
                segredoJustica: bool
                justicaGratuita: bool
                siglaTribunal: str
                esfera: str
                documentos: List[Documento]
                movimentos: List[Movimento]

            4. The output must be a JSON with all the information sent by the user, adding to the JSON the fields of "resultado", "justificativa" and "citacoes" at the end
            """

        )
@lru_cache()
def rag_chain():
    llm = get_llm()
    retriever = get_retriever()

    combine_docs_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=get_query_prompt()
    )

    rag = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=combine_docs_chain
    )

    return rag
