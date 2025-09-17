# text -> separate into lines -> upsert into Pinecone (vector database) -> give the most similar lines to AI -> AI reply as a human

# separating text into lines

# input - path
# output - records dictionary

path = "/Users/eugene/Desktop/ChatBot Project/chatbot/PUBG Rules.txt"
   
def separate_liens(path):
    with open(path, encoding="utf-8") as f:
     raw = f.read()

    # split on blank lines into non-empty paragraphs
    paragraphs = [p.strip() for p in raw.split("\n\n") if p.strip()]

    # Build records for upsert
    records = []
    for i, para in enumerate(paragraphs, start=1):
     records.append({
            "_id": f"rec{i}",
           "chunk_text": para,
      })

    return(records)

print(separate_liens(path))