import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
YAML_PATH="topics.yaml"
COOLDOWN_DAYS = 7
MAX_ITERATIONS = 3

BASE_URL = "https://api.groq.com/openai/v1"
WRITER_MODEL = "llama-3.3-70b-versatile"
CRITIC_MODEL = "llama-3.1-8b-instant"
RESEARCH_MODEL = "llama-3.1-8b-instant"

TELEGRAM_WELCOME_MESSAGE ="""
🤖 <b>Welcome, {user}!</b>

I'm your <b>AI Content Generation Assistant</b>.

Send me:
• 💡 An idea
• 📝 A topic
• 📖 A rough outline
• ✨ Or just a random thought

I'll:
🔍 Research it
✍️ Generate high-quality content
🧐 Critique and refine it
🚀 Prepare it for publishing

<i>Simply send your first idea to begin.</i>
"""