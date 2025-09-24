from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
from separate_line import separate_lines

# Initialize Pinecone with your API key
load_dotenv()
pc = Pinecone(api_key = os.getenv("PINECONE_API_KEY"))
document = "/Users/eugene/Desktop/ChatBot Project/chatbot/PUBG Rules.txt"

def search(query):
    """
    input: query
    output: top 3 search results in a list
    """
    # Create a serverless index for semantic search and reranking
    index_name = "pubg-rules"

    # embedding model: llama-text-embed-v2 -> converting text to vector
    if not pc.has_index(index_name):
        pc.create_index_for_model(
            name = index_name,
            cloud = "aws",
            region = "us-east-1",
            embed = {
                "model": "llama-text-embed-v2",
                "field_map": {"text": "chunk_text"}
            }
        )

    # Create and connect to the index (vector memory space)
    index = pc.Index(index_name)
    records = separate_lines(document)
    index.upsert_records("pubg", records)

    # print("Index:", index.describe_index_stats())

    # ### Semantic Search ###
    # # query = "type of healing items"

    # results = index.search(
    #     namespace = "pubg",
    #     query = {
    #         "top_k": 5, # k-nearest neighbors
    #         "inputs": {
    #             'text': query
    #         }
    #     }
    # )

    # print("Semantic Search:", results)

    # Reranking
    reranked_results = index.search(
        namespace = "pubg",
        query = {
            "top_k": 5,
            "inputs": {
                'text': query
            }
        },
        rerank = { # optimization
            "model": "bge-reranker-v2-m3",
            "top_n": 5,
            "rank_fields": ["chunk_text"]
        },
        fields = ["category", "chunk_text"]
    )

    # print("Rerank:" , reranked_results)

    top3 = []
    for i in range(3):
        top = reranked_results["result"]["hits"][i]["fields"]["chunk_text"]
        top3.append(top)
    
    return top3

print(search("number of players in a match"))