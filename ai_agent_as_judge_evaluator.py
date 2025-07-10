from ctransformers import AutoModelForCausalLM
import json
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from bert_score import score as bert_score
import numpy as np
import os

nltk.download("punkt")

# === Load the GGUF Judge Model ===
model = AutoModelForCausalLM.from_pretrained(
    "C:/myworks/MODELS",
    model_file="mistral-7b-instruct-v0.1.Q2_K.gguf",
    model_type="mistral",
    max_new_tokens=200,
    threads=4
)

# === Sample Evaluation Data ===
eval_data = [

 {"question": "What is the capital of Australia?", "answer": "Canberra"},
  {"question": "Who discovered penicillin?", "answer": "Alexander Fleming"},
  {"question": "What is the boiling point of water in Celsius?", "answer": "100°C"},
  {"question": "When did World War II end?", "answer": "1945"},
  {"question": "What is the chemical symbol for gold?", "answer": "Au"},
  {"question": "Who wrote 'To Kill a Mockingbird'?", "answer": "Harper Lee"},
  {"question": "What planet is known as the Red Planet?", "answer": "Mars"},
  {"question": "What is the largest mammal on Earth?", "answer": "Blue whale"},
  {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"},
  {"question": "What is the square root of 144?", "answer": "12"}

]

# === Embedding Model for Cosine Similarity ===
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# === ROUGE & BLEU Settings ===
rouge = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
smoothie = SmoothingFunction().method4

# === Store Results ===
results = []
all_preds = []
all_refs = []

# === Agent Prompt Template ===
def format_agent_prompt(question, reference, prediction):
    return f"""
You are an expert AI feedback evaluator. Your job is to judge the quality of a model-generated answer to a question, based on a reference answer.

Follow these steps:
1. Understand the question intent.
2. Compare the reference answer with the prediction.
3. Identify factual correctness, completeness, and clarity.
4. Give a score from 1 (poor) to 5 (excellent).
5. Explain your reasoning.

### Question:
{question}

### Reference Answer:
{reference}

### Model Prediction:
{prediction}

Now, respond in the format:
Score: <1-5>
Explanation: <your reasoning>
"""

# === Evaluation Loop ===
for item in eval_data:
    question = item['question']
    reference = item['answer'].strip()
    prompt = f"### Question: {question}\n### Answer:"
    
    # === Prediction by Model ===
    prediction = model(prompt).strip()
    
    # Save for batch metrics
    all_preds.append(prediction)
    all_refs.append(reference)

    # === Metrics ===
    exact_match = prediction.lower().strip() == reference.lower().strip()
    bleu = sentence_bleu([nltk.word_tokenize(reference)], nltk.word_tokenize(prediction), smoothing_function=smoothie)
    rouge_l = rouge.score(reference, prediction)['rougeL'].fmeasure
    cosine = cosine_similarity(embedder.encode([reference]), embedder.encode([prediction]))[0][0]

    # === AI Judge Agent ===
    judge_prompt = format_agent_prompt(question, reference, prediction)
    judge_output = model(judge_prompt).strip()

    # Extract Score from judge_output
    def extract_score(text):
        for line in text.split("\n"):
            if "score" in line.lower():
                digits = ''.join(filter(str.isdigit, line))
                return int(digits) if digits else None
        return None

    agent_score = extract_score(judge_output)

    results.append({
        "question": question,
        "reference": reference,
        "prediction": prediction,
        "exact_match": exact_match,
        "bleu": bleu,
        "rougeL": rouge_l,
        "cosine_similarity": cosine,
        "agent_score": agent_score,
        "agent_feedback": judge_output
    })

# === BERTScore (Batch) ===
P, R, F1 = bert_score(all_preds, all_refs, lang="en", rescale_with_baseline=True)
for i in range(len(results)):
    results[i]["bert_score_f1"] = float(F1[i])

# === Aggregated Metrics ===
aggregate = {
    "exact_match (%)": round(np.mean([r["exact_match"] for r in results]) * 100, 2),
    "bleu (avg)": round(np.mean([r["bleu"] for r in results]), 4),
    "rougeL (avg)": round(np.mean([r["rougeL"] for r in results]), 4),
    "cosine_similarity (avg)": round(np.mean([r["cosine_similarity"] for r in results]), 4),
    "bert_score_f1 (avg)": round(float(F1.mean()), 4),
    "agent_score (avg)": round(np.mean([r["agent_score"] for r in results if r["agent_score"] is not None]), 2)
}

# === JSON Safe Conversion ===
def safe_convert(obj):
    if isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    if isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    return str(obj) if not isinstance(obj, (dict, list, str, float, int)) else obj

# === Save Results to File ===
output_file = "C:/myworks/AI_Agent_AS_LLM_Judge_Evaluator/ai_agent_eval_factual_reasoning.txt"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    f.write("=== Detailed Evaluation Results ===\n\n")
    json_string = json.dumps(results, indent=2, default=safe_convert)
    f.write(json_string)
    f.write("\n\n=== Aggregated Metrics ===\n")
    json_string1 = json.dumps(aggregate, indent=2, default=safe_convert)
    f.write(json_string1)

# === Print Summary ===
print("✅ Evaluation Complete. Summary:")
print(json.dumps(aggregate, indent=2, default=safe_convert))
