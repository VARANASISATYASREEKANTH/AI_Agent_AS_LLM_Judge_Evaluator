import os
import json
import nltk
import numpy as np
import matplotlib.pyplot as plt

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from bert_score import score as bert_score
from ctransformers import AutoModelForCausalLM

nltk.download("punkt")

# === Load Multiple GGUF Models as Judges ===
judge_models = {
    "Mistral": AutoModelForCausalLM.from_pretrained(
        "C:/myworks/MODELS", model_file="mistral-7b-instruct-v0.1.Q2_K.gguf",
        model_type="mistral", max_new_tokens=200, threads=4
    ),
    # Add more agents below like LLaMA, Phi, etc.
    # "LLaMA": AutoModelForCausalLM.from_pretrained(...),
}

# === Evaluation Data ===
eval_data = [
 {"question": "What is 48 divided by 6?", "answer": "8"},
  {"question": "A car travels 60 km in 30 minutes. Speed in km/h?", "answer": "120 km/h"},
  {"question": "What is 15% of 200?", "answer": "30"},
  {"question": "Solve for x: 2x+3=11", "answer": "4"},
  {"question": "What is 7 factorial?", "answer": "5040"},
  {"question": "Solve: √81 + √16", "answer": "13"},
  {"question": "If x=3, find 2x²+1", "answer": "19"},
  {"question": "Compute 0.75 × 0.4", "answer": "0.3"},
  {"question": "Sum of first five natural numbers?", "answer": "15"},
  {"question": "If y=2, solve y³ - y", "answer": "6"}
]

# === Metric Tools ===
embedder = SentenceTransformer("all-MiniLM-L6-v2")
rouge = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
smoothie = SmoothingFunction().method4

results = []
all_preds = []
all_refs = []

# === Format AI Judge Prompt ===
def format_prompt(question, reference, prediction):
    return f"""
You are an expert AI feedback evaluator. Evaluate the model's prediction.

Steps:
1. Understand the question.
2. Compare prediction to reference.
3. Assess correctness, clarity, completeness.
4. Give score from 1 (poor) to 5 (excellent).
5. Justify the score.

Question: {question}
Reference: {reference}
Prediction: {prediction}

Respond with:
Score: <1-5>
Explanation: ...
"""

# === Evaluation Loop ===
for item in eval_data:
    question = item['question']
    reference = item['answer'].strip()
    prompt = f"### Question: {question}\n### Answer:"
    prediction = judge_models["Mistral"](prompt).strip()

    all_preds.append(prediction)
    all_refs.append(reference)

    exact_match = prediction.lower().strip() == reference.lower().strip()
    bleu = sentence_bleu([nltk.word_tokenize(reference)], nltk.word_tokenize(prediction), smoothing_function=smoothie)
    rouge_l = rouge.score(reference, prediction)['rougeL'].fmeasure
    cosine = cosine_similarity(embedder.encode([reference]), embedder.encode([prediction]))[0][0]

    judge_feedback = {}
    judge_scores = {}

    for name, model in judge_models.items():
        judge_prompt = format_prompt(question, reference, prediction)
        output = model(judge_prompt).strip()

        def extract_score(text):
            for line in text.split("\n"):
                if "score" in line.lower():
                    digits = ''.join(filter(str.isdigit, line))
                    return int(digits) if digits else None
            return None

        score = extract_score(output)
        judge_feedback[name] = output
        judge_scores[name] = score

    results.append({
        "question": question,
        "reference": reference,
        "prediction": prediction,
        "exact_match": exact_match,
        "bleu": bleu,
        "rougeL": rouge_l,
        "cosine_similarity": cosine,
        "judge_scores": judge_scores,
        "judge_feedback": judge_feedback
    })

# === BERTScore ===
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
}

# Add judge averages
for judge in judge_models:
    judge_avg = np.mean([
        r["judge_scores"][judge] for r in results if r["judge_scores"].get(judge) is not None
    ])
    aggregate[f"{judge}_score (avg)"] = round(judge_avg, 2)

# === JSON Save Utility ===
def safe_convert(obj):
    if isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    if isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    return str(obj) if not isinstance(obj, (dict, list, str, float, int)) else obj

# === Save to File ===
output_path = "C:/myworks/AI_Agent_AS_LLM_Judge_Evaluator/llm_multiagent_eval_mathematical_REASONING.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("=== Per-Sample Results ===\n")
    f.write(json.dumps(results, indent=2, default=safe_convert))
    f.write("\n\n=== Aggregated Metrics ===\n")
    f.write(json.dumps(aggregate, indent=2, default=safe_convert))

# === 🎨 Visualization ===
# Bar chart: per-question scores by each judge
'''questions = [r["question"] for r in results]
x = np.arange(len(questions))
width = 0.25

plt.figure(figsize=(10, 5))
for i, judge in enumerate(judge_models):
    scores = [r["judge_scores"][judge] for r in results]
    plt.bar(x + i * width, scores, width=width, label=judge)

plt.xticks(x + width / 2, questions, rotation=25, ha='right')
plt.title("Judge Scores per Sample")
plt.ylabel("Score (1–5)")
plt.legend()
plt.tight_layout()
plt.savefig("C:/myworks/AI_Agent_AS_LLM_Judge_Evaluator/judge_scores_per_sample_bar_chart_factual.pdf", bbox_inches="tight", dpi=900)
plt.show()

# Line chart: average score per judge
plt.figure(figsize=(6, 4))
avg_scores = [aggregate[f"{judge}_score (avg)"] for judge in judge_models]
plt.plot(list(judge_models.keys()), avg_scores, marker='o')
plt.title("Average Score per Judge")
plt.ylabel("Score")
plt.grid(True)
plt.tight_layout()
plt.savefig("C:/myworks/AI_Agent_AS_LLM_Judge_Evaluator/judge_avg_scores_bar_chart_factual.pdf", bbox_inches="tight", dpi=900)
plt.show()'''
