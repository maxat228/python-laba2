import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# noinspection PyUnresolvedReferences
from log_setup import log_command, setup_logging

class TestLogging:
    # Тесты для системы логирования

    def test_log_command_success(self, tmp_path):
        # Тест логирования успешной команды
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            setup_logging()
            log_command("test command", success=True)

            with open("shell.log", "r") as f:
                log_content = f.read()
                assert "test command" in log_content
                assert "ERROR" not in log_content
        finally:
            os.chdir(original_cwd)

    def test_log_command_error(self, tmp_path):
        # Тест логирования ошибки
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            setup_logging()
            log_command("test command", success=False, error_msg="test error")

            with open("shell.log", "r") as f:
                log_content = f.read()
                assert "ERROR" in log_content
                assert "test error" in log_content
        finally:
            os.chdir(original_cwd)
