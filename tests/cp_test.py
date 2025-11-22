import os
from unittest.mock import patch, ANY
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
# noinspection PyUnresolvedReferences
from command_cp import cp

class TestCommandCP:
    # Тесты для команды cp

    def test_cp_file(self, tmp_path):
        # Тест копирования файла
        source = tmp_path / "source.txt"
        source.write_text("test content")
        destination = tmp_path / "dest.txt"

        with patch('command_cp.log_command') as mock_log:
            cp(str(source), str(destination))
            assert destination.exists()
            assert destination.read_text() == "test content"
            # Исправляем формат строки - добавляем пробел
            mock_log.assert_called_once_with(f"cp  {source} {destination}", success=True)

    def test_cp_directory_without_recursive(self, tmp_path):
        # Тест копирования директории без -r
        source_dir = tmp_path / "source"
        source_dir.mkdir()

        with patch('command_cp.log_command') as mock_log:
            cp(str(source_dir), str(tmp_path / "dest"))
            # Добавляем пробел и ANY для error_msg
            mock_log.assert_called_once_with(f"cp  {source_dir} {tmp_path / 'dest'}", success=False, error_msg=ANY)

    def test_cp_directory_with_recursive(self, tmp_path):
        # Тест копирования директории с -r
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file.txt").write_text("content")
        dest_dir = tmp_path / "dest"

        with patch('command_cp.log_command') as mock_log:
            cp(str(source_dir), str(dest_dir), recursive=True)
            assert dest_dir.exists()
            assert (dest_dir / "file.txt").exists()
            # Исправляем формат строки
            mock_log.assert_called_once_with(f"cp -r {source_dir} {dest_dir}", success=True)

    def test_cp_nonexistent_source(self, tmp_path):
        # Тест копирования несуществующего источника
        with patch('command_cp.log_command') as mock_log:
            cp("/nonexistent/source", str(tmp_path / "dest"))
            # Добавляем пробел и ANY для error_msg
            mock_log.assert_called_once_with("cp  /nonexistent/source " + str(tmp_path / "dest"), success=False,
                                             error_msg=ANY)
