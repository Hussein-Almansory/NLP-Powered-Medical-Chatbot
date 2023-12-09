from nltk.translate.bleu_score import sentence_bleu
import Levenshtein

# Reference sentence
reference = ["If blood pressure measured in the clinic is 140/90 mmHg or higher: Take a second measurement during the consultation. If the second measurement is substantially different from the first, take a third measurement. Record the lower of the last two measurements as the clinic blood pressure."]


# Here Put the Genertaed text from the models 
generated_by_ChatOpenAI = ""
generated_by_Flan_T5_SMALL = ""

# Tokenize the actual and generated texts
actual_tokens = [word.lower() for word in reference[0].split()]
generated_tokens1 = [word.lower() for word in generated_by_ChatOpenAI.split()]
generated_tokens2 = [word.lower() for word in generated_by_Flan_T5_SMALL.split()]

# Compute BLEU scores
bleu_score1 = sentence_bleu([actual_tokens], generated_tokens1)
bleu_score2 = sentence_bleu([actual_tokens], generated_tokens2)

# Calculate Levenshtein distances
distance1 = Levenshtein.distance(reference[0], generated_by_ChatOpenAI)
distance2 = Levenshtein.distance(reference[0], generated_by_Flan_T5_SMALL)

# Calculate similarity percentages
similarity_percentage1 = 100 - (distance1 / max(len(reference[0]), len(generated_by_ChatOpenAI))) * 100
similarity_percentage2 = 100 - (distance2 / max(len(reference[0]), len(generated_by_Flan_T5_SMALL))) * 100

# Display results
print("Metrics for generated_by_ChatOpenAI:")
print(f"BLEU Score: {bleu_score1:.2f}")
print(f"Levenshtein Distance: {distance1}")
print(f"Similarity Percentage: {similarity_percentage1:.2f}%\n")

print("Metrics for generated_b:")
print(f"BLEU Score: {bleu_score2:.2f}")
print(f"Levenshtein Distance: {distance2}")
print(f"Similarity Percentage: {similarity_percentage2:.2f}%")
