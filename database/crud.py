from database.database import SessionLocal
from database.models import Poem


def save_poem(result: dict, telegram_message_id: int) -> None:
    db = SessionLocal()

    try:
        poem = Poem(
            topic=result["topic"],
            title=result["content"]["title"],
            content=result["content"]["content"],
            critic_score=result["critic"]["score"],
            iteration=result["iteration"],
            telegram_message_id=telegram_message_id,
        )

        db.add(poem)
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_recent_topics(limit: int = 10) -> list[str]:
    db = SessionLocal()
    try:
        poems = db.query(Poem).order_by(Poem.id.desc()).limit(limit).all()
        return [poem.topic for poem in poems]
    except Exception:
        return []
    finally:
        db.close()