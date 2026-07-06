from graph.state import poemState
from services.topic_service import get_next_topic
from agents.research_agent import research_agent
from agents.writer_agent import writer_agent
from agents.critic_agent import critic_agent


def topic_planner_node(state: poemState) -> poemState:
    print("\n--- [NODE] Topic Planner ---")
    try:
        topic=get_next_topic()
        print(f"Selected Topic: '{topic}'")
        return {"topic":topic}
    except Exception as e:
        print(f"[ERROR] Error occurred in Topic Planner: {e}")
        raise

def research_node(state: poemState) -> poemState:
    print("\n--- [NODE] Research ---")
    print(f"Researching topic: '{state['topic']}'...")
    research_content=research_agent(state["topic"])
    print("Research completed successfully!")
    print(f"  Core Idea: {research_content.get('core_idea', 'N/A')}")
    print(f"  Themes: {', '.join(research_content.get('themes', []))}")
    print(f"  Keywords: {', '.join(research_content.get('keywords', []))}")
    return {"research":research_content}

def content_generator_node(state: poemState) -> poemState:
    current_iteration = state["iteration"] + 1
    print(f"\n--- [NODE] Content Generator (Iteration {current_iteration}) ---")
    print("Generating content based on topic and research...")
    writing_content=writer_agent(state["topic"], state["research"],state.get("content"), state.get("critic"))
    print("Content generation completed!")
    print(f"  Title: '{writing_content.get('title', 'N/A')}'")
    print(f"  Content Preview:\n{writing_content.get('content', '')[:150]}...")
    return {"content": writing_content, "iteration": current_iteration}

def critic_node(state: poemState) -> poemState:
    print(f"\n--- [NODE] Critic (Iteration {state['iteration']}) ---")
    print("Evaluating generated content...")
    critic_content=critic_agent(state["topic"],state["research"], state["content"])
    print("Critic evaluation completed!")
    print(f"  Score: {critic_content.get('score', 'N/A')}/10")
    print(f"  Feedback: {critic_content.get('feedback', 'N/A')}")
    return {"critic":critic_content}


def formatted_output_node(state: poemState) -> poemState:
    pass

def publisher_node(state: poemState) -> poemState:
    pass