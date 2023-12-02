from typing import TypeVar

StateT = TypeVar('StateT')
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx

runtime = get_instance()
session_id = get_script_run_ctx().session_id
session_info = runtime._session_mgr.get_session_info(session_id)
def persistent_game_state(initial_state: StateT) -> StateT:
    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
    session = runtime._session_mgr.get_session_info(session_id).session
    # session_id = get_report_ctx().session_id
    # session = st.server.server.Server.get_current()._get_session_info(session_id).session
    if not hasattr(session, '_gamestate'):
        setattr(session, '_gamestate', initial_state)
    return session._gamestate
