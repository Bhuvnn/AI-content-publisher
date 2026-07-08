import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
API_KEY = os.getenv("GROQ_API_KEY")
MAX_ITERATIONS = 3

BASE_URL = "https://api.groq.com/openai/v1"
WRITER_MODEL = "llama-3.3-70b-versatile"
CRITIC_MODEL = "llama-3.1-8b-instant"
RESEARCH_MODEL = "llama-3.3-70b-versatile"
TOPIC_GENERATOR_MODEL = "llama-3.1-8b-instant"

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


TELEGRAM_HELP_MESSAGE = """🤖 <b>AI Content Publisher</b>

Generate original AI-crafted poetry directly from Telegram.

<b>Available Commands</b>

• <code>/start</code>
View the welcome message.

• <code>/write &lt;topic&gt;</code>
Generate a poem based on your idea.

Example: <code>/write A lonely lighthouse waiting for the sunrise</code>

• <code>/help</code>
Display this help message.

<b>After Generation</b>

Once your poem is ready, you'll see three options:

✅ <b>Publish</b> – Publish the poem to the Telegram channel.

🔄 <b>Regenerate</b> – Create an improved version of the poem.

❌ <b>Cancel</b> – Discard the generated poem.

Happy writing! ✨

"""