import unittest
from unittest.mock import Mock, ANY, patch
from io import StringIO
from repositories.reference_repository import ReferenceRepository
from app import App
from services.reference_service import ReferenceService
from console_io import ConsoleIO
from database_connection import get_db_connection


class TestApp(unittest.TestCase):
    def setUp(self):
        self._io_mock = Mock()
        self._reference_repository_mock = Mock(
            wraps=ReferenceRepository("connection"))
        self.app = App(self._io_mock, self._reference_repository_mock)
        self.mock_io = Mock()
        self.mock_rs = Mock()
        self.testApp = App(self.mock_io, self.mock_rs)
        self.testApp.write_columns = Mock()


    def test_app_creates_empty_list(self):
        self.assertEqual(len(self.app.list), 0)

    def test_run_stops_with_enter(self):
        self._io_mock.read.return_value = ""
        self.app.run()
        self._io_mock.write.assert_called_with(ANY)
        self._io_mock.write.assert_called_with(ANY)

    def test_run_help_works(self):
        self._io_mock.read.side_effect = ["help", ""]
        self.app.run()
        self.assertEqual(self._io_mock.write.call_count, 10)

    def test_list_references_gets_list(self):
        self.book1 = Mock()
        self.book2 = Mock()
        self.test_list = [self.book1, self.book2]
        self.mock_rs.get_all.return_value = self.test_list
        self.testApp.list_references()

        self.mock_rs.get_all.assert_called()

    def test_list_references_calls_io_write(self):
        self.book1 = Mock()
        self.book2 = Mock()
        self.test_list = [self.book1, self.book2]
        self.mock_rs.get_all.return_value = self.test_list
        self.testApp.list_references()

        self.mock_io.write.assert_called_with(self.test_list[1])

    def test_delete_reference_cancels_when_command_is_given(self):
        self.mock_io.read.return_value = "cancel"
        self.testApp.delete_reference()

        self.mock_rs.ref_key_taken.assert_not_called()

    def test_delete_reference_asks_for_confirmation_and_cancels_when_wrong_input(self):
        self.mock_io.read.return_value = 123
        self.mock_rs.ref_key_taken.return_value = True
        self.mock_rs.get_book_by_ref_key.return_value = "reference"
        self.testApp.delete_reference()

        self.mock_rs.delete_book_by_ref_key.assert_not_called()
        self.mock_io.write.assert_called_with("Deletion cancelled")

    def test_delete_reference_with_wrong_ref_key(self):
        self.mock_io.read.return_value = 123
        self.mock_rs.ref_key_taken.return_value = False
        self.mock_rs.get_book_by_ref_key.return_value = "reference"
        self.testApp.delete_reference()

        self.mock_rs.get_book_by_ref_key.assert_not_called()

    def test_delete_reference_with_acceptable_ref_key(self):
        self.mock_io.read.side_effect = [123, "y"]
        self.mock_rs.ref_key_taken.return_value = True
        self.mock_rs.get_book_by_ref_key.return_value = "reference"
        self.mock_rs.delete_book_by_ref_key.return_value = True
        self.testApp.delete_reference()

        self.mock_rs.delete_book_by_ref_key.assert_called_with(123)
        self.mock_io.write.assert_called_with("DELETED!")

    def test_delete_reference_problem_deleting_from_db(self):
        self.mock_io.read.side_effect = [123, "y"]
        self.mock_rs.ref_key_taken.return_value = True
        self.mock_rs.get_book_by_ref_key.return_value = "reference"
        self.mock_rs.delete_book_by_ref_key.return_value = False
        self.testApp.delete_reference()

        self.mock_rs.delete_book_by_ref_key.assert_called_with(123)
        self.mock_io.write.assert_called_with(
            "Something went wrong with deleting the reference")

    def test_command_add_calls_add_reference(self):
        self.testApp.add_reference = Mock()
        self.mock_io.read.side_effect = ["add", ""]
        self.testApp.run()

        self.testApp.add_reference.assert_called_once()

    def test_command_delete_calls_delete_reference(self):
        self.testApp.delete_reference = Mock()
        self.mock_io.read.side_effect = ["delete", ""]
        self.testApp.run()

        self.testApp.delete_reference.assert_called_once()

    def test_command_list_calls_delete_references(self):
        self.testApp.list_references = Mock()
        self.mock_io.read.side_effect = ["list", ""]
        self.testApp.run()

        self.testApp.list_references.assert_called_once()

    @patch('builtins.input', side_effect=['book', "ref", "auth", "title", "year", "publisher"])
    def test_add_reference(self, input):
        console_io = ConsoleIO()
        connection = get_db_connection()
        reference_repository = ReferenceRepository(connection)
        reference_service = ReferenceService(reference_repository)
        self.testApp = App(console_io, reference_service)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.testApp.add_reference()

            printed_output = mock_stdout.getvalue().strip()

            expected_output_lines = [
                'Type "cancel" to cancel',
                "ADDED!"
            ]

            for expected_line in expected_output_lines:
                self.assertIn(expected_line, printed_output)

    def test_add_reference_with_empty_user_input(self):
        self.mock_io.read.side_effect = ["book", " ", "aa"]
        self.mock_rs.get_fields_of_reference_type.return_value = ["title"]
        self.mock_rs.create_reference.return_value = False
        self.testApp.add_reference()

        self.mock_io.write.assert_called_with("This field is required!")

    def test_add_reference_with_taken_re_key(self):
        self.mock_io.read.side_effect = ["book", "1", "2"]
        self.mock_rs.get_fields_of_reference_type.return_value = ["ref_key"]
        self.mock_rs.create_reference.return_value = False
        self.mock_rs.ref_key_taken.side_effect = [True, False]
        self.testApp.add_reference()

        self.mock_io.write.assert_called_with("This ref_key is already taken!!")
