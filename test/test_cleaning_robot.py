from unittest import TestCase
from unittest.mock import Mock, patch, call

from mock import GPIO
from mock.ibs import IBS
from src.cleaning_robot import CleaningRobot


class TestCleaningRobot(TestCase):

    # User Story 1
    def test_initialize_robot(self):
        system = CleaningRobot()
        system.initialize_robot()
        self.assertEqual(system.robot_status(), "(0,0,N)")

    # User Story 2
    @patch.object(IBS, "get_charge_left")
    @patch.object(GPIO, "output")
    def test_manage_cleaning_system_up_10(self, mock_led: Mock, mock_ibs: Mock):
        system = CleaningRobot()
        mock_ibs.return_value = 20
        system.manage_cleaning_system()
        mock_led.assert_has_calls([call(system.RECHARGE_LED_PIN, GPIO.LOW), call(system.CLEANING_SYSTEM_PIN, GPIO.HIGH)])

    @patch.object(IBS, "get_charge_left")
    @patch.object(GPIO, "output")
    def test_manage_cleaning_system_below_10(self, mock_led: Mock, mock_ibs: Mock):
        system = CleaningRobot()
        mock_ibs.return_value = 7
        system.manage_cleaning_system()
        mock_led.assert_has_calls([call(system.RECHARGE_LED_PIN, GPIO.HIGH), call(system.CLEANING_SYSTEM_PIN, GPIO.LOW)])

    # User Story 3
    @patch.object(IBS, "get_charge_left")
    def test_move_forward(self, mock_ibs: Mock):
        system = CleaningRobot()
        mock_ibs.return_value = 11
        system.initialize_robot()
        system.execute_command(system.FORWARD)
        self.assertEqual(system.robot_status(), "(0,1,N)")