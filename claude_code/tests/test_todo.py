"""Tests for the todo app."""

import os
import tempfile
import json
import shutil
import unittest

from todo_app.todo import TodoManager, Todo
from todo_app.storage import Storage


class TestTodoApp(unittest.TestCase):
    def setUp(self):
        # create a temporary directory for storage file
        self.temp_dir = tempfile.mkdtemp()
        self.file_path = os.path.join(self.temp_dir, "test_todos.json")
        self.storage = Storage(self.file_path)
        self.manager = TodoManager(self.storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_add_and_list(self):
        self.manager.add("Buy milk", "2 liters")
        self.manager.add("Read book")
        todos = self.manager.list()
        self.assertEqual(len(todos), 2)
        titles = {t.title for t in todos}
        self.assertSetEqual(titles, {"Buy milk", "Read book"})

    def test_complete(self):
        todo = self.manager.add("Write tests")
        result = self.manager.complete(todo.id)
        self.assertTrue(result)
        todos = self.manager.list(completed=True)
        self.assertEqual(len(todos), 1)
        self.assertTrue(todos[0].completed)

    def test_delete(self):
        todo = self.manager.add("Temporary task")
        self.assertTrue(self.manager.delete(todo.id))
        self.assertIsNone(self.manager.get(todo.id))

    def test_persistence(self):
        # Add a todo and ensure it is saved
        todo = self.manager.add("Persist me")
        # Create a new manager pointing to same file
        new_manager = TodoManager(Storage(self.file_path))
        todos = new_manager.list()
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].title, "Persist me")

    def test_corrupted_file(self):
        # Write invalid JSON
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("{invalid json}")
        # Manager should handle it gracefully
        manager = TodoManager(Storage(self.file_path))
        self.assertEqual(len(manager.list()), 0)


if __name__ == "__main__":
    unittest.main()
