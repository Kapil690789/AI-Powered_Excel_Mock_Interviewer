import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import base64
from google.cloud import texttospeech
import io
import time
from datetime import datetime
import uuid
import pandas as pd

# --- SECURE CONFIGURATION LOADING ---
# def load_credentials():
#     """Securely load credentials from environment or Streamlit secrets"""
#     try:
#         # Force load .env file first for local development
#         current_dir = os.getcwd()
#         env_path = os.path.join(current_dir, '.env')
        
#         # Try multiple .env locations
#         env_locations = [env_path, './.env', '../.env']
#         for location in env_locations:
#             if os.path.exists(location):
#                 load_dotenv(location)
#                 break
        
#         # Get API key from environment first
#         api_key = os.getenv("GOOGLE_API_KEY")
        
#         # If not found in env, try Streamlit secrets
#         if not api_key:
#             try:
#                 if hasattr(st, 'secrets') and len(st.secrets) > 0:
#                     api_key = st.secrets.get("GOOGLE_API_KEY")
                    
#                     # Handle Google Cloud credentials if available
#                     if api_key and "gcp_service_account" in st.secrets:
#                         gcp_creds = dict(st.secrets["gcp_service_account"])
#                         with open("google-credentials.json", "w") as f:
#                             json.dump(gcp_creds, f)
#                         os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "google-credentials.json"
#             except:
#                 pass
        
#         # Set Google Cloud credentials path from .env if available
#         if api_key:
#             credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
#             if credentials_path:
#                 # Handle relative path
#                 if credentials_path.startswith('./'):
#                     credentials_path = os.path.join(current_dir, credentials_path[2:])
                
#                 if os.path.exists(credentials_path):
#                     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        
#         return api_key
        
#     except Exception as e:
#         return None
# --- SECURE CONFIGURATION AND CREDENTIALS SETUP ---
def setup_credentials():
    """
    Sets up credentials for both local and deployed environments.
    - For local: Relies on a .env file.
    - For deployment: Reads Streamlit secrets, creates a temporary credentials file,
      and sets the necessary environment variables.
    """
    # First, try to load the .env file for local development
    load_dotenv()

    # Check if the app is running on Streamlit Cloud
    if hasattr(st, 'secrets'):
        # If on Streamlit Cloud, get secrets
        gcp_creds_dict = dict(st.secrets.get("gcp_service_account"))
        api_key = st.secrets.get("GOOGLE_API_KEY")

        if gcp_creds_dict:
            # Create a temporary credentials file from secrets
            with open("google-credentials.json", "w") as f:
                json.dump(gcp_creds_dict, f)
            # Set the environment variable to this new file
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "google-credentials.json"
        
        if api_key:
            # Set the Gemini API key
            genai.configure(api_key=api_key)

# Call the setup function right at the top of your script
setup_credentials()

# --- CONFIGURATION ---
# This section is now much simpler as setup_credentials() handles everything.
model = genai.GenerativeModel('gemini-1.5-flash')
ENABLE_TTS = os.getenv("ENABLE_TTS", "true").lower() == "true"
# --- CONFIGURATION ---

# --- ENHANCED QUESTION BANK WITH DIFFICULTY LEVELS ---
QUESTION_BANK = [
    {
        "question": "Explain the VLOOKUP function in Excel. What are its main arguments and when would you use it?",
        "criteria": "A good answer should mention that VLOOKUP searches for a value in the first column of a table. It must correctly identify the four arguments: lookup_value, table_array, col_index_num, and range_lookup. Should mention use cases like finding employee details or product prices.",
        "difficulty": "Beginner",
        "category": "Lookup Functions"
    },
    {
        "question": "What is a Pivot Table and why is it useful? Can you describe the process of creating one?",
        "criteria": "The user should explain that a Pivot Table is a tool to summarize and analyze large datasets. Key benefits to mention are data aggregation, finding patterns, and creating reports without complex formulas. Should describe the basic creation process.",
        "difficulty": "Intermediate",
        "category": "Data Analysis"
    },
    {
        "question": "Describe the difference between the SUM and SUMIF functions. Provide an example scenario for each.",
        "criteria": "The answer must state that SUM adds all numbers in a range, while SUMIF adds numbers based on a specific condition or criteria. An example would make this answer stronger, like summing sales by region.",
        "difficulty": "Beginner",
        "category": "Formula Logic"
    },
    {
        "question": "How would you remove duplicate values from a column in Excel? What are the different methods available?",
        "criteria": "The user should describe the 'Remove Duplicates' feature found in the Data tab. They should explain that you select the column(s) and Excel removes rows with duplicate values. Bonus points for mentioning conditional formatting or advanced filters.",
        "difficulty": "Intermediate",
        "category": "Data Management"
    },
    {
        "question": "Explain INDEX and MATCH functions. How do they work together and what advantages do they have over VLOOKUP?",
        "criteria": "Should explain that INDEX returns a value from a specific position and MATCH finds the position of a value. Together they're more flexible than VLOOKUP - can look left, handle column insertions, and are more efficient for large datasets.",
        "difficulty": "Advanced",
        "category": "Advanced Lookup"
    },
    {
        "question": "What are Excel macros and VBA? When would you use them in a business context?",
        "criteria": "Should explain that macros are recorded sequences of actions and VBA is the programming language behind them. Use cases include automating repetitive tasks, creating custom functions, and building interactive dashboards. Should mention security considerations.",
        "difficulty": "Advanced",
        "category": "Automation"
    }
]

# --- ENHANCED TEXT-TO-SPEECH FUNCTIONS ---
# @st.cache_data
# def text_to_speech(text):
#     """Convert text to speech using Google Cloud TTS with enhanced error handling"""
#     if not ENABLE_TTS:
#         return None
        
#     try:
#         # Check if credentials are available
#         credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
#         if not credentials_path or not os.path.exists(credentials_path):
#             return None
            
#         # Initialize the TTS client
#         client = texttospeech.TextToSpeechClient()
        
#         # Set the text input to be synthesized
#         synthesis_input = texttospeech.SynthesisInput(text=text)
        
#         # Build the voice request with professional settings
#         voice = texttospeech.VoiceSelectionParams(
#             language_code="en-US",
#             name="en-US-Neural2-J",  # Professional male voice for interviews
#             ssml_gender=texttospeech.SsmlVoiceGender.MALE
#         )
        
#         # Select the type of audio file with optimized settings
#         audio_config = texttospeech.AudioConfig(
#             audio_encoding=texttospeech.AudioEncoding.MP3,
#             speaking_rate=0.9,  # Slightly slower for clarity
#             pitch=-2.0,  # Slightly deeper for professionalism
#             volume_gain_db=1.0
#         )
        
#         # Perform the text-to-speech request
#         response = client.synthesize_speech(
#             input=synthesis_input, voice=voice, audio_config=audio_config
#         )
        
#         return response.audio_content
#     except Exception as e:
#         # Silently fail and disable TTS for this session
#         return None
# --- ENHANCED TEXT-TO-SPEECH FUNCTIONS ---
@st.cache_data
def text_to_speech(text):
    """Convert text to speech using Google Cloud TTS with enhanced error handling"""
    if not ENABLE_TTS:
        return None
        
    try:
        # Initialize the TTS client. It will automatically find the credentials
        # from the environment variable set by setup_credentials().
        client = texttospeech.TextToSpeechClient()
        
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-J",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        
        # Select the type of audio file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.9,
            pitch=-2.0,
            volume_gain_db=1.0
        )
        
        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        return response.audio_content
    except Exception as e:
        # If any error occurs, it will be caught here.
        print(f"TTS Error: {e}")
        return None

def play_question_audio(question_text):
    """Generate and play audio for the question with enhanced UX"""
    audio_content = text_to_speech(f"Interview Question: {question_text}")
    if audio_content:
        st.audio(audio_content, format='audio/mp3', autoplay=False)
        return True
    return False

# --- ADVANCED AI EVALUATION FUNCTIONS ---
def evaluate_answer_advanced(question, criteria, user_answer, difficulty, category):
    """Enhanced AI evaluation with context-aware scoring"""
    prompt = f"""
    You are a senior Excel expert and hiring manager conducting a professional technical interview 
    for a {difficulty.lower()}-level Excel position focusing on {category}.
    
    **Question Context:**
    - Question: "{question}"
    - Difficulty Level: {difficulty}
    - Category: {category}
    - Expected Criteria: "{criteria}"
    
    **Candidate's Answer:**
    "{user_answer}"
    
    **Evaluation Instructions:**
    1. Assess the answer based on the difficulty level and category
    2. Consider technical accuracy, practical examples, and depth of understanding
    3. Provide constructive feedback that helps the candidate improve
    4. Score considering the difficulty level (Advanced questions require deeper knowledge)
    
    **Response Format (separated by '|||'):**
    1. **Detailed Feedback:** Professional, constructive feedback (2-3 sentences)
    2. **Score:** Integer from 1 to 5
    3. **Key Strength:** One specific strength demonstrated (1 sentence)
    4. **Improvement Tip:** One specific suggestion for improvement (1 sentence)
    
    Example:
    Excellent explanation of VLOOKUP's core functionality! You correctly identified all four arguments and provided a practical business example. However, mentioning VLOOKUP's limitation of only searching the first column would demonstrate deeper technical understanding.|||4|||Strong grasp of function syntax and practical applications|||Consider discussing function limitations to show expert-level knowledge
    """
    
    try:
        response = model.generate_content(prompt)
        parts = response.text.strip().split('|||')
        if len(parts) >= 4:
            return parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip()
        elif len(parts) >= 2:
            return parts[0].strip(), parts[1].strip(), "Good technical understanding", "Keep practicing for improvement"
        else:
            return response.text.strip(), "3", "Shows effort in answering", "Focus on providing more detailed explanations"
    except Exception as e:
        st.error(f"Error evaluating answer: {e}")
        return "Could not evaluate the answer due to technical issues.", "0", "Unable to assess", "Please try again"

def generate_comprehensive_report(interview_summary, candidate_info=None):
    """Generate detailed final interview report with analytics"""
    total_score = sum(int(entry.get('score', 0)) for entry in interview_summary)
    max_score = len(interview_summary) * 5
    percentage = (total_score / max_score) * 100 if max_score > 0 else 0
    
    # Category-wise analysis
    categories = {}
    for entry in interview_summary:
        category = entry.get('category', 'General')
        if category not in categories:
            categories[category] = {'total': 0, 'count': 0}
        categories[category]['total'] += int(entry.get('score', 0))
        categories[category]['count'] += 1
    
    category_analysis = {cat: data['total']/data['count'] for cat, data in categories.items()}
    
    prompt = f"""
    You are a Senior Technical Hiring Manager at a Fortune 500 company. Generate a comprehensive 
    Excel skills assessment report based on the interview performance below.
    
    **PERFORMANCE METRICS:**
    - Total Questions: {len(interview_summary)}
    - Overall Score: {total_score}/{max_score} ({percentage:.1f}%)
    - Category Performance: {json.dumps(category_analysis, indent=2)}
    
    **DETAILED INTERVIEW TRANSCRIPT:**
    {json.dumps(interview_summary, indent=2)}
    
    **REPORT REQUIREMENTS:**
    Generate a professional assessment report with the following sections:
    
    **EXECUTIVE SUMMARY** (2-3 sentences)
    Overall assessment of candidate's Excel proficiency level and readiness for the role.
    
    **PERFORMANCE ANALYSIS**
    - Technical Competency Score: X/10
    - Communication Clarity Score: X/10
    - Practical Application Score: X/10
    
    **CATEGORY BREAKDOWN**
    Analyze performance in each question category with specific insights.
    
    **KEY STRENGTHS** (3-4 bullet points)
    Specific strengths demonstrated during the interview.
    
    **DEVELOPMENT AREAS** (3-4 bullet points)
    Areas for improvement with specific suggestions.
    
    **HIRING RECOMMENDATION**
    One of: Strong Hire | Hire | Consider with Training | No Hire
    Provide clear justification for your recommendation.
    
    **LEARNING ROADMAP**
    Specific next steps and resources for the candidate's Excel skill development.
    
    Make the report professional, actionable, and encouraging while being honest about areas for improvement.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating report: {e}")
        return "Could not generate the comprehensive report due to technical issues."

# --- ANALYTICS AND TRACKING ---
def save_interview_transcript(interview_data):
    """Save interview transcript for analytics and improvement"""
    transcript = {
        'session_id': str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat(),
        'interview_data': interview_data,
        'total_score': sum(int(entry.get('score', 0)) for entry in interview_data),
        'completion_rate': len(interview_data) / len(QUESTION_BANK) * 100
    }
    
    # Save to session state for download
    st.session_state.transcript = transcript
    return transcript

# --- ENHANCED UI COMPONENTS ---
def render_header():
    """Render enhanced application header with logo and title"""
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        try:
            st.image("codingninja.jpeg", width=100)
        except:
            st.markdown("🏢 **CODING NINJAS**")
    
    with col2:
        st.markdown("""
        # 🎯 AI-Powered Excel Mock Interviewer
        ### *Professional Skills Assessment Platform*
        """)
    
    with col3:
        st.markdown("**Powered by AI** 🤖")

def render_progress_dashboard(current_question, total_questions, interview_summary):
    """Enhanced progress dashboard with analytics"""
    progress = current_question / total_questions if total_questions > 0 else 0
    
    # Progress bar
    st.progress(progress)
    
    # Metrics dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Progress", f"{current_question}/{total_questions}")
    
    with col2:
        if interview_summary:
            avg_score = sum(int(entry.get('score', 0)) for entry in interview_summary) / len(interview_summary)
            st.metric("Avg Score", f"{avg_score:.1f}/5")
        else:
            st.metric("Avg Score", "-")
    
    with col3:
        if interview_summary:
            total_score = sum(int(entry.get('score', 0)) for entry in interview_summary)
            st.metric("Total Points", f"{total_score}/{len(interview_summary)*5}")
        else:
            st.metric("Total Points", "0/0")
    
    with col4:
        completion_percentage = progress * 100
        st.metric("Completion", f"{completion_percentage:.0f}%")

def render_question_card(question_item, question_number, total_questions):
    """Enhanced question card with metadata"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    ">
        <h2>📝 Question {question_number} of {total_questions}</h2>
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
            <h3>{question_item["question"]}</h3>
        </div>
        <div style="display: flex; gap: 1rem; font-size: 0.9em; opacity: 0.9;">
            <span>🎯 Difficulty: {question_item.get("difficulty", "Standard")}</span>
            <span>📂 Category: {question_item.get("category", "General")}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_interview_history(interview_summary):
    """Enhanced interview history with detailed analytics"""
    if not interview_summary:
        return
    
    st.subheader("📊 Interview Performance Dashboard")
    
    # Summary metrics
    total_score = sum(int(entry.get('score', 0)) for entry in interview_summary)
    avg_score = total_score / len(interview_summary)
    
    # Performance by category
    categories = {}
    for entry in interview_summary:
        category = entry.get('category', 'General')
        if category not in categories:
            categories[category] = []
        categories[category].append(int(entry.get('score', 0)))
    
    # Category performance chart
    if categories:
        st.markdown("#### Performance by Category")
        category_data = {cat: sum(scores)/len(scores) for cat, scores in categories.items()}
        
        col1, col2 = st.columns([2, 1])
        with col1:
            # Display as a simple bar chart using metrics
            for category, score in category_data.items():
                st.metric(f"{category}", f"{score:.1f}/5", delta=f"{score-3:.1f}" if score != 3 else None)
        
        with col2:
            st.markdown("**Legend:**")
            st.markdown("- 🟢 4.0+ : Excellent")
            st.markdown("- 🟡 3.0+ : Good") 
            st.markdown("- 🔴 <3.0 : Needs Work")
    
    st.divider()
    
    # Detailed question review
    st.markdown("#### Detailed Question Review")
    for i, entry in enumerate(interview_summary):
        score = int(entry.get('score', 0))
        score_emoji = "🟢" if score >= 4 else "🟡" if score >= 3 else "🔴"
        difficulty = entry.get('difficulty', 'Standard')
        
        with st.expander(f"{score_emoji} Q{i+1}: {entry['question'][:60]}... | {difficulty} | Score: {score}/5"):
            st.markdown("**Your Answer:**")
            st.info(entry['user_answer'])
            
            st.markdown("**AI Feedback:**")
            st.success(entry['feedback'])
            
            if entry.get('strength'):
                st.markdown("**Key Strength:**")
                st.write(f"✅ {entry['strength']}")
            
            if entry.get('improvement'):
                st.markdown("**Improvement Tip:**")
                st.write(f"💡 {entry['improvement']}")

# --- MAIN APPLICATION LOGIC ---
def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="AI Excel Interviewer - Professional Assessment",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Enhanced CSS styling
    st.markdown("""
    <style>
    .main {
        padding: 1rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
        st.session_state.interview_summary = []
        st.session_state.interview_finished = False
        st.session_state.interview_started = False
        st.session_state.start_time = None
    
    # Render header
    render_header()
    
    # Main routing logic
    if not st.session_state.interview_started:
        render_welcome_screen()
    elif st.session_state.interview_finished:
        render_completion_screen()
    else:
        render_active_interview()

def render_welcome_screen():
    """Enhanced welcome screen with better UX"""
    st.markdown("---")
    
    # Introduction section
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ## 👋 Welcome to Your Professional Excel Assessment!
        
        This AI-powered interview platform evaluates your Microsoft Excel skills through 
        interactive technical questions, providing real-time feedback and comprehensive 
        performance analysis.
        
        ### 🎯 What You'll Experience:
        - **6 comprehensive questions** covering core Excel concepts
        - **AI-powered evaluation** with detailed, constructive feedback  
        - **Real-time audio playback** for enhanced accessibility
        - **Professional assessment report** with personalized recommendations
        - **Category-wise performance analysis** for targeted learning
        
        ### 💡 Success Tips:
        - Provide detailed explanations with practical examples
        - Mention specific Excel features and their business applications
        - Don't worry about perfect answers - we value understanding and thought process
        - Take your time to think through each response
        
        **⏱️ Estimated Duration:** 15-20 minutes
        """)
    
    with col2:
        st.markdown("### 📋 Assessment Categories")
        
        categories = set(q.get('category', 'General') for q in QUESTION_BANK)
        difficulties = set(q.get('difficulty', 'Standard') for q in QUESTION_BANK)
        
        st.info(f"""
        **Topics Covered:**
        {chr(10).join('• ' + cat for cat in sorted(categories))}
        
        **Difficulty Levels:**
        {chr(10).join('• ' + diff for diff in sorted(difficulties))}
        
        **Scoring:**
        • 5 = Excellent
        • 4 = Good  
        • 3 = Average
        • 2 = Below Average
        • 1 = Needs Improvement
        """)
        
        if ENABLE_TTS and os.path.exists(os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')):
            st.success("🔊 Audio features enabled")
        else:
            st.warning("🔇 Audio features disabled")
    
    st.markdown("---")
    
    # Start button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🚀 Begin Assessment", type="primary", use_container_width=True):
            st.session_state.interview_started = True
            st.session_state.start_time = datetime.now()
            st.rerun()

def render_active_interview():
    """Enhanced active interview interface"""
    idx = st.session_state.current_question_index
    
    # Progress dashboard
    render_progress_dashboard(idx, len(QUESTION_BANK), st.session_state.interview_summary)
    st.markdown("---")
    
    # Interview history
    render_interview_history(st.session_state.interview_summary)
    
    # Current question
    if idx < len(QUESTION_BANK):
        question_item = QUESTION_BANK[idx]
        
        # Enhanced question display
        render_question_card(question_item, idx + 1, len(QUESTION_BANK))
        
        # Audio section
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 🎤 Audio Playback")
        with col2:
            if st.button("🔊 Play Question", use_container_width=True):
                with st.spinner("Generating audio..."):
                    audio_success = play_question_audio(question_item["question"])
                    if not audio_success:
                        st.info("📝 Audio unavailable - please read the question above")
        
        # Answer input section
        st.markdown("### ✍️ Your Response")
        user_answer = st.text_area(
            "Provide your detailed answer:",
            height=200,
            key=f"answer_{idx}",
            placeholder="Share your knowledge about this Excel concept. Include examples, use cases, and any relevant details you think are important..."
        )
        
        # Action buttons
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("⏭️ Skip Question", use_container_width=True):
                # Allow skipping with a default answer
                process_answer(question_item, "Question skipped by candidate", idx, skipped=True)
        
        with col3:
            if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                if user_answer.strip():
                    process_answer(question_item, user_answer, idx)
                else:
                    st.warning("⚠️ Please provide an answer or use the Skip option.")
    else:
        st.session_state.interview_finished = True
        st.rerun()

def process_answer(question_item, user_answer, idx, skipped=False):
    """Enhanced answer processing with better UX"""
    # AI interaction simulation
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        
        if skipped:
            thinking_placeholder.write("📝 Question skipped - moving to next question...")
            time.sleep(1)
            
            # Add skipped entry
            st.session_state.interview_summary.append({
                "question": question_item["question"],
                "user_answer": "Question skipped",
                "feedback": "Question was skipped - no evaluation available",
                "score": "0",
                "category": question_item.get("category", "General"),
                "difficulty": question_item.get("difficulty", "Standard"),
                "strength": "N/A",
                "improvement": "Consider attempting similar questions in practice"
            })
        else:
            thinking_placeholder.write("🤔 Analyzing your response in detail...")
            time.sleep(1.5)
            
            # Enhanced AI evaluation
            with st.spinner("Evaluating your answer..."):
                feedback, score, strength, improvement = evaluate_answer_advanced(
                    question_item["question"],
                    question_item["criteria"], 
                    user_answer,
                    question_item.get("difficulty", "Standard"),
                    question_item.get("category", "General")
                )
            
            thinking_placeholder.write("✅ Analysis complete!")
            
            # Store enhanced results
            st.session_state.interview_summary.append({
                "question": question_item["question"],
                "user_answer": user_answer,
                "feedback": feedback,
                "score": score,
                "category": question_item.get("category", "General"),
                "difficulty": question_item.get("difficulty", "Standard"),
                "strength": strength,
                "improvement": improvement
            })
            
            # Show immediate feedback
            st.success(f"**AI Feedback:** {feedback}")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Score:** {score}/5")
            with col2:
                score_int = int(score) if score.isdigit() else 0
                if score_int >= 4:
                    st.success("🎉 Excellent work!")
                elif score_int >= 3:
                    st.info("👍 Good job!")
                else:
                    st.warning("💪 Keep practicing!")
    
    # Move to next question
    st.session_state.current_question_index += 1
    time.sleep(2)  # Brief pause to read feedback
    st.rerun()

def render_completion_screen():
    """Enhanced completion screen with comprehensive analytics"""
    # Celebration
    st.balloons()
    
    # Calculate completion time
    if st.session_state.start_time:
        completion_time = datetime.now() - st.session_state.start_time
        time_taken = f"{completion_time.total_seconds() / 60:.1f} minutes"
    else:
        time_taken = "Unknown"
    
    # Header
    st.markdown("## 🎉 Assessment Complete!")
    st.markdown(f"**Congratulations!** You've completed the Excel skills assessment in {time_taken}.")
    
    # Save transcript
    transcript = save_interview_transcript(st.session_state.interview_summary)
    
    # Quick stats
    total_score = sum(int(entry.get('score', 0)) for entry in st.session_state.interview_summary)
    max_score = len(st.session_state.interview_summary) * 5
    percentage = (total_score / max_score) * 100 if max_score > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Score", f"{total_score}/{max_score}")
    with col2:
        st.metric("Percentage", f"{percentage:.1f}%")
    with col3:
        st.metric("Questions", len(st.session_state.interview_summary))
    with col4:
        st.metric("Time Taken", time_taken)
    
    # Generate comprehensive report
    with st.spinner("Generating your comprehensive performance report..."):
        final_report = generate_comprehensive_report(st.session_state.interview_summary)
    
    st.markdown("---")
    st.markdown("## 📊 Your Comprehensive Performance Report")
    st.markdown(final_report)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 New Assessment", use_container_width=True):
            # Reset all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    with col2:
        # Download detailed report
        report_data = {
            'session_info': {
                'completion_time': time_taken,
                'total_score': f"{total_score}/{max_score}",
                'percentage': f"{percentage:.1f}%"
            },
            'detailed_report': final_report,
            'interview_transcript': st.session_state.interview_summary,
            'generated_at': datetime.now().isoformat()
        }
        
        st.download_button(
            "📄 Download Report",
            json.dumps(report_data, indent=2),
            file_name=f"excel_assessment_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col3:
        # Share functionality placeholder
        if st.button("🔗 Share Results", use_container_width=True):
            st.info("Feature coming soon! For now, you can download your report.")
    
    with col4:
        # Feedback link
        if st.button("🌟 Rate Platform", use_container_width=True):
            st.success("Thank you for your interest! Visit codingninjas.com for more resources.")
    
    # Additional resources
    st.markdown("---")
    st.markdown("### 📚 Recommended Learning Resources")
    
    # Get lowest scoring categories for recommendations
    categories_performance = {}
    for entry in st.session_state.interview_summary:
        category = entry.get('category', 'General')
        score = int(entry.get('score', 0))
        if category not in categories_performance:
            categories_performance[category] = []
        categories_performance[category].append(score)
    
    # Calculate average scores per category
    avg_category_scores = {
        cat: sum(scores)/len(scores) 
        for cat, scores in categories_performance.items()
    }
    
    # Show improvement recommendations
    improvement_areas = [cat for cat, avg in avg_category_scores.items() if avg < 3.5]
    
    if improvement_areas:
        st.info(f"💡 **Focus Areas for Improvement:** {', '.join(improvement_areas)}")
        
        # Specific recommendations based on categories
        recommendations = {
            'Lookup Functions': "Practice VLOOKUP, INDEX-MATCH, and XLOOKUP with real datasets",
            'Data Analysis': "Work on Pivot Tables, charts, and data summarization techniques", 
            'Formula Logic': "Master logical functions like IF, AND, OR, and nested formulas",
            'Data Management': "Learn data cleaning, sorting, filtering, and validation techniques",
            'Advanced Lookup': "Focus on complex lookup scenarios and array formulas",
            'Automation': "Explore VBA basics and macro recording for repetitive tasks"
        }
        
        for area in improvement_areas:
            if area in recommendations:
                st.markdown(f"**{area}:** {recommendations[area]}")
    else:
        st.success("🎉 Excellent performance across all categories! Consider exploring advanced Excel features like Power Query and Power Pivot.")

if __name__ == "__main__":
    main()