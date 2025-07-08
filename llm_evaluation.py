from ctransformers import AutoModelForCausalLM
import json
import nltk
nltk.download("punkt_tab")
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from bert_score import score as bert_score
import numpy as np

#nltk.download('punkt')

# === Load the GGUF Model ===
model = AutoModelForCausalLM.from_pretrained(
    "C:/myworks/MODELS",
    model_file="mistral-7b-instruct-v0.1.Q2_K.gguf",
    model_type="mistral",
    max_new_tokens=200,
    threads=4
)

# === Sample Evaluation Data ===
eval_data = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "Who wrote Romeo and Juliet?", "answer": "William Shakespeare"},
    {"question": "What is the chemical formula of water?", "answer": "H2O"},
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

# === Evaluation Loop ===
for item in eval_data:
    prompt = f"### Question: {item['question']}\n### Answer:"
    prediction = model(prompt).strip()
    reference = item['answer'].strip()

    # Save for batch metrics
    all_preds.append(prediction)
    all_refs.append(reference)

    # === Metrics ===
    exact_match = prediction.lower().strip() == reference.lower().strip()
    bleu = sentence_bleu([nltk.word_tokenize(reference)], nltk.word_tokenize(prediction), smoothing_function=smoothie)
    rouge_l = rouge.score(reference, prediction)['rougeL'].fmeasure
    cosine = cosine_similarity(embedder.encode([reference]), embedder.encode([prediction]))[0][0]

    results.append({
        "question": item["question"],
        "reference": reference,
        "prediction": prediction,
        "exact_match": exact_match,
        "bleu": bleu,
        "rougeL": rouge_l,
        "cosine_similarity": cosine
    })

# === BERTScore (Batch) ===
P, R, F1 = bert_score(all_preds, all_refs, lang="en", rescale_with_baseline=True)

# === Aggregate Metrics ===
aggregate = {
    "exact_match (%)": round(np.mean([r["exact_match"] for r in results]) * 100, 2),
    "bleu (avg)": round(np.mean([r["bleu"] for r in results]), 4),
    "rougeL (avg)": round(np.mean([r["rougeL"] for r in results]), 4),
    "cosine_similarity (avg)": round(np.mean([r["cosine_similarity"] for r in results]), 4),
    "bert_score_f1 (avg)": round(float(F1.mean()), 4)
}
import json

# Safe conversion: convert all NumPy float32 values to Python float
def safe_convert(obj):
    if isinstance(obj, np.float32) or isinstance(obj, np.float64):
        return float(obj)
    if isinstance(obj, np.int32) or isinstance(obj, np.int64):
        return int(obj)
    return str(obj) if not isinstance(obj, (dict, list, str, float, int)) else obj

# === Save to File ===
with open("C:\myworks\AI_Agent_AS_LLM_Judge_Evaluator/llm_eval_full_metrics.txt", "w", encoding="utf-8") as f:
    f.write("=== Detailed Results ===\n")
    json_string = json.dumps(results, indent=2, default=safe_convert)
    f.write(json_string)

    #f.write(json.dumps(results, indent=2))
    f.write("\n\n=== Aggregated Metrics ===\n")
    json_string1= json.dumps(aggregate, indent=2, default=safe_convert)
    f.write(json_string1)
    #f.write(json.dumps(aggregate, indent=2))

print("✅ Evaluation Complete. Summary:")

json_string = json.dumps(aggregate, indent=2, default=safe_convert)

print(json_string)
