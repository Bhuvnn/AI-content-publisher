from app.logger import get_logger
from agents.critic_agent import critic_agent
from agents.research_agent import research_agent
from agents.writer_agent import writer_agent
from graph.state import poemState
from services.topic_service import get_next_topic


logger = get_logger(__name__)


def topic_planner_node(state: poemState) -> poemState:
    logger.info("--- [NODE] Topic Planner ---")
    try:
        topic = get_next_topic()
        logger.info(f"Selected Topic: '{topic}'")
        return {"topic": topic}
    except Exception as e:
        logger.error(f"Error occurred in Topic Planner: {e}", exc_info=True)
        raise


def research_node(state: poemState) -> poemState:
    logger.info("--- [NODE] Research ---")
    logger.info(f"Researching topic: '{state['topic']}'...")

    research_content = research_agent(state["topic"])

    logger.info("Research completed successfully!")
    logger.info(f"  Core Idea: {research_content.get('core_idea', 'N/A')}")
    logger.info(f"  Themes: {', '.join(research_content.get('themes', []))}")
    logger.info(f"  Keywords: {', '.join(research_content.get('keywords', []))}")

    return {"research": research_content}


def content_generator_node(state: poemState) -> poemState:
    current_iteration = state["iteration"] + 1

    logger.info(f"--- [NODE] Content Generator (Iteration {current_iteration}) ---")
    logger.info("Generating content based on topic and research...")

    writing_content = writer_agent(
        state["topic"],
        state["research"],
        state.get("content"),
        state.get("critic"),
    )

    logger.info("Content generation completed!")
    logger.info(f"  Title: '{writing_content.get('title', 'N/A')}'")
    logger.info(f"  Content Preview:\n{writing_content.get('content', '')[:150]}...")
    return {"content": writing_content, "iteration": current_iteration}


def critic_node(state: poemState) -> poemState:
    logger.info(f"--- [NODE] Critic (Iteration {state['iteration']}) ---")
    logger.info("Evaluating generated content...")
    critic_content = critic_agent(state["topic"], state["research"], state["content"])
    logger.info("Critic evaluation completed!")
    logger.info(f"  Score: {critic_content.get('score', 'N/A')}/10")
    logger.info(f"  Feedback: {critic_content.get('feedback', 'N/A')}")
    return {"critic": critic_content}


def formatted_output_node(state: poemState) -> poemState:
    writer = state["content"]

    poem = writer["content"].replace("\\n", "\n")

    formatted = (
        f"📖 <b>{writer['title']}</b>\n\n"
        f"{poem}"
    )

    return {"formatted_content": formatted}


def publisher_node(state: poemState) -> poemState:
    pass
