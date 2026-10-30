# Autonomous Fake News Detection System: Hybrid Machine Learning with Real-Time Live Web Fact Verification

An end-to-end, production-grade Fake News Detection and Fact Verification web application combining supervised Machine Learning (TF-IDF + Linear Support Vector Classifier) with an autonomous, real-time Live Web Fact Verification engine (Wikipedia Web API).

---

## 🌟 Key Features

1. **Dual-Engine Architecture**:
   - **Engine 1 (Live Web Fact Verifier)**: Direct real-time Wikipedia Web API querying with multi-domain authority parsers for Cinema, Corporate Governance (CEOs/Founders), Politics (Prime Ministers/Presidents), Geography (Capitals/Continents), and Scientific opposites.
   - **Engine 2 (Statistical ML Classifier)**: Linear Support Vector Machine (LinearSVC) trained on 56,714 news articles from the Indian Fake News Dataset (IFND) using 24,305 TF-IDF n-gram features.
2. **Strict Proper-Name Authority Matching (`match_claimed_person`)**:
   - Word-boundary token checking prevents partial matches and dictionary false positives (e.g., stops words like "panic" matching "Phani").
   - Transliteration tolerance handles phonetic variants seamlessly (e.g., `Ravi Bhasur` correctly matches `Ravi Basrur`).
3. **Silent Typo Auto-Correction**:
   - Integrated Wikipedia suggestion engine (`suggestion=True`) that transparently corrects human typos (e.g., `jio stduios` $\rightarrow$ `jio studios`) without intrusive UI banners.
4. **Explainable Ground-Truth Citations**:
   - Outputs verified status cards (**🟢 News is Real** / **🔴 News is Fake**) quoting the official ground truth and providing clickable source attribution.
5. **Fact Manager Dashboard**:
   - Password-protected administrative panel to view, add, and curate local ground-truth triples (`fact_database.csv`).
6. **Executive Presentation Deck**:
   - Built-in automated 15-slide widescreen (16:9) PowerPoint presentation generator (`generate_slides.py`) detailing the architecture, metrics, and case studies.

---

## 📊 Dataset & Model Performance

- **Dataset**: Indian Fake News Dataset (IFND) — 56,714 articles (37,800 True, 18,914 Fake).
- **Split**: 80% Training (45,371) / 20% Testing (11,343).
- **Evaluation Results on Held-Out Test Set**:
  - **Testing Accuracy**: **95.34%** (10,814 / 11,343 correct predictions)
  - **Precision**: **95.02%**
  - **Recall**: **98.15%**
  - **F1-Score**: **96.56%**
- **Confusion Matrix**:
  - True Real (TP): 7,420
  - True Fake (TN): 3,394
  - False Positives (FP): 389
  - False Negatives (FN): 140

---

## 🛠️ Project Structure

```text
Fakenews-Detection-using-ML/
├── dataset/
│   └── IFND.csv                     # Indian Fake News Dataset (56,714 records)
├── models/
│   ├── fake_news_model.pkl          # Trained LinearSVC model
│   └── tfidf_vectorizer.pkl         # Fitted TF-IDF vectorizer (24,305 features)
├── app.py                           # Main Streamlit web application
├── fact_checker.py                  # Curated fact-checking engine (Subject-Relation-Object)
├── fact_database.csv                # Local ground-truth triples knowledge base
├── train_model.py                   # Model training and evaluation script
├── predict_news.py                  # CLI single-article prediction script
├── generate_slides.py               # Automated 15-slide PowerPoint deck generator
├── Fake_News_Detection_Presentation.pptx # Pre-generated presentation slides
├── Project_Report.md                # Comprehensive technical project report
├── requirements.txt                 # Project dependencies
└── README.md                        # Documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/neeleshphani/Fakenews-Detection-using-ML.git
cd Fakenews-Detection-using-ML
```

### 2. Set Up a Virtual Environment & Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On Linux/macOS

pip install -r requirements.txt
```

### 3. Launch the Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Example Test Claims

| Claim | Expected Verdict | Reason / Ground Truth Cited |
| :--- | :---: | :--- |
| `the ceo of indigo is phani` | **🔴 News is Fake** | Quotes actual CEO Pieter Elbers / Rahul Bhatia |
| `the ceo of indigo is pieter elbers` | **🟢 News is Real** | Confirms Pieter Elbers served as CEO |
| `the music composer of kgf chapter one is anirudh` | **🔴 News is Fake** | Identifies true score composer as Ravi Basrur |
| `the music composer of kgf chapter one is ravi bhasur` | **🟢 News is Real** | Transliteration tolerance matches Ravi Basrur |
| `the ceo of jio stduios is phani` | **🔴 News is Fake** | Auto-corrects typo, cites CEO Jyoti Deshpande |
| `capital of telangana is andhra` | **🔴 News is Fake** | Identifies Hyderabad as capital |
| `capital of telangana is hyderabad` | **🟢 News is Real** | Confirmed |
| `india is a continent` | **🔴 News is Fake** | Identifies India as a country |
| `asia is a country` | **🔴 News is Fake** | Identifies Asia as a continent |

---

## 🔐 Fact Manager Administration
1. Go to the sidebar navigation and select **🔐 Fact Manager**.
2. Enter the administrator password: `admin123`.
3. Add or update verified facts directly into `fact_database.csv`.

---

## 📄 License
This project is licensed under the MIT License.
