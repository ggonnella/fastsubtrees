def pytest_addoption(parser):
    parser.addoption(
        "--subtree_id",
        action='append',
        help="id of the node to test the value on (must be string)"
    ),
    parser.addoption(
        '--parent',
        action='append',
    ),
    parser.addoption(
        '--node_number',
        action='append'
    ),
    parser.addoption(
        '--delete_node_number',
        action='append'
    )

def pytest_generate_tests(metafunc):
    if "subtree_id" in metafunc.fixturenames:
        metafunc.parametrize("subtree_id", metafunc.config.getoption("subtree_id"))
    if "parent" in metafunc.fixturenames:
        metafunc.parametrize("parent", metafunc.config.getoption("parent"))
    if "node_number" in metafunc.fixturenames:
        metafunc.parametrize("node_number", metafunc.config.getoption("node_number"))
    if "delete_node_number" in metafunc.fixturenames:
        metafunc.parametrize("delete_node_number", metafunc.config.getoption("delete_node_number"))