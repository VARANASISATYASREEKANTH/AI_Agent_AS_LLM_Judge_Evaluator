# AI_Agent_AS_LLM_Judge_Evaluator(: Will be updated soon)

# 📊 LLM Evaluation Metrics – Comparative Guide

This repository provides a comprehensive comparison of common evaluation metrics for **Large Language Models (LLMs)** including definitions, strengths, and weaknesses. It covers both traditional string-based metrics and modern embedding-based metrics.

---

## 📘 Metrics Compared

- **Exact Match (EM)**
- **BLEU**
- **ROUGE-L**
- **Cosine Similarity**
- **BERT F1 Score** (BERTScore)

---

## 📊 Relative Comparison Table

| Feature / Metric              | **Exact Match (EM)** | **BLEU**                | **ROUGE-L**             | **Cosine Similarity**      | **BERT F1 Score** (BERTScore)  |
|-------------------------------|----------------------|-------------------------|-------------------------|-----------------------------|-------------------------------|
| **Type**                      | String match         | N-gram precision        | Longest common subsequence (recall) | Embedding-based            | Embedding + token alignment  |
| **Output Range**              | 0 or 1 (binary)      | 0–1                     | 0–1                     | –1 to 1 (usually 0–1)        | 0–1                          |
| **Captures Semantics?**       | ❌ No                | ❌ Limited              | ❌ Limited              | ✅ Yes                      | ✅ Yes                        |
| **Case & Synonym Sensitivity**| ✅ High (sensitive)  | ✅ High (sensitive)     | ✅ High (sensitive)     | ❌ Low (robust)             | ❌ Low (robust)               |
| **Handles Paraphrasing?**     | ❌ No                | ❌ Poorly               | ❌ Poorly               | ✅ Yes                      | ✅ Yes                        |
| **Factual Match Required?**   | ✅ Yes               | ✅ Yes                  | ✅ Yes                  | ❌ No                       | ❌ No                         |
| **Best For**                  | Exact span QA, NER   | Translation, factual generation | Summarization         | Sentence similarity         | QA, generation, summarization |
| **Weakness**                  | Overly strict        | Fails on paraphrase     | Surface-level only      | Ignores structure/context   | Can overfit to embeddings     |
| **Speed / Efficiency**        | ⚡ Very fast          | ⚡ Fast                 | ⚡ Fast                 | 🐢 Medium                  | 🐢 Medium to Slow             |
| **Interpretability**          | ✅ Easy              | ✅ Moderate             | ✅ Easy                 | ⚠️ Requires vector understanding | ⚠️ Harder to interpret         |
| **Granularity**               | Sentence/Span level  | Sentence/Corpus         | Sentence/Corpus         | Sentence-level              | Token-level alignment         |
| **Reference Needed?**         | ✅ Yes               | ✅ Yes                  | ✅ Yes                  | ❌ No (optional)           | ✅ Yes                        |
| **Implementation**            | Easy                 | Easy (e.g., NLTK)       | Easy (e.g., Hugging Face) | Moderate (e.g., SBERT)    | Harder (needs BERT model)     |

---

## 🧾 Metric Definitions

### 1. **Exact Match (EM)**

- **Definition:** Binary metric. Returns 1 if the predicted output **exactly matches** the reference; 0 otherwise.
- **Used for:** Extractive QA, NER, classification.
- **Limitation:** Very strict; fails on minor variation or paraphrasing.

---

### 2. **BLEU** (Bilingual Evaluation Understudy)

- **Definition:** Measures **n-gram precision** between candidate and reference with a brevity penalty.
- **Commonly used in:** Machine translation, factual generation.
- **Limitation:** Doesn't account for synonyms or reordering.

---

### 3. **ROUGE-L** (Recall-Oriented Understudy for Gisting Evaluation)

- **Definition:** Measures **Longest Common Subsequence (LCS)** between prediction and reference. Emphasizes recall.
- **Used in:** Summarization, report generation.
- **Limitation:** Still surface-based; no deep semantic understanding.

---

### 4. **Cosine Similarity (Embedding-Based)**

- **Definition:** Computes cosine of the angle between vector embeddings of sentences (e.g., using SBERT or USE).
- **Used in:** Semantic similarity, paraphrase detection.
- **Strength:** Captures meaning, not just surface structure.

---

### 5. **BERT F1 Score** (BERTScore)

- **Definition:** Uses BERT to align tokens between prediction and reference, then calculates precision, recall, and F1 in embedding space.
- **Used in:** Generation, summarization, QA.
- **Strength:** Sensitive to meaning, handles paraphrasing and synonyms well.

---

## 📦 Summary Table

| Metric        | Captures Semantics | Surface-Level | Strict Match | Embedding-Based |
|---------------|--------------------|----------------|--------------|------------------|
| **Exact Match**| ❌ No              | ✅ Yes         | ✅ Yes       | ❌ No            |
| **BLEU**       | ❌ No              | ✅ Yes         | ⚠️ Moderate  | ❌ No            |
| **ROUGE-L**    | ❌ No              | ✅ Yes         | ⚠️ Moderate  | ❌ No            |
| **Cosine Sim.**| ✅ Yes             | ❌ No          | ❌ No        | ✅ Yes           |
| **BERT F1**    | ✅ Yes             | ❌ No          | ❌ No        | ✅ Yes           |

---

## 🧠 Recommendation

| Use Case               | Recommended Metric(s)            |
|------------------------|----------------------------------|
| **Extractive QA**      | Exact Match, F1                 |
| **Translation**        | BLEU, BERTScore                 |
| **Summarization**      | ROUGE-L, BERTScore              |
| **Semantic Similarity**| Cosine Similarity, BERTScore    |
| **Paraphrase Detection**| Cosine Similarity              |












# Using AI Agent as LLM Judge Evaluator 

## Code Generation
<table border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr>
      <th>S.No</th>
      <th>Evaluation Metric</th>
      <th>LLM</th>
      <th>AI Agent</th>
      <th>Multi AI Agent</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> 1  </td>
      <td>Exact Match</td>
      <td>  20.0 </td>
      <td>  10</td>
      <td>  30</td>
    </tr>
    <tr>
      <td>2   </td>
      <td>BLEU(avg)</td>
      <td>0.345</td>
      <td>0.2798</td>
      <td>0.416</td>
    </tr>
    <tr>
      <td> 3  </td>
      <td>ROUGE L(avg)</td>
      <td>0.4779</td>
      <td>0.4367</td>
      <td>05795</td>
    </tr>
    <tr>
      <td>  4 </td>
      <td>Cosine similarity</td>
      <td>0.7034</td>
      <td>0.687</td>
      <td>0.789</td>
    </tr>
    <tr>
      <td> 5  </td>
      <td>BERT-f_1 score </td>
      <td> 0.4308</td>
      <td>0.383</td>
      <td>0.5423</td>
    </tr>


    
  </tbody>
</table>





## Commonsense Reasoning
<table border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr>
      <th>S.No</th>
      <th>Evaluation Metric</th>
      <th>LLM</th>
      <th>AI Agent</th>
      <th>Multi AI Agent</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> 1  </td>
      <td>Exact Match</td>
      <td>  0 </td>
      <td> 0 </td>
      <td> 0 </td>
    </tr>
    <tr>
      <td> 2 </td>
      <td>BLEU(avg)</td>
      <td>0.0195</td>
      <td>0.09</td>
      <td>0.0175</td>
    </tr>
    <tr>
      <td>  3 </td>
      <td>ROUGE L(avg)</td>
      <td>0.2378</td>
      <td>0.1297</td>
      <td>0.1871</td>
    </tr>
    <tr>
      <td> 4  </td>
      <td>Cosine similarity</td>
      <td>0.4025</td>
      <td>0.344</td>
      <td>0.418</td>
    </tr>
    <tr>
      <td>  5</td>
      <td>BERT-f_1 score </td>
      <td> 0.132</td>
      <td>0.1061</td>
      <td>0.127</td>
    </tr>


    
  </tbody>
</table>


## Mathematical Reasoning
<table border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr>
      <th>S.No</th>
      <th>Evaluation Metric</th>
      <th>LLM</th>
      <th>AI Agent</th>
      <th>Multi AI Agent</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> 1  </td>
      <td>Exact Match</td>
      <td> 50  </td>
      <td> 60 </td>
      <td> 60</td>
    </tr>
    <tr>
      <td> 2  </td>
      <td>BLEU(avg)</td>
      <td>0.5368</td>
      <td>0.5221</td>
      <td>0.5221</td>
    </tr>
    <tr>
      <td> 3  </td>
      <td>ROUGE L(avg)</td>
      <td>0.55</td>
      <td>0.7</td>
      <td>0.6</td>
    </tr>
    <tr>
      <td>  4 </td>
      <td>Cosine similarity</td>
      <td>0.745</td>
      <td>0.8089</td>
      <td>0.776</td>
    </tr>
    <tr>
      <td>  5 </td>
      <td>BERT-f_1 score </td>
      <td>0.7194 </td>
      <td>0.8407</td>
      <td>0.8007</td>
    </tr>


    
  </tbody>
</table>


## Open ended text generation
<table border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr>
      <th>S.No</th>
      <th>Evaluation Metric</th>
      <th>LLM</th>
      <th>AI Agent</th>
      <th>Multi AI Agent</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1   </td>
      <td>Exact Match</td>
      <td>  0</td>
      <td>  0</td>
      <td>  0</td>
    </tr>
    <tr>
      <td>  2 </td>
      <td>BLEU(avg)</td>
      <td>0.0489</td>
      <td>0.0216</td>
      <td>0.0175</td>
    </tr>
    <tr>
      <td> 3  </td>
      <td>ROUGE L(avg)</td>
      <td>0.1735</td>
      <td>0.1803</td>
      <td>0.01914</td>
    </tr>
    <tr>
      <td> 4  </td>
      <td>Cosine similarity</td>
      <td>0.5221</td>
      <td>0.5213</td>
      <td>0.4986</td>
    </tr>
    <tr>
      <td>5   </td>
      <td>BERT-f_1 score </td>
      <td> 0.1757</td>
      <td>0.1718</td>
      <td>0.1818</td>
    </tr>


    
  </tbody>
</table>


## Factual Reasoning
<table border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr>
      <th>S.No</th>
      <th>Evaluation Metric</th>
      <th>LLM</th>
      <th>AI Agent</th>
      <th>Multi AI Agent</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1   </td>
      <td>Exact Match</td>
      <td> 60  </td>
      <td> 60 </td>
      <td>  50</td>
    </tr>
    <tr>
      <td>  2 </td>
      <td>BLEU(avg)</td>
      <td>0.566</td>
      <td>0.4137</td>
      <td>0.466</td>
    </tr>
    <tr>
      <td> 3  </td>
      <td>ROUGE L(avg)</td>
      <td>0.847</td>
      <td>0.7522</td>
      <td>0.7633</td>
    </tr>
    <tr>
      <td> 4  </td>
      <td>Cosine similarity</td>
      <td>0.91</td>
      <td>0.8705</td>
      <td>0.866</td>
    </tr>
    <tr>
      <td> 5  </td>
      <td>BERT-f_1 score </td>
      <td> 0.685</td>
      <td>0.6248/td>
      <td>0.5939</td>
    </tr>
    
  </tbody>
</table>

## Logical Reasoning
<table border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr>
      <th>S.No</th>
      <th>Evaluation Metric</th>
      <th>LLM</th>
      <th>AI Agent</th>
      <th>Multi AI Agent</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> 1  </td>
      <td>Exact Match</td>
      <td> 30  </td>
      <td> 30 </td>
      <td>  30</td>
    </tr>
    <tr>
      <td> 2  </td>
      <td>BLEU(avg)</td>
      <td>0.2332</td>
      <td>0.2478</td>
      <td>0.248</td>
    </tr>
    <tr>
      <td>  3 </td>
      <td>ROUGE L(avg)</td>
      <td>0.3754</td>
      <td>0.4168</td>
      <td>0.4158</td>
    </tr>
    <tr>
      <td>  4 </td>
      <td>Cosine similarity</td>
      <td>0.6700</td>
      <td>0.7361</td>
      <td>0.74690</td>
    </tr>
    <tr>
      <td>  5 </td>
      <td>BERT-f_1 score </td>
      <td>0.6850 </td>
      <td>0.7426</td>
      <td>0.755</td>
    </tr>


    
  </tbody>
</table>

## Multi-step Problem Solving
<table border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr>
      <th>S.No</th>
      <th>Evaluation Metric</th>
      <th>LLM</th>
      <th>AI Agent</th>
      <th>Multi AI Agent</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> 1  </td>
      <td>Exact Match</td>
      <td>  30 </td>
      <td>  30</td>
      <td>  30</td>
    </tr>
    <tr>
      <td> 2 </td>
      <td>BLEU(avg)</td>
      <td>0.2332</td>
      <td>0.04</td>
      <td>0.037</td>
    </tr>
    <tr>
      <td>3   </td>
      <td>ROUGE L(avg)</td>
      <td>0.3754</td>
      <td>0.2405</td>
      <td>0.1471</td>
    </tr>
    <tr>
      <td> 4  </td>
      <td>Cosine similarity</td>
      <td>0.6709</td>
      <td>0.62</td>
      <td>0.6248</td>
    </tr>
    <tr>
      <td> 5  </td>
      <td>BERT-f_1 score </td>
      <td> 0.6805</td>
      <td>0.553</td>
      <td>0.5883</td>
    </tr>
  </tbody>
</table>
