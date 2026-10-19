"""Apply the shared literal-argument contract to connection discovery."""
import test_search_wrapper


class TestConnectionsWrapper(test_search_wrapper.TestSearchWrapper):
    wrapper_name = "run_connections.sh"
    endpoint = "/connections?"
