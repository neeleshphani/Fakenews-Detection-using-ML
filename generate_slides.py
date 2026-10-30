import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Theme Colors
    BG_DARK = RGBColor(15, 23, 42)       # Slate 900
    BG_LIGHT = RGBColor(248, 250, 252)   # Slate 50
    CARD_BG = RGBColor(255, 255, 255)    # White
    CARD_BORDER = RGBColor(226, 232, 240)# Slate 200
    
    PRIMARY_BLUE = RGBColor(37, 99, 235) # Blue 600
    DARK_BLUE = RGBColor(30, 58, 138)    # Blue 900
    ACCENT_GREEN = RGBColor(22, 163, 74) # Emerald 600
    ACCENT_RED = RGBColor(220, 38, 38)   # Rose 600
    
    TEXT_MAIN = RGBColor(15, 23, 42)     # Dark slate
    TEXT_MUTED = RGBColor(71, 85, 105)   # Slate 600
    TEXT_LIGHT = RGBColor(255, 255, 255) # Pure White
    
    def add_header(slide, title_text, category_text="FAKE NEWS DETECTION SYSTEM"):
        # Header background
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = PRIMARY_BLUE
        p_cat.font.name = "Segoe UI"
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = BG_DARK
        p_title.font.name = "Segoe UI"

    def add_footer(slide, slide_num):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.4))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"Autonomous Fake News Detection System | Hybrid ML & Real-Time Live Web Verification               Slide {slide_num}"
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(148, 163, 184)
        p.font.name = "Segoe UI"

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
        return shape

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Luxury Theme)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.fill.background()
    
    # Accent bar
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = PRIMARY_BLUE
    bar.line.fill.background()
    
    tbox1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.8))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "MAJOR PROJECT REVIEW / PRESENTATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.font.name = "Segoe UI"
    
    p = tf1.add_paragraph()
    p.text = "Autonomous Fake News Detection System"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    p.font.name = "Segoe UI"
    
    p = tf1.add_paragraph()
    p.text = "Hybrid Machine Learning with Real-Time Live Web Fact Verification"
    p.font.size = Pt(20)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.font.name = "Segoe UI"
    
    p = tf1.add_paragraph()
    p.text = "\nDomain: Artificial Intelligence, Machine Learning & Natural Language Processing"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.font.name = "Segoe UI"

    # Meta card at bottom
    meta_card = add_card(slide1, Inches(1.2), Inches(5.6), Inches(11.0), Inches(1.2), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))
    mtbox = slide1.shapes.add_textbox(Inches(1.4), Inches(5.7), Inches(10.6), Inches(1.0))
    mtf = mtbox.text_frame
    mtf.word_wrap = True
    p = mtf.paragraphs[0]
    p.text = "System Components: Streamlit Web Framework | Scikit-Learn Linear SVM (95.34% Acc) | Live Wikipedia Web API"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    p.font.name = "Segoe UI"
    p = mtf.add_paragraph()
    p.text = "Department of Computer Science & Engineering | Academic Project Review"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 2: CONTENTS / AGENDA
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Presentation Agenda & Project Roadmap")
    add_footer(slide2, 2)
    
    agenda_items = [
        ("01", "Introduction & Motivation", "The challenge of viral misinformation & why static ML models fail alone."),
        ("02", "Problem Definition & Limitations", "Outdated knowledge bases, black-box labels, and undetected entity swaps."),
        ("03", "Proposed Hybrid Solution", "Dual-engine architecture: Statistical SVM + Real-Time Live Web Fact Verification."),
        ("04", "System Workflow & Pipeline", "Step-by-step pipeline from gibberish filtering to ground-truth citation."),
        ("05", "Dataset & Knowledge Base", "Indian Fake News Dataset (56,714 articles) & Live Wikipedia API."),
        ("06", "System Architecture & Modules", "Detailed component design: Preprocessing, FactChecker, ML, Web UI."),
        ("07", "Machine Learning & NLP", "TF-IDF N-grams (24,305 features), Linear SVM, Probability Calibration."),
        ("08", "Live Web Verification Engine", "Multi-domain extractors for Cinema, Corporate, Politics, Geography & Science."),
        ("09", "Strict Entity Matching Algorithm", "Token subset & phonetic distance preventing false positives & handling typos."),
        ("10", "Output & Explainable UI", "Streamlit dashboard, color-coded visual cards, and verified ground-truth quotes."),
        ("11", "Evaluation Results & Metrics", "95.34% Accuracy, 96.56% F1-score, Confusion Matrix & Baseline Comparisons."),
        ("12", "Conclusion & Future Scope", "Key technical achievements, edge-case robustness, and future expansion.")
    ]
    
    for i, (num, title, desc) in enumerate(agenda_items):
        col = i // 6
        row = i % 6
        x = Inches(0.8 + col * 5.9)
        y = Inches(1.7 + row * 0.85)
        
        card = add_card(slide2, x, y, Inches(5.7), Inches(0.75), bg_color=CARD_BG, border_color=CARD_BORDER)
        tb = slide2.shapes.add_textbox(x + Inches(0.15), y + Inches(0.08), Inches(5.4), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.text = f"{num}. {title}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_BLUE
        p.font.name = "Segoe UI"
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MUTED
        p2.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 3: INTRODUCTION & MOTIVATION
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Introduction: The Misinformation Epidemic")
    add_footer(slide3, 3)
    
    # 3 Cards
    cards_data3 = [
        ("The Growing Challenge", 
         "Rapid Spread of Fake News",
         "The digital age has democratized news publishing, allowing misinformation, deceptive propaganda, and unverified rumors to spread exponentially across social media and messaging platforms.\n\n"
         "Real-World Consequences:\n"
         "Manipulated public opinion, market panic, political destabilization, and widespread social unrest.",
         PRIMARY_BLUE),
        ("Critical Bottleneck", 
         "Why Traditional ML Models Fail",
         "Existing fake news detectors rely entirely on static text classification models (e.g. naive bayes, LSTM, SVM).\n\n"
         "The Fundamental Flaw:\n"
         "Static ML only learns linguistic style and word patterns. It has NO concept of real-world truth or recent real-time facts. If a fake claim is written in authoritative, professional language, standard ML will incorrectly classify it as REAL.",
         ACCENT_RED),
        ("Project Motivation", 
         "The Need for a Hybrid Dual-Engine",
         "To reliably combat fake news, a system must combine linguistic screening with real-time fact-checking.\n\n"
         "Our Core Objective:\n"
         "Build an intelligent system that verifies claims against live global knowledge (Wikipedia Web API) and structured records, providing users with the verified truth and authoritative sources rather than an unexplained label.",
         ACCENT_GREEN)
    ]
    
    for i, (tag, heading, text, accent) in enumerate(cards_data3):
        x = Inches(0.8 + i * 3.95)
        add_card(slide3, x, Inches(1.8), Inches(3.8), Inches(4.9))
        
        # Accent bar on top of card
        top_bar = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(3.8), Inches(0.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = accent
        top_bar.line.fill.background()
        
        tb = slide3.shapes.add_textbox(x + Inches(0.25), Inches(2.05), Inches(3.3), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tag.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = accent
        
        p = tf.add_paragraph()
        p.text = heading
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = BG_DARK
        
        p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 4: PROBLEM DEFINITION & LIMITATIONS
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Problem Definition & Limitations of Existing Systems")
    add_footer(slide4, 4)
    
    # 2 Wide Columns: Existing Limitations vs Project Solution
    add_card(slide4, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    tb_left = slide4.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfl = tb_left.text_frame
    tfl.word_wrap = True
    
    p = tfl.paragraphs[0]
    p.text = "LIMITATIONS OF EXISTING DETECTORS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    
    p = tfl.add_paragraph()
    p.text = "1. Static Knowledge Cutoff Date"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfl.add_paragraph()
    p.text = "Models trained on older datasets (e.g. 2018-2022) are blind to recent corporate appointments, elections, cinema releases, and world events."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    
    p = tfl.add_paragraph()
    p.text = "2. Vulnerable to Entity Swapping"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfl.add_paragraph()
    p.text = "Claims like 'The CEO of IndiGo is Phani' mimic true news patterns. A purely statistical classifier often marks them REAL because the sentence structure is valid."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    p = tfl.add_paragraph()
    p.text = "3. Black-Box Unexplained Output"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfl.add_paragraph()
    p.text = "Standard systems output only a bare probability or label without quoting what the actual real fact is or providing verifiable source links."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    add_card(slide4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), bg_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    tb_right = slide4.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfr = tb_right.text_frame
    tfr.word_wrap = True
    
    p = tfr.paragraphs[0]
    p.text = "OUR ADDRESSING METHODOLOGY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    
    p = tfr.add_paragraph()
    p.text = "1. Dynamic Live Web Integration"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfr.add_paragraph()
    p.text = "Connects directly to Wikipedia's Live Web API, dynamically retrieving the latest global facts across 6.8+ million active encyclopedia articles."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    
    p = tfr.add_paragraph()
    p.text = "2. Strict Proper-Name Authority Matching"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfr.add_paragraph()
    p.text = "Employs full-token subset and word-boundary regex checking to stop false positives while gracefully handling phonetic transliterations (e.g. 'Ravi Bhasur' -> 'Ravi Basrur')."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    p = tfr.add_paragraph()
    p.text = "3. Transparent Ground-Truth Citation"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfr.add_paragraph()
    p.text = "Whenever a fake claim is detected, the system quotes the official record (e.g., actual CEO or composer) and cites the exact source page."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 5: PROPOSED SOLUTION ARCHITECTURE
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Proposed Solution: Dual-Engine Hybrid AI")
    add_footer(slide5, 5)
    
    # 2 Feature Cards: Engine 1 & Engine 2
    add_card(slide5, Inches(0.8), Inches(1.8), Inches(5.7), Inches(3.6))
    tb_e1 = slide5.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(3.2))
    tfe1 = tb_e1.text_frame
    tfe1.word_wrap = True
    p = tfe1.paragraphs[0]
    p.text = "ENGINE 1: DYNAMIC FACT VERIFICATION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p = tfe1.add_paragraph()
    p.text = "Real-Time Knowledge & Ground-Truth Verification"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfe1.add_paragraph()
    p.text = "• Local Curated Knowledge Base: Fast Subject-Relation-Object triple verification via fact_database.csv.\n" \
             "• Live Wikipedia Web API: Real-time queries for current leadership, entertainment credits, geography, science.\n" \
             "• Zero Hallucination: Quotes extracted official sentences directly from Wikipedia pages.\n" \
             "• Silent Typo Auto-Correction: Resolves misspellings (e.g. 'jio stduios') without intrusive UI warnings."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    
    add_card(slide5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(3.6))
    tb_e2 = slide5.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(3.2))
    tfe2 = tb_e2.text_frame
    tfe2.word_wrap = True
    p = tfe2.paragraphs[0]
    p.text = "ENGINE 2: MACHINE LEARNING CLASSIFIER"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p = tfe2.add_paragraph()
    p.text = "TF-IDF + Linear Support Vector Machine (SVM)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfe2.add_paragraph()
    p.text = "• Statistical Pattern Recognition: Screen full-length news articles, essays, and unstructured text.\n" \
             "• TF-IDF Vectorizer: 24,305 extracted linguistic features capturing subtle styling cues.\n" \
             "• Linear SVM Classifier: High-dimensional linear hyperplane separating genuine vs deceptive language.\n" \
             "• Validated on IFND: Evaluated on 56,714 articles achieving 95.34% test accuracy."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    # Bottom Banner
    bot_card = add_card(slide5, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.2), bg_color=RGBColor(241, 245, 249), border_color=PRIMARY_BLUE)
    tbb = slide5.shapes.add_textbox(Inches(1.1), Inches(5.75), Inches(11.1), Inches(0.9))
    tfb = tbb.text_frame
    tfb.word_wrap = True
    p = tfb.paragraphs[0]
    p.text = "HYBRID ADVANTAGE: WHY COMBINING BOTH ENGINES WINS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p = tfb.add_paragraph()
    p.text = "When factual claims (e.g. cinema composers, company CEOs, capital cities) enter the system, Engine 1 guarantees factual accuracy against live records. When full articles enter, Engine 2 inspects language patterns. The user always receives an explainable, grounded result."
    p.font.size = Pt(11)
    p.font.color.rgb = BG_DARK

    # ==========================================
    # SLIDE 6: END-TO-END SYSTEM WORKFLOW
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "System Workflow: From Claim to Verified Evidence")
    add_footer(slide6, 6)
    
    stages = [
        ("Step 1", "Claim Input & Validation", "User enters claim in Streamlit UI; system verifies length >= 3 words and filters gibberish / repeated characters."),
        ("Step 2", "Curated Fact Base", "FactChecker checks local verified triples (S-R-O). If SUPPORTED or CONTRADICTED, immediate result is returned."),
        ("Step 3", "Dynamic Role / Category Router", "Identifies domain intent via regex: Leadership (CEO/PM), Cinema (Director/Composer), Geography (Capitals/Continents)."),
        ("Step 4", "Live Wikipedia Querying", "Searches Wikipedia with suggestion=True. Resolves typos silently and fetches target entity pages."),
        ("Step 5", "Strict Authority Matching", "match_claimed_person inspects role sentence; checks token subsets & phonetic distance (e.g. Ravi Bhasur)."),
        ("Step 6", "Explainable Output", "Renders green REAL card or red FAKE card with quoted ground-truth fact and official Wikipedia source.")
    ]
    
    for i, (step, title, desc) in enumerate(stages):
        x = Inches(0.8 + i * 1.95)
        add_card(slide6, x, Inches(1.8), Inches(1.85), Inches(4.9))
        
        # Step header pill
        pill = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.15), Inches(2.0), Inches(1.55), Inches(0.4))
        pill.fill.solid()
        pill.fill.fore_color.rgb = PRIMARY_BLUE
        pill.line.fill.background()
        ptf = pill.text_frame
        p = ptf.paragraphs[0]
        p.text = step
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        p.alignment = PP_ALIGN.CENTER
        
        tb = slide6.shapes.add_textbox(x + Inches(0.1), Inches(2.55), Inches(1.65), Inches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = BG_DARK
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 7: DATASET & KNOWLEDGE REPOSITORY
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Dataset Details & Real-Time Knowledge Repository")
    add_footer(slide7, 7)
    
    # Left: IFND Dataset Breakdown
    add_card(slide7, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9))
    tb_d1 = slide7.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfd1 = tb_d1.text_frame
    tfd1.word_wrap = True
    p = tfd1.paragraphs[0]
    p.text = "OFFLINE ML TRAINING DATASET"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p = tfd1.add_paragraph()
    p.text = "Indian Fake News Dataset (IFND)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfd1.add_paragraph()
    p.text = "• Total Sample Size: 56,714 labeled news articles\n" \
             "• Genuine News (TRUE): 37,800 records (66.6%)\n" \
             "• Fabricated News (FAKE): 18,914 records (33.4%)\n" \
             "• Data Partitioning:\n" \
             "   - Training Set (80%): 45,371 articles\n" \
             "   - Test Set (20%): 11,343 articles (Stratified)\n\n" \
             "Preprocessing Pipeline:\n" \
             "• Removal of HTTP/HTTPS URLs & web artifacts\n" \
             "• Lowercase text normalization\n" \
             "• Preservation of critical numerical entities & dates\n" \
             "• Stopword removal using Scikit-Learn English dictionary"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    # Right: Live Wikipedia & Curated Knowledge
    add_card(slide7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9))
    tb_d2 = slide7.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfd2 = tb_d2.text_frame
    tfd2.word_wrap = True
    p = tfd2.paragraphs[0]
    p.text = "REAL-TIME KNOWLEDGE REPOSITORY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p = tfd2.add_paragraph()
    p.text = "Wikipedia Web API & Curated Triples"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfd2.add_paragraph()
    p.text = "1. Wikipedia Live Web API Integration:\n" \
             "• Over 6.8 million English Wikipedia articles dynamically queried in real time.\n" \
             "• Direct programmatic access via custom User-Agent to retrieve live summaries, infoboxes, and role credits.\n" \
             "• Search suggestions (suggestion=True) automatically resolve human typographical errors.\n\n" \
             "2. Curated Fact Database (fact_database.csv):\n" \
             "• High-priority ground-truth triples for instant local verification.\n" \
             "• Subject-Relation-Object format.\n" \
             "• Easily extensible via the built-in Fact Manager UI."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 8: SYSTEM MODULES
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Core System Modules & Implementation")
    add_footer(slide8, 8)
    
    modules = [
        ("Module 1", "Input Preprocessing & Validation", 
         "Validates text length (min 3 words), screens out gibberish or character repetitions, normalizes whitespace, and extracts numerical/named entity tokens."),
        ("Module 2", "Curated Fact Checker", 
         "Maintains local ground-truth triples in fact_database.csv. Evaluates Subject-Relation-Object overlap and detects direct contradictions instantly."),
        ("Module 3", "Autonomous Live Web Verifier", 
         "Queries Wikipedia Web API for target entities. Applies domain-specific parsers for Cinema, Leadership, Capitals, Geography, and Scientific opposites."),
        ("Module 4", "Strict Entity Matcher", 
         "match_claimed_person inspects role-holding sentences. Requires token-subset alignment, word-boundary checks, and handles phonetic transliterations."),
        ("Module 5", "Machine Learning Pipeline", 
         "TF-IDF vectorizer (24,305 features) and Linear Support Vector Classifier (LinearSVC) provide statistical styling classification for long narrative articles."),
        ("Module 6", "Interactive Web Dashboard", 
         "Modern Streamlit web application with real-time prediction, color-coded visual cards (🟢 Real / 🔴 Fake), quoted facts, and Fact Manager administration.")
    ]
    
    for i, (m_id, m_name, m_desc) in enumerate(modules):
        col = i % 3
        row = i // 3
        x = Inches(0.8 + col * 3.95)
        y = Inches(1.8 + row * 2.5)
        
        add_card(slide8, x, y, Inches(3.8), Inches(2.35))
        tb = slide8.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), Inches(3.4), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = m_id.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_BLUE
        p = tf.add_paragraph()
        p.text = m_name
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = BG_DARK
        p = tf.add_paragraph()
        p.text = m_desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 9: ML & NLP ALGORITHMS
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Machine Learning & Natural Language Processing Algorithms")
    add_footer(slide9, 9)
    
    add_card(slide9, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9))
    tb_a1 = slide9.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfa1 = tb_a1.text_frame
    tfa1.word_wrap = True
    p = tfa1.paragraphs[0]
    p.text = "FEATURE EXTRACTION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p = tfa1.add_paragraph()
    p.text = "TF-IDF Vectorization"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfa1.add_paragraph()
    p.text = "Term Frequency - Inverse Document Frequency evaluates the statistical significance of words across the dataset:\n\n" \
             "TF-IDF(t, d, D) = TF(t, d) × log(|D| / |{d ∈ D : t ∈ d}|)\n\n" \
             "Project Implementation Details:\n" \
             "• 24,305 unique unigrams & bigrams extracted.\n" \
             "• Document frequency threshold: max_df = 0.7 (filters corpus-wide noise words).\n" \
             "• Sublinear term frequency scaling applied to normalize varying document lengths.\n" \
             "• Saved artifact: models/tfidf_vectorizer.pkl."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    add_card(slide9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9))
    tb_a2 = slide9.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfa2 = tb_a2.text_frame
    tfa2.word_wrap = True
    p = tfa2.paragraphs[0]
    p.text = "SUPERVISED CLASSIFICATION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p = tfa2.add_paragraph()
    p.text = "Linear Support Vector Machine (LinearSVC)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfa2.add_paragraph()
    p.text = "SVM constructs an optimal maximum-margin separating hyperplane in high-dimensional space:\n\n" \
             "min_{w,b} (1/2)||w||² + C ∑ max(0, 1 - y_i(w^T x_i + b))\n\n" \
             "Why Linear SVM was Selected as the Best Model:\n" \
             "• Superior text classification performance: 95.34% accuracy on IFND test set.\n" \
             "• High resilience against overfitting in sparse, 24,000+ dimensional feature spaces.\n" \
             "• Outperformed Multinomial Naive Bayes and Logistic Regression in precision (95.02%) and recall (98.15%).\n" \
             "• Saved artifact: models/fake_news_model.pkl."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 10: SYSTEM ARCHITECTURE
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "System Architecture: Hybrid Layered Design")
    add_footer(slide10, 10)
    
    layers = [
        ("Layer 1: User Presentation Layer", "Streamlit Interactive Web Interface", 
         "Input Claim Area | Live Real/Fake Cards | Real Information Display | Source Citations | Fact Manager Administration", PRIMARY_BLUE),
        ("Layer 2: Validation & Sanitization", "Input Validator & Typo Resolver", 
         "Gibberish Detector (regex) | Minimum Word Length Filter | Wikipedia Search Suggestion Engine (Silent Typo Corrector)", DARK_BLUE),
        ("Layer 3: Verification Routing Engine", "Intent Classifier & Category Matcher", 
         "Routes to: [1] Curated Triples (S-R-O) -> [2] Domain Role Verifiers (Cinema/Gov/Tech) -> [3] Opposites & Science -> [4] ML Fallback", RGBColor(79, 70, 229)),
        ("Layer 4: Real-Time Fact Resolution", "Dynamic Web & Entity Validator", 
         "Wikipedia Live Web API | Strict Word-Boundary Token Matcher (match_claimed_person) | Transliteration Distance Matcher", ACCENT_GREEN),
        ("Layer 5: Statistical Pattern Fallback", "Machine Learning Pipeline", 
         "TF-IDF Vectorizer (24,305 vocabulary) | Linear Support Vector Classifier (LinearSVC) trained on 56,714 IFND records", RGBColor(14, 116, 144))
    ]
    
    for i, (l_title, l_sub, l_details, color) in enumerate(layers):
        y = Inches(1.8 + i * 0.98)
        card = add_card(slide10, Inches(0.8), y, Inches(11.733), Inches(0.85))
        
        # Color bar on left
        cbar = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.12), Inches(0.85))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = color
        cbar.line.fill.background()
        
        tb = slide10.shapes.add_textbox(Inches(1.1), y + Inches(0.08), Inches(11.2), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{l_title.upper()}  —  {l_sub}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = color
        p = tf.add_paragraph()
        p.text = l_details
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 11: USER INTERFACE & OUTPUT DESIGN
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "User Interface & Explainable Output Design")
    add_footer(slide11, 11)
    
    # Left Card: Real Result Mockup
    add_card(slide11, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), bg_color=RGBColor(240, 253, 244), border_color=ACCENT_GREEN)
    tb_u1 = slide11.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfu1 = tb_u1.text_frame
    tfu1.word_wrap = True
    p = tfu1.paragraphs[0]
    p.text = "AUTHENTICATED RESULT DISPLAY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p = tfu1.add_paragraph()
    p.text = "🟢 News is Real"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p = tfu1.add_paragraph()
    p.text = "Input Claim: 'the music composer of kgf chapter one is ravi basrur'\n\n" \
             "Real Information:\n" \
             "Live Wikipedia records confirm that 'Ravi Basrur' is associated as the music composer of KGF: Chapter 1 (soundtrack): Ravi Basrur composed the songs and the background score.\n\n" \
             "Source:\n" \
             "Wikipedia Live Web API (KGF: Chapter 1 (soundtrack))\n\n" \
             "Key Features:\n" \
             "• Instant green verification banner (#d4edda).\n" \
             "• Transparent quotation of official movie credits.\n" \
             "• Clickable authoritative source attribution."
    p.font.size = Pt(11)
    p.font.color.rgb = BG_DARK

    # Right Card: Fake Result Mockup
    add_card(slide11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), bg_color=RGBColor(254, 242, 242), border_color=ACCENT_RED)
    tb_u2 = slide11.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfu2 = tb_u2.text_frame
    tfu2.word_wrap = True
    p = tfu2.paragraphs[0]
    p.text = "REFUTED RESULT DISPLAY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    p = tfu2.add_paragraph()
    p.text = "🔴 News is Fake"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    p = tfu2.add_paragraph()
    p.text = "Input Claim: 'the ceo of indigo is phani'\n\n" \
             "Real Information:\n" \
             "Live Wikipedia records state that: \"In the aftermath of the operational disruptions, CEO Pieter Elbers resigned on 10 March 2026, with managing director Rahul Bhatia assuming management of the airline as the interim CEO.\" The claim asserting that 'Phani' is the ceo is incorrect.\n\n" \
             "Source:\n" \
             "Wikipedia Live Web API (IndiGo)\n\n" \
             "Key Features:\n" \
             "• Red contradiction alert (#f8d7da).\n" \
             "• Cites the actual historical and current leadership."
    p.font.size = Pt(11)
    p.font.color.rgb = BG_DARK

    # ==========================================
    # SLIDE 12: EVALUATION RESULTS & METRICS
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "Model Evaluation & Empirical Results")
    add_footer(slide12, 12)
    
    # 4 Metric Cards
    metrics = [
        ("95.34%", "Testing Accuracy", "10,814 / 11,343 correct predictions on held-out test set.", PRIMARY_BLUE),
        ("95.02%", "Precision Score", "High confidence: minimizes false positive misclassifications.", ACCENT_GREEN),
        ("98.15%", "Recall Score", "Comprehensive coverage: detects 98% of all true articles.", RGBColor(14, 116, 144)),
        ("96.56%", "F1-Score", "Balanced harmonic mean across both classes.", RGBColor(109, 40, 217))
    ]
    
    for i, (val, title, desc, color) in enumerate(metrics):
        x = Inches(0.8 + i * 2.95)
        add_card(slide12, x, Inches(1.8), Inches(2.85), Inches(1.6))
        
        # Color bar
        cbar = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(2.85), Inches(0.08))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = color
        cbar.line.fill.background()
        
        tb = slide12.shapes.add_textbox(x + Inches(0.15), Inches(1.95), Inches(2.55), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = color
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = BG_DARK
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED

    # Confusion Matrix Table & Analysis
    add_card(slide12, Inches(0.8), Inches(3.6), Inches(5.7), Inches(3.1))
    tb_cm = slide12.shapes.add_textbox(Inches(1.0), Inches(3.75), Inches(5.3), Inches(2.8))
    tfcm = tb_cm.text_frame
    tfcm.word_wrap = True
    p = tfcm.paragraphs[0]
    p.text = "CONFUSION MATRIX ON HELD-OUT TEST DATA (11,343 SAMPLES)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p = tfcm.add_paragraph()
    p.text = "• True Fake Correctly Detected (TN): 3,394 articles\n" \
             "• False Positives (Fake predicted as Real): 389 articles\n" \
             "• False Negatives (Real predicted as Fake): 140 articles\n" \
             "• True Real Correctly Detected (TP): 7,420 articles\n\n" \
             "Key Takeaway:\n" \
             "Extremely low False Negative rate (only 1.85%) ensures genuine news is rarely rejected, while maintaining over 95% precision."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    add_card(slide12, Inches(6.8), Inches(3.6), Inches(5.7), Inches(3.1))
    tb_comp = slide12.shapes.add_textbox(Inches(7.0), Inches(3.75), Inches(5.3), Inches(2.8))
    tfcomp = tb_comp.text_frame
    tfcomp.word_wrap = True
    p = tfcomp.paragraphs[0]
    p.text = "BENCHMARK ALGORITHM COMPARISON"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p = tfcomp.add_paragraph()
    p.text = "Model                           Accuracy     Precision    Recall      F1-Score\n" \
             "--------------------------------------------------------------------------\n" \
             "Multinomial Naive Bayes          87.40%       86.20%       91.10%      88.58%\n" \
             "Logistic Regression              92.85%       91.90%       95.40%      93.62%\n" \
             "Linear SVM (Selected)           95.34%       95.02%       98.15%      96.56%\n\n" \
             "Conclusion:\n" \
             "Linear SVM delivered the highest overall accuracy (+2.49% over Logistic Regression) and best handled the sparse TF-IDF text representation."
    p.font.size = Pt(10.5)
    p.font.color.rgb = BG_DARK

    # ==========================================
    # SLIDE 13: LIVE WEB TEST CASE STUDIES
    # ==========================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "Real-Time Verification Case Studies & Robustness")
    add_footer(slide13, 13)
    
    test_cases = [
        ("the ceo of indigo is phani", "🔴 FAKE", "Cites Pieter Elbers (resigned 2026) / Rahul Bhatia", "Strict token boundary stops false word match"),
        ("the ceo of indigo is pieter elbers", "🟢 REAL", "Live Wikipedia confirms Pieter Elbers as former CEO", "Direct role-statement match"),
        ("the music composer of kgf chapter one is anirudh", "🔴 FAKE", "Wikipedia credits Ravi Basrur for KGF score & album", "Zero hallucination (avoids Beast film)"),
        ("the music composer of kgf chapter one is ravi bhasur", "🟢 REAL", "Phonetic transliteration match with Ravi Basrur", "Fuzzy token similarity > 91%"),
        ("the ceo of jio stduios is phani", "🔴 FAKE", "Auto-corrects 'stduios' -> 'studios', cites Jyoti Deshpande", "Silent search suggestion correction"),
        ("the director of jailer is nelson dilipkumar", "🟢 REAL", "Confirmed: Nelson Dilipkumar directed Jailer", "Entertainment credit extraction"),
        ("the prime minister of india is rahul gandhi", "🔴 FAKE", "Identifies Narendra Modi as incumbent Prime Minister", "Rejects non-incumbent leadership claim"),
        ("capital of telangana is andhra", "🔴 FAKE", "Correctly identifies Hyderabad as capital", "Capitals relational verification"),
        ("india is a continent", "🔴 FAKE", "Identifies India as country; cites 7 continents", "Geographical category contradiction")
    ]
    
    # Table layout
    rows = len(test_cases) + 1
    cols = 4
    left = Inches(0.8)
    top = Inches(1.8)
    width = Inches(11.733)
    height = Inches(4.9)
    
    table_shape = slide13.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(3.8)
    table.columns[1].width = Inches(1.2)
    table.columns[2].width = Inches(3.8)
    table.columns[3].width = Inches(2.933)
    
    headers = ["Test Claim Submitted", "Result", "Live Ground-Truth Evidence", "Engineering Mechanism"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BG_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        
    for i, (claim, res, ev, mech) in enumerate(test_cases):
        row_idx = i + 1
        bg = RGBColor(248, 250, 252) if i % 2 == 0 else RGBColor(255, 255, 255)
        
        c0 = table.cell(row_idx, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = bg
        p = c0.text_frame.paragraphs[0]
        p.text = f'"{claim}"'
        p.font.size = Pt(9.5)
        p.font.name = "Segoe UI"
        
        c1 = table.cell(row_idx, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = bg
        p = c1.text_frame.paragraphs[0]
        p.text = res
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.name = "Segoe UI"
        
        c2 = table.cell(row_idx, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = bg
        p = c2.text_frame.paragraphs[0]
        p.text = ev
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        
        c3 = table.cell(row_idx, 3)
        c3.fill.solid()
        c3.fill.fore_color.rgb = bg
        p = c3.text_frame.paragraphs[0]
        p.text = mech
        p.font.size = Pt(9.5)
        p.font.color.rgb = PRIMARY_BLUE

    # ==========================================
    # SLIDE 14: CONCLUSION & FUTURE SCOPE
    # ==========================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_header(slide14, "Conclusion & Future Scope")
    add_footer(slide14, 14)
    
    add_card(slide14, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9))
    tb_c1 = slide14.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfc1 = tb_c1.text_frame
    tfc1.word_wrap = True
    p = tfc1.paragraphs[0]
    p.text = "PROJECT CONTRIBUTIONS & ACHIEVEMENTS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p = tfc1.add_paragraph()
    p.text = "Key Takeaways & Technical Impact"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfc1.add_paragraph()
    p.text = "• Solved the Static ML Bottleneck: Integrated live Wikipedia Web API querying so the system is never constrained by training data age.\n\n" \
             "• Zero Hallucination Entity Matching: Developed match_claimed_person to eliminate false dictionary matches (e.g. 'panic' matching 'phani').\n\n" \
             "• High Machine Learning Efficacy: 95.34% test accuracy and 98.15% recall on 56,714 IFND news articles.\n\n" \
             "• Transparent Explainability: Displays the authentic real fact and quotes the direct Wikipedia page source.\n\n" \
             "• Production-Ready Deployment: Fully functional interactive Streamlit application with live reload."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    add_card(slide14, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9))
    tb_c2 = slide14.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfc2 = tb_c2.text_frame
    tfc2.word_wrap = True
    p = tfc2.paragraphs[0]
    p.text = "FUTURE ENHANCEMENTS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p = tfc2.add_paragraph()
    p.text = "Roadmap for Future Research"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BG_DARK
    p = tfc2.add_paragraph()
    p.text = "1. Multimodal Fact-Checking:\n" \
             "Extend detection to multimedia fake news by combining computer vision models to detect deepfakes and manipulated news images.\n\n" \
             "2. Multilingual Indian Language Support:\n" \
             "Incorporate mBERT and IndicBERT to natively verify vernacular news articles across Hindi, Telugu, Tamil, and Bengali.\n\n" \
             "3. Browser Extension & Social Media Plugin:\n" \
             "Package the verification API into a lightweight browser add-on to flag unverified claims directly on Twitter/X, WhatsApp Web, and Reddit."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 15: THANK YOU / Q&A
    # ==========================================
    slide15 = prs.slides.add_slide(blank_layout)
    bg15 = slide15.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg15.fill.solid()
    bg15.fill.fore_color.rgb = BG_DARK
    bg15.line.fill.background()
    
    tbox15 = slide15.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.333), Inches(3.5))
    tf15 = tbox15.text_frame
    tf15.word_wrap = True
    
    p = tf15.paragraphs[0]
    p.text = "THANK YOU!"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.font.name = "Segoe UI"
    p.alignment = PP_ALIGN.CENTER
    
    p = tf15.add_paragraph()
    p.text = "Autonomous Fake News Detection System"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    p.font.name = "Segoe UI"
    p.alignment = PP_ALIGN.CENTER
    
    p = tf15.add_paragraph()
    p.text = "Hybrid Machine Learning with Real-Time Live Web Fact Verification\n"
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.font.name = "Segoe UI"
    p.alignment = PP_ALIGN.CENTER
    
    p = tf15.add_paragraph()
    p.text = "Questions & Feedback Welcome"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.font.name = "Segoe UI"
    p.alignment = PP_ALIGN.CENTER

    out_path = r"C:\Users\Phani\OneDrive\Desktop\Fakenews_ml\Fake_News_Detection_Presentation.pptx"
    prs.save(out_path)
    print(f"Presentation successfully saved to: {out_path}")
    print(f"Total slides generated: {len(prs.slides)}")

if __name__ == "__main__":
    create_presentation()
