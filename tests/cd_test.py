import os
from unittest.mock import patch, ANY
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
# noinspection PyUnresolvedReferences
from command_cd import cd

class TestCommandCD:
    # Тесты для команды cd

    def test_cd_relative_path(self, tmp_path):
        # Тест cd с относительным путем
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            test_dir = tmp_path / "test_dir"
            test_dir.mkdir()

            with patch('command_cd.log_command') as mock_log:
                cd("test_dir")
                assert os.getcwd() == str(test_dir)
                mock_log.assert_called_once_with("cd test_dir", success=True)
        finally:
            os.chdir(original_cwd)

    def test_cd_absolute_path(self, tmp_path):
        # Тест cd с абсолютным путем
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        with patch('command_cd.log_command') as mock_log:
            cd(str(test_dir))
            mock_log.assert_called_once_with(f"cd {test_dir}", success=True)

    def test_cd_parent_directory(self, tmp_path):
        # Тест cd ..
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            test_dir = tmp_path / "test_dir"
            test_dir.mkdir()
            os.chdir(test_dir)

            with patch('command_cd.log_command') as mock_log:
                cd("..")
                assert os.getcwd() == str(tmp_path)
                mock_log.assert_called_once_with("cd ..", success=True)
        finally:
            os.chdir(original_cwd)

    def test_cd_home_directory(self):
        # Тест cd ~
        home_dir = os.path.expanduser("~")
        original_cwd = os.getcwd()

        try:
            with patch('command_cd.log_command') as mock_log:
                cd("~")
                assert os.getcwd() == home_dir
                mock_log.assert_called_once_with("cd ~", success=True)
        finally:
            os.chdir(original_cwd)

    def test_cd_nonexistent_directory(self):
        # Тест cd с несуществующей директорией
        with patch('command_cd.log_command') as mock_log:
            cd("/nonexistent/directory")
            # Добавляем ANY для error_msg
            mock_log.assert_called_once_with("cd /nonexistent/directory", success=False, error_msg=ANY)

    def test_cd_file_instead_of_directory(self, tmp_path):
        # Тест cd с путем к файлу
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        with patch('command_cd.log_command') as mock_log:
            cd(str(test_file))
            # Добавляем ANY для error_msg
            mock_log.assert_called_once_with(f"cd {test_file}", success=False, error_msg=ANY)
