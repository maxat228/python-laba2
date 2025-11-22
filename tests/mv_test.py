import os
from unittest.mock import patch, ANY
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
# noinspection PyUnresolvedReferences
from command_mv import mv

class TestCommandMV:
    # Тесты для команды mv

    def test_mv_file(self, tmp_path):
        # Тест перемещения файла
        source = tmp_path / "source.txt"
        source.write_text("content")
        destination = tmp_path / "dest.txt"

        with patch('command_mv.log_command') as mock_log:
            mv(str(source), str(destination))
            assert not source.exists()
            assert destination.exists()
            assert destination.read_text() == "content"
            mock_log.assert_called_once_with(f"mv {source} {destination}", success=True)

    def test_mv_rename_file(self, tmp_path):
        # Тест переименования файла
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            source = tmp_path / "old_name.txt"
            source.write_text("content")
            destination = "new_name.txt"

            with patch('command_mv.log_command') as mock_log:
                mv(str(source), destination)
                assert not source.exists()
                assert os.path.exists(destination)
                mock_log.assert_called_once_with(f"mv {source} {destination}", success=True)
        finally:
            os.chdir(original_cwd)

    def test_mv_nonexistent_source(self, tmp_path):
        # Тест перемещения несуществующего файла
        with patch('command_mv.log_command') as mock_log:
            mv("/nonexistent/source", str(tmp_path / "dest"))
            # Добавляем ANY для error_msg
            mock_log.assert_called_once_with("mv /nonexistent/source " + str(tmp_path / "dest"), success=False,
                                             error_msg=ANY)
