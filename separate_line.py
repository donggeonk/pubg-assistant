# text -> separate into lines -> upsert into Pinecone (vector database) -> give the most similar lines to AI -> AI reply as a human
# separating text into lines
import re

#path = "/Users/eugene/Desktop/ChatBot Project/chatbot/PUBG Rules.txt"

# input = path to the pubg file
# output = formatted records for Pinecone upsert
def separate_lines(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    # split into sentences on terminal punctuation (. ! ?) followed by whitespace
    # keeps the punctuation at the end of each sentence
    pieces = [piece.strip() for piece in re.split(r'(?<=[.!?])\s+', raw) if piece.strip()]

    records = []
    for i, piece in enumerate(pieces, start=1):
        records.append({
            "_id": f"rec{i}",
            "chunk_text": piece,
        })
    
    return records


#records = separate_lines(path)
#print(len(records), records)