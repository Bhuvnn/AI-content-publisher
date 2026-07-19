from langgraph.checkpoint.sqlite import SqliteSaver
from graph.thread import thread_id

checkpointer = SqliteSaver.from_conn_string(
    "checkpoints.db"
)
