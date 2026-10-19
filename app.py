
import re
import difflib
import streamlit as st

st.set_page_config(
    page_title="CareerBot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp,
[data-testid="stAppViewContainer"] {
    background: #f6f8fc !important;
    color: #172033 !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: #f6f8fc !important;
}

[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e5eaf2;
}

[data-testid="stSidebar"] * {
    color: #172033 !important;
}

.main .block-container {
    max-width: 1100px;
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}

/* Hero banner */
.hero {
    background: linear-gradient(120deg, #172554, #3157a4);
    color: #ffffff !important;
    padding: 28px 30px;
    border-radius: 18px;
    margin-bottom: 24px;
}

.hero h1 {
    color: #ffffff !important;
    font-size: 30px;
    font-weight: 800;
    margin: 0 0 8px 0;
}

.hero p {
    color: #e3eaff !important;
    font-size: 15px;
    line-height: 1.6;
    margin: 0;
}

.section-title {
    font-size: 19px;
    font-weight: 700;
    color: #172554 !important;
    margin: 12px 0;
}

.small-label {
    color: #64748b !important;
    font-size: 13px;
    margin-bottom: 10px;
}

/* Topic and suggested question buttons */
div.stButton > button {
    width: 100%;
    min-height: 46px;
    text-align: left;
    border: 1px solid #dfe6f2 !important;
    background: #ffffff !important;
    color: #172033 !important;
    border-radius: 10px;
    padding: 10px 13px;
    font-weight: 500;
}

div.stButton > button p,
div.stButton > button span {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

div.stButton > button:hover {
    border-color: #5276cf !important;
    background: #f0f4ff !important;
}

div.stButton > button:hover p,
div.stButton > button:hover span {
    color: #1e40af !important;
    -webkit-text-fill-color: #1e40af !important;
}

/* CHAT: force readable text in every message */
[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #e1e7f0 !important;
    border-radius: 14px !important;
    padding: 14px 16px !important;
    margin-bottom: 12px !important;
    opacity: 1 !important;
}

[data-testid="stChatMessage"] * {
    opacity: 1 !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] *,
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] ol,
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    opacity: 1 !important;
}

/* Chat input */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    background: #ffffff !important;
}

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus {
    background: #ffffff !important;
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    caret-color: #172033 !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    opacity: 1 !important;
}

/* General text */
[data-testid="stAppViewContainer"] .stMarkdown,
[data-testid="stAppViewContainer"] .stMarkdown p,
[data-testid="stAppViewContainer"] .stMarkdown li {
    color: #172033;
}

hr {
    border-color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- KNOWLEDGE BASE ----------------
FAQS = [
    {
        "topic": "Internships",
        "question": "How can I find an internship?",
        "keywords": ["find internship", "get internship", "internship opportunities"],
        "answer": """You can find internships through:

1. **Internship platforms:** Internshala, LinkedIn, AICTE Internship Portal and company career pages.
2. **Company websites:** Check official internship announcements.
3. **GitHub:** Showcase your projects.
4. **College network:** Ask faculty and placement coordinators about opportunities.

**Tip:** Verify the organization before applying, and check whether the internship is free."""
    },
    {
        "topic": "Internships",
        "question": "What skills are needed for an AI/ML internship?",
        "keywords": ["ai ml internship skills", "machine learning internship"],
        "answer": """For a beginner AI/ML internship, focus on:

- Python fundamentals
- NumPy and pandas
- Basic statistics
- Machine learning algorithms
- Scikit-learn
- Git and GitHub
- One or two practical projects

Build your fundamentals and keep improving while applying."""
    },
    {
        "topic": "Internships",
        "question": "How do I prepare my internship application?",
        "keywords": ["internship application", "apply internship"],
        "answer": """Prepare your application like this:

1. Create a clear, one-page resume.
2. Include your genuine skills and projects.
3. Upload your project code and README to GitHub.
4. Write a short, customized application message.
5. Apply through official company websites or verified portals.
6. Track your applications and practise interviews.

Be cautious of anyone promising guaranteed employment in exchange for money."""
    },
    {
        "topic": "Resume",
        "question": "How do I create a good resume as a student?",
        "keywords": ["student resume", "resume format", "make resume"],
        "answer": """A good student resume can include:

1. Name and professional contact details
2. Career objective
3. Education and academic performance
4. Technical skills
5. Projects and technologies used
6. Relevant certifications or achievements

Keep it to one page when possible. Use clear headings and honest information."""
    },
    {
        "topic": "Resume",
        "question": "What should I write in my career objective?",
        "keywords": ["career objective", "resume objective"],
        "answer": """**Sample career objective:**

"Motivated Computer Science engineering student interested in software development, Python and artificial intelligence. Eager to apply technical knowledge to real-world problems, strengthen problem-solving skills and contribute to a collaborative team."

Customize this to match your actual skills and the role you are applying for."""
    },
    {
        "topic": "Resume",
        "question": "How should I describe projects on my resume?",
        "keywords": ["project description", "resume projects", "project section"],
        "answer": """For each project, mention:

- **Project name:** A clear title
- **Purpose:** The problem it addresses
- **Technologies:** Languages, libraries and tools
- **Your contribution:** What you personally developed
- **Results:** Outcomes you actually tested

Be ready to explain your project during an interview."""
    },
    {
        "topic": "Interviews",
        "question": "How should I answer tell me about yourself?",
        "keywords": ["introduce yourself", "self introduction", "tell me about yourself"],
        "answer": """Use this structure:

1. Your name and education
2. Your technical interests
3. Your skills and learning journey
4. Your career goal

**Sample answer:**

"Hello, I am a Computer Science engineering student specializing in Artificial Intelligence and Machine Learning. I am interested in Python, software development and solving problems using technology. I am continuously improving my technical and communication skills through regular practice. My goal is to join a good organization where I can learn, contribute and grow as a software professional."

Speak naturally instead of memorizing every word."""
    },
    {
        "topic": "Interviews",
        "question": "How can I overcome interview nervousness?",
        "keywords": ["interview nervous", "interview fear", "confidence interview"],
        "answer": """To reduce interview nervousness:

- Practise your introduction aloud daily.
- Prepare answers to common questions.
- Record yourself and notice where you hesitate.
- Take a slow breath before answering.
- Listen carefully to the complete question.
- If you don't know something, be honest.

Regular practice builds confidence over time."""
    },
    {
        "topic": "Interviews",
        "question": "What are common HR interview questions?",
        "keywords": ["hr questions", "hr interview", "common interview questions"],
        "answer": """Prepare for these questions:

1. Tell me about yourself.
2. What are your strengths?
3. What skill are you currently improving?
4. Why should we hire you?
5. Why do you want to join this company?
6. Describe a challenge you faced.
7. Where do you see yourself in five years?
8. How do you handle teamwork?

Use genuine examples and keep your answers concise."""
    },
    {
        "topic": "Coding",
        "question": "How should a beginner learn Python?",
        "keywords": ["learn python", "python beginner", "python roadmap"],
        "answer": """Follow this order:

1. Variables, data types and input/output
2. Operators and conditions
3. Loops
4. Strings and lists
5. Tuples, sets and dictionaries
6. Functions
7. File handling and exceptions
8. Basic object-oriented programming
9. Small projects and coding problems

Write code yourself every day instead of only watching tutorials."""
    },
    {
        "topic": "Coding",
        "question": "How can I improve my problem-solving skills?",
        "keywords": ["problem solving", "coding logic", "logical thinking"],
        "answer": """Improve your problem-solving by:

- Starting with easy problems.
- Understanding input, output and constraints.
- Solving examples manually before coding.
- Writing the logic in simple steps.
- Testing normal and edge cases.
- Reviewing mistakes and trying again.

Practise conditions, loops, strings, arrays, searching and sorting."""
    },
    {
        "topic": "Coding",
        "question": "What is object-oriented programming?",
        "keywords": ["object oriented programming", "oops", "oop concepts"],
        "answer": """Object-oriented programming (OOP) organizes code using **classes and objects**.

Its four main principles are:

- **Encapsulation:** Bundling data and methods together.
- **Abstraction:** Hiding unnecessary implementation details.
- **Inheritance:** Creating a class based on another class.
- **Polymorphism:** Allowing the same interface or method name to behave differently.

For example, a `Car` class can define properties and methods, while individual cars are objects created from that class."""
    },
    {
        "topic": "Coding",
        "question": "Where can I practise coding?",
        "keywords": ["coding practice", "coding websites", "leetcode"],
        "answer": """Try these platforms:

- **HackerRank:** Beginner-friendly programming exercises.
- **CodeChef:** Programming problems and contests.
- **LeetCode:** Data structures, algorithms and interview preparation.
- **GeeksforGeeks:** Tutorials and coding practice.
- **Exercism:** Language-specific practice.

Start with easy Python questions and practise consistently."""
    },
    {
        "topic": "AI & ML",
        "question": "How do I start learning artificial intelligence and machine learning?",
        "keywords": ["learn ai", "learn machine learning", "ai ml roadmap"],
        "answer": """A beginner-friendly AI/ML roadmap:

1. Learn Python fundamentals.
2. Study basic statistics and linear algebra.
3. Practise NumPy, pandas and Matplotlib.
4. Learn supervised and unsupervised learning.
5. Study regression, classification and model evaluation.
6. Build projects using scikit-learn.
7. Learn Git and GitHub.
8. Explore deep learning and generative AI.

Focus on understanding concepts and building projects."""
    },
    {
        "topic": "AI & ML",
        "question": "What is the difference between AI, ML and deep learning?",
        "keywords": ["difference ai ml deep learning", "ai vs ml"],
        "answer": """- **Artificial Intelligence (AI):** The broad field of building systems that perform tasks associated with intelligence.
- **Machine Learning (ML):** A part of AI where systems learn patterns from data.
- **Deep Learning:** A part of ML that uses neural networks with multiple layers.

In short, deep learning is part of machine learning, and machine learning is part of AI."""
    },
    {
        "topic": "AI & ML",
        "question": "What beginner AI/ML projects can I build?",
        "keywords": ["ai ml project ideas", "machine learning projects"],
        "answer": """Beginner AI/ML project ideas:

1. Student placement prediction
2. Movie recommendation system
3. Spam message classification
4. House price prediction
5. Customer churn prediction
6. Sentiment analysis
7. Expense categorization

Choose a clear problem, use an appropriate dataset and explain your model's limitations."""
    },
    {
        "topic": "Placements",
        "question": "How should I prepare for campus placements?",
        "keywords": ["campus placement preparation", "placement roadmap"],
        "answer": """Prepare in four areas:

1. **Coding:** Programming fundamentals and basic data structures.
2. **Aptitude:** Percentages, ratios, reasoning and time management.
3. **Core subjects:** OOP, DBMS, operating systems and computer networks.
4. **Communication:** Self-introduction and project explanation.

Follow a weekly schedule, take mock tests and review your mistakes."""
    },
    {
        "topic": "Placements",
        "question": "What skills do IT companies expect from freshers?",
        "keywords": ["fresher skills", "it company skills", "placement skills"],
        "answer": """Many entry-level IT roles value:

- Programming fundamentals
- Problem-solving and basic DSA
- OOP and database basics
- Understanding of the role
- Communication and teamwork
- Ability to learn new tools
- Projects you can explain clearly

Requirements vary by company and role, so check each job description."""
    },
    {
        "topic": "Placements",
        "question": "How can I prepare for aptitude tests?",
        "keywords": ["aptitude preparation", "aptitude test", "quantitative aptitude"],
        "answer": """Start with:

1. Percentages, ratios and proportions
2. Averages, profit and loss
3. Time and work
4. Speed, distance and time
5. Simple and compound interest
6. Number series and logical reasoning
7. Syllogisms and blood relations

Learn the basics first, then practise shortcuts and timed questions."""
    },
    {
        "topic": "Communication",
        "question": "How can I improve my English speaking skills?",
        "keywords": ["improve english", "english speaking", "spoken english"],
        "answer": """Practise for 15–20 minutes every day:

- Speak about your day in English for five minutes.
- Read a short paragraph aloud.
- Listen to English conversations and repeat sentences.
- Learn useful phrases and use them in your own sentences.
- Record yourself and notice your progress.
- Practise interview answers with a friend.

Focus on clear sentences and confidence, not a perfect accent."""
    },
    {
        "topic": "Communication",
        "question": "How can I speak confidently in front of others?",
        "keywords": ["stage fear", "public speaking", "speaking confidence"],
        "answer": """Build confidence gradually:

1. Speak for one minute about a familiar topic.
2. Prepare three main points instead of memorizing a full speech.
3. Practise in front of a mirror or record yourself.
4. Speak slowly and pause between ideas.
5. Practise with friends and small groups.

Feeling nervous is normal. Confidence grows through repeated practice."""
    },
    {
        "topic": "Communication",
        "question": "How do I explain my project in an interview?",
        "keywords": ["explain project", "project interview", "project presentation"],
        "answer": """Explain your project in this order:

1. **Problem:** What issue were you solving?
2. **Solution:** What does your project do?
3. **Technology:** Which tools did you use?
4. **Your role:** What did you personally implement?
5. **Challenges:** What problems did you face?
6. **Results and limitations:** What worked, and what would you improve?

Prepare a one-minute explanation and practise follow-up questions."""
    },
]


# ---------------- SUGGESTED QUESTIONS ----------------
TOPIC_QUESTIONS = {
    "Internships": [
        "How can I find an internship?",
        "What skills are needed for an AI/ML internship?",
        "How do I prepare my internship application?",
    ],
    "Resume": [
        "How do I create a good resume as a student?",
        "What should I write in my career objective?",
        "How should I describe projects on my resume?",
    ],
    "Interviews": [
        "How should I answer tell me about yourself?",
        "How can I overcome interview nervousness?",
        "What are common HR interview questions?",
    ],
    "Coding": [
        "How should a beginner learn Python?",
        "How can I improve my problem-solving skills?",
        "Where can I practise coding?",
    ],
    "AI & ML": [
        "How do I start learning artificial intelligence and machine learning?",
        "What is the difference between AI, ML and deep learning?",
        "What beginner AI/ML projects can I build?",
    ],
    "Placements": [
        "How should I prepare for campus placements?",
        "What skills do IT companies expect from freshers?",
        "How can I prepare for aptitude tests?",
    ],
    "Communication": [
        "How can I improve my English speaking skills?",
        "How can I speak confidently in front of others?",
        "How do I explain my project in an interview?",
    ],
}


# ---------------- CHATBOT RESPONSE ----------------
def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s&]", " ", text)
    return re.sub(r"\s+", " ", text)


def answer_question(user_text):
    message = normalize(user_text)

    if not message:
        return "Please type a question so I can help you."

    # Greetings are checked first.
    greetings = {
        "hi", "hii", "hiii", "hiiii", "hello",
        "hey", "heyy", "good morning",
        "good afternoon", "good evening",
        "hi there", "hello there",
    }

    words = set(message.split())

    if message in greetings or (
        len(words) <= 3
        and words.intersection(
            {"hi", "hii", "hiii", "hiiii", "hello", "hey", "heyy"}
        )
    ):
        return (
            "Hii! 👋 Welcome to CareerBot!\n\n"
            "I can help you with internships, resumes, interviews, coding, "
            "AI/ML, placements and communication skills.\n\n"
            "Choose a topic above or ask me a career-related question. 😊"
        )

    if message in {"thanks", "thank you", "thank you so much", "thx", "ty"}:
        return "You're welcome! 😊 Ask me another question whenever you need help."

    if message in {"bye", "goodbye", "see you", "good night"}:
        return "Goodbye! 👋 Keep learning and practising. Come back whenever you need career guidance."

    if message in {"help", "what can you do", "what can you help with"}:
        return (
            "I can help you with internships, resumes, interviews, Python, "
            "AI/ML, placements, aptitude and communication skills. "
            "Choose a topic or type a specific question."
        )

    # Exact match.
    for item in FAQS:
        if message == normalize(item["question"]):
            return item["answer"]

    # Match related questions without guessing too aggressively.
    stop_words = {
        "how", "what", "why", "when", "where", "can", "could",
        "should", "do", "does", "is", "are", "the", "a", "an",
        "i", "my", "me", "to", "for", "of", "and", "in", "on",
        "please", "tell", "about", "you", "help"
    }

    user_words = set(message.split()) - stop_words
    best_item = None
    best_score = 0.0

    for item in FAQS:
        for candidate in [item["question"]] + item["keywords"]:
            candidate_text = normalize(candidate)
            candidate_words = set(candidate_text.split()) - stop_words

            similarity = difflib.SequenceMatcher(
                None, message, candidate_text
            ).ratio()

            overlap = 0.0
            if user_words and candidate_words:
                overlap = len(user_words & candidate_words) / max(
                    len(user_words), len(candidate_words)
                )

            score = max(similarity, overlap)

            if score > best_score:
                best_score = score
                best_item = item

    if best_item and best_score >= 0.48:
        return best_item["answer"]

    return (
        "I'm not completely sure what you mean yet. 😊\n\n"
        "Try asking about internships, resumes, interviews, Python, AI/ML, "
        "placements or communication skills.\n\n"
        "Example: **How can I prepare for campus placements?**"
    )


# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "Internships"

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ---------------- SIDEBAR ----------------
TOPIC_ICONS = {
    "Internships": "🎯",
    "Resume": "📄",
    "Interviews": "🎤",
    "Coding": "💻",
    "AI & ML": "🤖",
    "Placements": "🚀",
    "Communication": "💬",
}

with st.sidebar:
    st.markdown("## 💼 CareerBot")
    st.caption("Your career guidance assistant")
    st.divider()
    st.markdown("### Explore topics")

    for topic, icon in TOPIC_ICONS.items():
        if st.button(
            f"{icon}  {topic}",
            key=f"topic_{topic}",
            use_container_width=True,
        ):
            st.session_state.selected_topic = topic
            st.rerun()

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()


# ---------------- MAIN UI ----------------
# Welcome message and footer intentionally removed.
st.markdown("""
<div class="hero">
    <h1>Career guidance, made simpler.</h1>
    <p>Explore opportunities, build your skills, and prepare for your next career step.</p>
</div>
""", unsafe_allow_html=True)

selected_topic = st.session_state.selected_topic

st.markdown(
    f'<div class="section-title">{TOPIC_ICONS[selected_topic]} {selected_topic}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="small-label">Choose one of these three questions to get a quick answer.</div>',
    unsafe_allow_html=True,
)

columns = st.columns(3)

for index, question in enumerate(TOPIC_QUESTIONS[selected_topic]):
    with columns[index]:
        if st.button(
            question,
            key=f"question_{selected_topic}_{index}",
            use_container_width=True,
        ):
            st.session_state.pending_question = question
            st.rerun()


st.divider()


# ---------------- DISPLAY CONVERSATION ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Handle selected suggested question.
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    response = answer_question(question)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
    })

    st.rerun()


# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Ask CareerBot a question...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
    })

    response = answer_question(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
    })

    st.rerun()
