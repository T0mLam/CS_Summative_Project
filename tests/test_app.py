import unittest
from unittest.mock import patch
import tkinter as tk
from tkinter import messagebox
from graph_game.app import GraphGameGUI, Login, Register


class TestLogin(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.root = tk.Tk()
        self.login_frame = Login(parent=GraphGameGUI())

    def test_login_success(self):
        """test successful login"""
        self.login_frame.username_Entry.insert(0, "testuser")
        self.login_frame.password_Entry.insert(0, "testpass")

        with patch('graph_game_app.authenticate') as mocked_auth:
            mocked_auth.return_value = ("testuser", 100)
            self.login_frame.login()
            self.assertEqual(self.login_frame.parent.current_player, "testuser")
            self.assertEqual(self.login_frame.parent.current_balance, 100)
            mocked_auth.assert_called_with("testuser", "testpass")




class TestRegister(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.register_frame = Register(parent=GraphGameGUI())

    def test_register_success(self):
        """test successful register"""
        self.register_frame.username_Entry.insert(0, "newuser")
        self.register_frame.password_Entry.insert(0, "newpass")
        self.register_frame.password_repeat_Entry.insert(0, "newpass")

        with patch('graph_game_app.register_player') as mocked_register:
            self.register_frame.register()
            mocked_register.assert_called_with("newuser", "newpass", 100)
            self.assertEqual(self.register_frame.parent.current_player, "newuser")
            self.assertEqual(self.register_frame.parent.current_balance, 100)

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
