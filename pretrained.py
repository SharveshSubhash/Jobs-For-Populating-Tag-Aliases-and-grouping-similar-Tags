from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
def parse_phrases_to_list(input_file):
    phrases_list = []
    with open(input_file, 'r') as f:
        for line in f:
            phrase = line.strip()
            if phrase:  
                phrases_list.append(phrase)
    return phrases_list

input_file = 'Filtered_Phrases.txt'  
phrases = parse_phrases_to_list(input_file)
embeddings = model.encode(phrases, convert_to_tensor=True)

similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)


threshold = 0.6  

grouped_phrases = {}
for i, phrase in enumerate(phrases):
    similar_phrases = []
    for j in range(len(phrases)):
        if i != j and similarity_matrix[i][j] > threshold:
            similar_phrases.append(phrases[j])

    grouped_phrases[phrase] = similar_phrases

output_file = "Grouped_Output_bert0.6.txt"

with open(output_file, 'w') as f_out:
    for key, phrase in grouped_phrases.items():
        f_out.write(f"{key}: {phrase}" + '\n')
print("Grouped Tags:")

for key, value in grouped_phrases.items():
    print(f"{key}: {value}")
