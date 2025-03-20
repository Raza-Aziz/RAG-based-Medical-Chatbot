from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

# Get API keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
os.environ['OPENROUTER_API_KEY'] = OPENROUTER_API_KEY

extracted_data = load_pdf_file("data/")     # Load all the files in the data folder
text_chunks = text_split(extracted_data)    # Split the text into chunks of specific size
embeddings = download_hugging_face_embeddings() # Download the huggingface embedding model

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Giving an index name
index_name = "medicalbot"

# Creating a Pinecone index with code rather than manually by GUI
pc.create_index(
    name=index_name,
    dimension=384,
    metric='cosine',
    spec=ServerlessSpec(
        cloud='aws',
        region='us-east-1'
    )
)

# Get the chunks extracted from documents, convert to vector embeddings and store to Pinecone index
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings
)