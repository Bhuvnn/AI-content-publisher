from langgraph.graph import START,END,StateGraph
from graph.state import poemState
from graph.nodes import topic_planner_node, research_node, content_generator_node, critic_node, formatted_output_node, publisher_node
from app.config import MAX_ITERATIONS
from app.logger import get_logger

logger = get_logger(__name__)

graph=StateGraph(poemState)

def should_rewrite(state: poemState):
    iteration = state["iteration"]
    score = state["critic"]["score"]
    logger.info("--- [ROUTE DECISION] Evaluating rewrite condition ---")
    logger.info(f"  Current Iteration: {iteration} (Max allowed: {MAX_ITERATIONS})")
    logger.info(f"  Critic Score: {score}/10")
    
    if iteration >= MAX_ITERATIONS:
        logger.info("  Decision: Max iterations reached. Proceeding to END.")
        return False
        
    if score < 8:
        logger.info(f"  Decision: Score {score} < 8. Routing back to 'content_generator' to rewrite content.")
        return True
    else:
        logger.info(f"  Decision: Score {score} >= 8. Content is satisfactory. Proceeding to END.")
        return False


graph.add_node("topic_planner", topic_planner_node)
graph.add_node("research", research_node)
graph.add_node("content_generator", content_generator_node)
graph.add_node("critic", critic_node)
# graph.add_node("formatted_output", formatted_output_node)
# graph.add_node("publisher", publisher_node)

# graph.add_edge(START, "topic_planner")
graph.add_edge(START, "research")
graph.add_edge("research", "content_generator")
graph.add_edge("content_generator", "critic")
graph.add_conditional_edges("critic", should_rewrite,{True:"content_generator", False:END})
# graph.add_edge("critic", "formatted_output")
# graph.add_edge("formatted_output", "publisher")

workflow=graph.compile()

result=workflow.invoke({"topic":"Im sitting under a tree and I see a bird flying in the sky", "iteration": 0})
logger.info(f"Workflow execution result:\n{result}")