# AI-Powered Excel Mock Interviewer

A sophisticated AI-driven interview platform for assessing Microsoft Excel skills, built with Streamlit and Google Cloud APIs.

## 🚀 Features

- **AI-Powered Evaluation**: Uses Google's Gemini AI for intelligent answer assessment
- **Text-to-Speech Integration**: Questions are read aloud using Google Cloud TTS
- **Professional UI**: Clean, modern interface with progress tracking
- **Comprehensive Reporting**: Detailed performance analysis and recommendations
- **Interactive Experience**: Real-time feedback and conversational flow

## 📋 Prerequisites

1. **Google API Key**: Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Google Cloud Credentials**: Set up a service account for Text-to-Speech API
3. **Python 3.8+**: Ensure you have Python installed

## 🛠️ Setup Instructions

### 1. Clone and Setup Environment

\`\`\`bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

### 2. Configure Environment Variables

Create a `.env` file in the project root:

\`\`\`env
GOOGLE_API_KEY=your_gemini_api_key_here
\`\`\`

### 3. Setup Google Cloud TTS (Optional but Recommended)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Text-to-Speech API
4. Create a service account and download the JSON key file
5. Rename the key file to `google-credentials.json` and place it in the project root

### 4. Run the Application

\`\`\`bash
streamlit run app.py
\`\`\`

## 🎯 Usage

1. **Start Interview**: Click "Start Interview" on the welcome screen
2. **Answer Questions**: Provide detailed answers to Excel-related questions
3. **Listen to Audio**: Use the audio playback feature for accessibility
4. **Review Progress**: Track your performance in real-time
5. **Get Report**: Receive comprehensive feedback and recommendations

## 🏗️ Architecture

### Core Components

- **Question Bank**: Curated Excel interview questions with evaluation criteria
- **AI Evaluator**: Gemini-powered answer assessment with scoring
- **TTS Engine**: Google Cloud Text-to-Speech for audio questions
- **UI Framework**: Streamlit with custom CSS for professional appearance
- **State Management**: Session-based interview progress tracking

### Key Functions

- `evaluate_answer()`: AI-powered answer evaluation
- `text_to_speech()`: Convert questions to audio
- `generate_final_report()`: Comprehensive performance analysis
- `render_*()`: Modular UI components

## 🎨 Customization

### Adding New Questions

Edit the `QUESTION_BANK` list in `app.py`:

\`\`\`python
{
    "question": "Your Excel question here",
    "criteria": "Evaluation criteria for the perfect answer"
}
\`\`\`

### Modifying TTS Voice

Update the voice parameters in `text_to_speech()`:

\`\`\`python
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Neural2-F",  # Change voice type
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)
\`\`\`

### UI Styling

Modify the CSS in the `st.markdown()` section for custom styling.

## 🔧 Troubleshooting

### Common Issues

1. **TTS Not Working**: Ensure `google-credentials.json` is in the project root
2. **API Errors**: Check your Google API key in the `.env` file
3. **Import Errors**: Verify all dependencies are installed correctly

### Error Handling

The application includes comprehensive error handling:
- Graceful TTS fallback if credentials are missing
- AI evaluation fallback for API failures
- User-friendly error messages

## 📊 Performance Metrics

The system evaluates candidates on:
- Technical accuracy (40%)
- Explanation clarity (30%)
- Practical examples (20%)
- Advanced concepts (10%)

## 🚀 Deployment

### Local Development
\`\`\`bash
streamlit run app.py
\`\`\`

### Production Deployment
- **Streamlit Cloud**: Push to GitHub and deploy via Streamlit Cloud
- **Heroku**: Use the provided `requirements.txt` for deployment
- **Docker**: Create a Dockerfile for containerized deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google AI for Gemini API
- Google Cloud for Text-to-Speech API
- Streamlit for the amazing web framework
- Coding Ninjas for the inspiration

---

**Built with ❤️ for the Coding Ninjas AI Engineer Role**
