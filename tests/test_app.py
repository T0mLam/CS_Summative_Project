import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from graph_game.app import GraphGameGUI, Login, Register, Play

class TestGraphGameGUI(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.app = GraphGameGUI()
        self.app.frames['login'] = Login(self.app)
        self.app.frames['register'] = Register(self.app)
        self.app.frames['play'] = Play(self.app)

    def tearDown(self):
        self.app.destroy()

    def test_login_success(self):
        """test login success"""
        with patch('graph_game.db.database.authenticate') as mocked_auth:
            mocked_auth.return_value = ('testuser', 100)
            self.app.frames['login'].username_Entry.insert(0, 'testuser')
            self.app.frames['login'].password_Entry.insert(0, 'password')
            self.app.frames['login'].login()
            mocked_auth.assert_called_with('testuser', 'password')
            self.assertEqual(self.app.current_player, 'testuser')
            self.assertEqual(self.app.current_balance, 100)
            self.assertTrue(isinstance(self.app.frames['login'].master.current_frame, tk.Frame))

    def test_login_failure(self):
        """test login fails"""
        with patch('graph_game.db.database.authenticate') as mocked_auth:
            mocked_auth.return_value = False
            self.app.frames['login'].username_Entry.insert(0, 'wronguser')
            self.app.frames['login'].password_Entry.insert(0, 'wrongpass')
            self.app.frames['login'].login()
            mocked_auth.assert_called_with('wronguser', 'wrongpass')
            self.assertIsNone(self.app.current_player)
            self.assertIsNone(self.app.current_balance)
            self.assertFalse(isinstance(self.app.frames['login'].master.current_frame, tk.Frame))

    def test_register_success(self):
        """test register"""
        with patch('graph_game.db.database.authenticate') as mocked_register:
            mocked_register.return_value = True
            self.app.frames['register'].username_Entry.insert(0, 'newuser')
            self.app.frames['register'].password_Entry.insert(0, 'newpass')
            self.app.frames['register'].password_repeat_Entry.insert(0, 'newpass')
            self.app.frames['register'].register()
            mocked_register.assert_called_with('newuser', 'newpass', 100)
            self.assertEqual(self.app.current_player, 'newuser')
            self.assertEqual(self.app.current_balance, 100)

    def test_register_failure(self):
        """test register fail"""
        self.app.frames['register'].username_Entry.insert(0, 'newuser')
        self.app.frames['register'].password_Entry.insert(0, 'newpass')
        self.app.frames['register'].password_repeat_Entry.insert(0, 'wrongpass')
        self.app.frames['register'].register()
        self.assertIsNone(self.app.current_player)
        self.assertIsNone(self.app.current_balance)

    def test_initial_conditions(self):
        """test initial conditions"""
        self.assertTrue(self.app.frames['play'].game_started)
        self.assertEqual(self.app.frames['play'].bid_scale['state'], 'normal')

    def test_game_flow(self):
        """test game flow"""
        self.app.frames['play'].starting_node_combobox.set('1')
        self.app.frames['play'].ending_node_combobox.set('2')
        self.app.frames['play'].bid_scale.set(50)
        with patch('graph_game.app.GraphGame.check_player_wins') as mocked_win_check:
            mocked_win_check.return_value = True
            self.app.frames['play'].bet_start_game()
            self.assertTrue(isinstance(self.app.frames['play'].master.current_frame, tk.Frame))
            self.assertFalse(self.app.frames['play'].game_started)

if __name__ == '__main__':
    unittest.main()
