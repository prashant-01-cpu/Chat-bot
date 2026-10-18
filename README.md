AI Career Guidance Chatbot
A web-based AI chatbot that helps students explore careers, identify skills to learn, and plan practical next steps. It uses Flask for the backend and the Groq API to generate responses with a Llama 3.1 model.
Project status: Educational/demo project. The chatbot provides general career guidance, not guaranteed admissions, employment, or professional advice.

Features
- Career conversations: Ask about roles, skills, learning resources, and next steps.
- Step-by-step roadmaps: Request a career roadmap and confirm to receive a five-stage plan.
- AI-powered answers: Uses Groq chat completions with llama-3.1-8b-instant by default.
- Environment-based configuration: API keys and session secrets stay out of source code.
- Separate chat sessions: Browsers have isolated, temporary conversation histories in the development server.
- Simple Flask interface: Serves the frontend from templates/ and static/ and exposes a JSON chat endpoint.
Current limitation: Roadmaps are text-based; the project does not yet generate pictorial/graphical roadmaps. Conversation history is stored temporarily in server memory and is not persistent across restarts or multiple server processes.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Run locally
1. Prerequisites
- Python 3.10+
- Git
- A Groq API key from Groq Console
2. Clone the repository
git clone https://github.com/prashant-01-cpu/Chat-bot.git
cd Chat-bot
3. Create and activate a virtual environment
macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate
Windows PowerShell:
py -m venv .venv
.venv\Scripts\Activate.ps1
4. Install dependencies
python -m pip install -r requirements.txt
5. Configure environment variables
macOS/Linux:
cp .env.example .env
Windows PowerShell:
Copy-Item .env.example .env
Edit .env and set:
GROQ_API_KEY=your_new_groq_api_key_here
FLASK_SECRET_KEY=your_long_random_secret_here
GROQ_MODEL=llama-3.1-8b-instant
Generate a strong Flask session secret with:
python -c "import secrets; print(secrets.token_hex(32))"
6. Start the app
python main.py
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Security and responsible deployment
- Keep credentials in environment variables, not in Python, HTML, JavaScript, screenshots, or commits.
- Commit .env.example but never .env.
- Revoke/rotate any previously exposed Groq API key. .gitignore does not remove secrets from old Git commits.
- Review your full Git history before making the repository public; follow GitHub's guide to removing sensitive data if credentials were committed.
- Do not enable Flask's debugger on a publicly accessible server.
- For actual internet deployment, use a production WSGI server and HTTPS; set SESSION_COOKIE_SECURE=True, add authentication/rate limiting and provider usage limits, and replace the in-memory chat cache with a shared session store (or use a stateless API).
- Be careful about recording or sharing user conversations, which may contain personal details.
Future improvements
- Personalized roadmaps with diagrams or downloadable images
- Persistent conversation history using a database
- Career recommendations based on skills and interests
- Better input safeguards and usage controls for hosted deployments
- Automated tests and deployment configuration
Contributions
Issues and pull requests are welcome. Please avoid including real API keys, tokens, or private conversation data in submissions.
