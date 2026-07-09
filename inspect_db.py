"""Script to inspect what's inside the database"""

from database.database import SessionLocal
from database.models import Poem

db = SessionLocal()

try:
    poems = db.query(Poem).all()
    
    print(f"\n{'='*80}")
    print(f"Total poems in database: {len(poems)}")
    print(f"{'='*80}\n")
    
    if poems:
        for poem in poems:
            print(f"ID: {poem.id}")
            print(f"Topic: {poem.topic}")
            print(f"Title: {poem.title}")
            print(f"Content: {poem.content[:100]}...")
            print(f"Score: {poem.critic_score}")
            print(f"Iteration: {poem.iteration}")
            print(f"Telegram Message ID: {poem.telegram_message_id}")
            print(f"Generated at: {poem.generated_at}")
            print(f"{'-'*80}\n")
    else:
        print("Database is empty!\n")
        
finally:
    db.close()
