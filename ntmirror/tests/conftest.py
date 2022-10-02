#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import yaml

VERBOSE_CONNECTION = True

@pytest.fixture
def testout():
  return lambda fn: Path(__file__).parent / 'output' / fn

@pytest.fixture
def testdata():
  return lambda fn: Path(__file__).parent / 'testdata' / fn

@pytest.fixture
def testdatadir():
  return Path(__file__).parent / 'testdata'

@pytest.fixture
def script():
  return lambda fn: Path(__file__).parent.parent / 'bin' / fn

def get_config():
  config_file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
  if not os.path.exists(config_file_path):
    return None
  with open(config_file_path) as f:
    config = yaml.safe_load(f)
  return config

@pytest.fixture(scope="session")
def connection_string():
  config = get_config()
  if config is None:
    return None
  args = {k: v for k, v in config.items() if k in ['drivername',
                                           'host', 'port', 'database',
                                           'username', 'password']}
  if 'socket' in config:
    args['query'] = {'unix_socket': config['socket']}
  return URL.create(**args)

@pytest.fixture(scope="session")
def connection(connection_string):
  if connection_string is None:
    yield None
  else:
    engine = create_engine(connection_string, echo=VERBOSE_CONNECTION,
                           future=True)
    with engine.connect() as conn:
      with conn.begin():
        yield conn
        conn.commit()

@pytest.fixture(scope="session")
def mysql_connection_data():
  config = get_config()
  if config is None:
    return None
  return [config["host"], config["username"], config["password"],
          config["database"], config["socket"]]

@pytest.fixture(scope="session")
def connection_args():
  config = get_config()
  if config is None:
    return None
  return [config["username"],
          config["password"],
          config["database"],
          config["socket"]]
