# PROJECT REPORT: Fake News Detection System

---

## 1. ABSTRACT
The rapid spread of misinformation and fake news on digital platforms poses a significant threat to society. Traditional Machine Learning (ML) approaches attempt to classify fake news by analyzing text patterns; however, they fundamentally lack the ability to verify objective real-world facts. 

This project proposes a **Hybrid Fake News Detection System** that combines a **Knowledge-Based Fact Verification Engine** with a **Support Vector Machine (SVM) Text Classifier**. The system first attempts to logically verify a user's claim against a local, highly trusted fact database. If the claim is unknown (unverified), the system falls back to the ML classifier to analyze the linguistic and statistical patterns of the text using TF-IDF feature extraction. This dual-engine approach significantly mitigates the hallucination and false-positive issues present in standard ML-only classifiers.

---

## 2. INTRODUCTION
### 2.1 Background
Fake news is fabricated information that mimics news media content in form but not in organizational process or intent. 

### 2.2 Objective
To build a scalable, interactive, and intelligent Fake News Detection system capable of:
1. Logically verifying known facts using a database.
2. Classifying unknown text based on linguistic patterns learned from a large dataset.
3. Providing a clean, intuitive web interface for demonstrations.

---

## 3. PROBLEM STATEMENT
Standard Machine Learning algorithms (like Logistic Regression, Naive Bayes, or SVM) **do not know facts**. They are statistical text classifiers. If a completely false claim is written using formal, grammatically correct journalistic language, a standard ML model will likely classify it as "REAL." There is a critical need to separate **objective factual verification** from **linguistic pattern recognition**.

---

## 4. PROPOSED SYSTEM ARCHITECTURE
The system operates using a two-tier architecture:

### Tier 1: Fact Verification Engine
- **Input:** A textual claim (e.g., "India has 28 states").
- **Process:** The text undergoes smart tokenization, removing stop-words while explicitly preserving numerical values. It then uses set-intersection logic to match the subjects and objects against `fact_database.csv`.
- **Output:** 
  - `VERIFIED TRUE` (Matches known facts)
  - `VERIFIED FALSE` (Contradicts known facts)
  - `UNVERIFIED` (Proceed to Tier 2)

### Tier 2: Machine Learning Classifier
- **Input:** Unverified text.
- **Process:** The text is cleaned and converted into numerical vectors using **TF-IDF (Term Frequency-Inverse Document Frequency)**. The vectorized text is fed into a trained **Support Vector Machine (SVM)**.
- **Output:** A statistical prediction of `REAL` or `FAKE`.

---

## 5. DATASET DESCRIPTION
- **Dataset Name:** IFND (Indian Fake News Dataset)
- **Total Articles:** 56,714
- **Label Distribution:**
  - TRUE (Real News): 37,800
  - FAKE (Fake News): 18,914
- **Features Used:** `Statement` (Text), `Label` (Target Variable).

---

## 6. IMPLEMENTATION & METHODOLOGY
### 6.1 Text Preprocessing
- Conversion to lowercase.
- Removal of URLs and special characters.
- **Preservation of Numbers:** Unlike standard NLP pipelines that strip numbers, this system preserves them to accurately verify numerical facts (e.g., distinguishing "28 states" from "29 states").

### 6.2 Machine Learning Models Evaluated
The dataset was split into 80% training and 20% testing data. Three models were trained and compared:

1. **Logistic Regression**
   - Accuracy: ~94.44%
2. **Naive Bayes (Multinomial)**
   - Accuracy: ~94.14%
3. **Support Vector Machine (Linear SVC) - [SELECTED]**
   - **Accuracy:** 95.34%
   - **Precision:** 95.02%
   - **Recall:** 98.15%
   - **F1 Score:** 96.56%

### 6.3 User Interface (Streamlit)
The frontend was developed using Streamlit, featuring:
- **Check News:** The main dashboard for analyzing input.
- **Fact Manager:** A password-protected (`admin123`) administrator panel to perform CRUD (Create, Read, Update, Delete) operations on the fact database dynamically.
- **Input Validation:** Blocks gibberish (e.g., "fghjklsfgh") and ultra-short meaningless strings.

---

## 7. RESULTS & DISCUSSION
The project successfully bridges the gap between text classification and factual verification. 
- During testing, the Fact Verification Engine achieved 100% accuracy on known claims with varying syntactic structures (e.g., "The PM is Modi" vs. "Modi is the PM").
- The SVM model serves as an excellent fallback for unknown claims, analyzing text structure with 95.34% accuracy. 
- As expected, the ML model correctly identified that it is a *statistical predictor*, explicitly warning users that its output is not independent proof of factual truth.

---

## 8. LIMITATIONS
1. **Database Dependency:** The accuracy of Tier 1 is heavily dependent on the size and currency of the local `fact_database.csv`.
2. **ML Hallucination:** If an unknown fake claim is written in a highly professional tone, Tier 2 (SVM) may classify it as REAL due to the limitations of statistical pattern matching.

---

## 9. FUTURE SCOPE
- **Automated Source Retrieval:** Integrating Live APIs (e.g., Google News or Wikipedia API) to fetch real-time facts instead of relying solely on a local CSV.
- **Advanced NLP Entities:** Implementing Named Entity Recognition (NER) to automatically extract subjects and relations from complex paragraphs.
- **Transformer Models:** Upgrading the Tier 2 classifier from SVM to advanced contextual models like BERT or RoBERTa for deeper semantic understanding.

---

## 10. CONCLUSION
This project successfully demonstrates a highly effective, dual-engine approach to Fake News Detection. By treating objective factual verification and linguistic pattern classification as two separate but complementary problems, the system provides a much more robust, transparent, and accurate defense against misinformation than traditional single-model ML approaches.
