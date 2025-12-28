# Interview-Mate

**Your AI-Powered Career Mentor for Interview Preparation**

## Overview

Interview-Mate is an intelligent web application designed to help job seekers prepare for technical interviews and navigate their career paths. The application serves as a personalized AI mentor that guides users through domain exploration, role selection, and interview preparation with tailored roadmaps and resources.

The platform addresses the challenge of unstructured interview preparation by providing:
- Domain-specific career guidance
- Personalized learning roadmaps
- Real-time job listings
- AI-powered conversational mentorship
- Curated study resources

**Target Audience:** Job seekers, career changers, recent graduates, and professionals looking to transition into new technical roles.

## Key Features

- **AI-Powered Chat Interface**: Interactive conversation with an intelligent mentor that understands context and provides personalized guidance
- **Domain Exploration**: Explore multiple career domains including Data Science, Web Development, DevOps, Cybersecurity, and AI/ML
- **Role Recommendations**: Get suggested roles based on your skills, interests, or domain preferences
- **Personalized Roadmaps**: Generate 4-week structured learning roadmaps tailored to your selected role
- **Study Resources**: Access curated learning materials and resources specific to your career path
- **Live Job Listings**: Browse real-time job opportunities relevant to your selected role
- **Skill-Based Matching**: Automatic domain detection based on skills you mention
- **Domain History Tracking**: Keep track of domains you've explored for easy reference

## Tech Stack

- **Frontend Framework**: Streamlit (Python-based web framework)
- **Backend**: Python 3.x
- **AI Integration**: OpenAI API (GPT-4o-mini)
- **Job Search API**: RapidAPI (JSearch)
- **Environment Management**: python-dotenv
- **HTTP Client**: Requests library
- **Styling**: Custom CSS with gradient themes

## How It Works

1. **Initial Interaction**: Users start by chatting with Interview-Mate about their career interests, skills, or desired domain
2. **Domain Detection**: The application intelligently detects career domains from user input or skill mentions
3. **Role Suggestions**: Based on the selected domain, Interview-Mate presents relevant job roles with descriptions
4. **Role Selection**: Users choose a role that aligns with their career goals
5. **Roadmap Generation**: The AI generates a comprehensive 4-week learning roadmap with weekly goals
6. **Resource Provision**: Study resources and learning materials are provided for the selected role
7. **Job Discovery**: Real-time job listings are fetched and displayed for the selected role
8. **Ongoing Support**: Users can continue chatting for additional guidance and clarification

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- OpenAI API key
- RapidAPI key (optional, for job listings)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Interview-Mate.git
   cd Interview-Mate
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   - Create a `.env` file in the root directory
   - Add your API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     RAPIDAPI_KEY=your_rapidapi_key_here
     ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Access the application**
   - The application will automatically open in your default web browser
   - Default URL: `http://localhost:8501`

## Usage Instructions

### Getting Started

1. Launch the application using `streamlit run app.py`
2. In the chat interface, introduce yourself or mention your career interests
3. Examples of good starting messages:
   - "I'm interested in data science"
   - "I know Python and SQL"
   - "I want to become a frontend developer"

### Exploring Domains

- Mention any domain name (e.g., "data science", "web development", "cloud")
- The application will detect the domain and suggest relevant roles
- Click on any suggested role card to explore that career path

### Using Roadmaps

- After selecting a role, a 4-week roadmap is automatically generated
- Expand each week's section to view detailed goals and learning objectives
- Access study resources in the dedicated resources section

### Job Listings

- Job listings appear in the right sidebar after selecting a role
- Click "Refresh Jobs" to fetch the latest opportunities
- Use the "Apply" links to navigate to job postings

### Chat Features

- Ask questions about career paths, skills, or interview preparation
- Switch between domains by mentioning different career fields
- The conversation history is maintained throughout your session

## Folder Structure

```
Interview-Mate/
├── app.py                 # Main application file (Streamlit app)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── data/
│   ├── domains.json       # Career domain definitions
│   ├── roles.json         # Role mappings by domain
│   └── questions.json     # Sample interview questions
├── assets/                # Static assets (if any)
└── venv/                  # Virtual environment (gitignored)
```

## Future Enhancements

- **User Authentication**: Save user progress and preferences across sessions
- **Progress Tracking**: Track completion of roadmap milestones
- **Mock Interviews**: AI-powered mock interview sessions with feedback
- **Question Bank**: Expandable database of domain-specific interview questions
- **Performance Analytics**: Dashboard showing preparation progress and strengths
- **Resume Builder**: AI-assisted resume creation tailored to selected roles
- **Interview Scheduling**: Integration with calendar for interview reminders
- **Community Features**: Share roadmaps and resources with other users
- **Multi-language Support**: Support for multiple languages
- **Mobile Application**: Native mobile app for on-the-go preparation

## Contribution Guidelines

We welcome contributions to Interview-Mate. To contribute:

1. **Fork the repository** to your GitHub account
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the existing code style
4. **Test your changes** thoroughly before submitting
5. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "feat: add new feature description"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** with a detailed description of your changes

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular

### Reporting Issues

If you encounter bugs or have suggestions:
1. Check existing issues to avoid duplicates
2. Create a new issue with a clear title and description
3. Include steps to reproduce if reporting a bug
4. Add relevant labels if possible

## License

This project is licensed under the MIT License.

Copyright (c) 2024 Interview-Mate Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

