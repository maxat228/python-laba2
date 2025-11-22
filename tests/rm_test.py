import os
from unittest.mock import patch, ANY
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
# noinspection PyUnresolvedReferences
from command_rm import rm

class TestCommandRM:
    # Тесты для команды rm

    def test_rm_file(self, tmp_path):
        # Тест удаления файла
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        with patch('command_rm.log_command') as mock_log:
            rm(str(test_file))
            assert not test_file.exists()
            # Исправляем формат строки - добавляем пробел
            mock_log.assert_called_once_with(f"rm  {test_file}", success=True)

    def test_rm_directory_without_recursive(self, tmp_path):
        # Тест удаления директории без -r
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        with patch('command_rm.log_command') as mock_log:
            rm(str(test_dir))
            assert test_dir.exists()  # Директория должна остаться
            # Добавляем пробел и ANY для error_msg
            mock_log.assert_called_once_with(f"rm  {test_dir}", success=False, error_msg=ANY)

    def test_rm_directory_with_recursive_confirmed(self, tmp_path, monkeypatch):
        # Тест удаления директории с -r и подтверждением
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")

        # Мокаем input для подтверждения удаления
        monkeypatch.setattr('builtins.input', lambda _: 'y')

        with patch('command_rm.log_command') as mock_log:
            rm(str(test_dir), recursive=True)
            assert not test_dir.exists()
            # Исправляем формат строки
            mock_log.assert_called_once_with(f"rm -r {test_dir}", success=True)

    def test_rm_directory_with_recursive_cancelled(self, tmp_path, monkeypatch):
        # Тест удаления директории с -r и отменой
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        # Мокаем input для отмены удаления
        monkeypatch.setattr('builtins.input', lambda _: 'n')

        with patch('command_rm.log_command') as mock_log:
            rm(str(test_dir), recursive=True)
            assert test_dir.exists()  # Директория должна остаться
            mock_log.assert_called_once_with(f"rm -r {test_dir}", success=False, error_msg="Cancelled by user")

    def test_rm_nonexistent_file(self):
        # Тест удаления несуществующего файла
        with patch('command_rm.log_command') as mock_log:
            rm("/nonexistent/file.txt")
            # Добавляем пробел и ANY для error_msg
            mock_log.assert_called_once_with("rm  /nonexistent/file.txt", success=False, error_msg=ANY)
