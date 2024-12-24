from unittest import TestCase
from unittest.mock import Mock, patch, call

from mock import GPIO
from mock.ibs import IBS
from src.cleaning_robot import CleaningRobot, CleaningRobotError


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
        mock_ibs.return_value = 20
        system.initialize_robot()
        system.execute_command(system.FORWARD)
        self.assertEqual(system.robot_status(), "(0,1,N)")

    @patch.object(IBS, "get_charge_left")
    def test_move_right(self, mock_ibs: Mock):
        system = CleaningRobot()
        mock_ibs.return_value = 20
        system.initialize_robot()
        system.execute_command(system.RIGHT)
        self.assertEqual(system.robot_status(), "(0,0,E)")

    @patch.object(IBS, "get_charge_left")
    def test_move_left(self, mock_ibs: Mock):
        system = CleaningRobot()
        mock_ibs.return_value = 20
        system.initialize_robot()
        system.execute_command(system.LEFT)
        self.assertEqual(system.robot_status(), "(0,0,W)")

    @patch.object(IBS, "get_charge_left")
    def test_no_movement(self, mock_ibs: Mock):
        system = CleaningRobot()
        mock_ibs.return_value = 20
        system.initialize_robot()
        self.assertRaises(CleaningRobotError, system.execute_command, "X")

    # User Story 4
    @patch.object(IBS, "get_charge_left")
    @patch.object(GPIO, "input")
    def test_obstacle_found(self, mock_input: Mock, mock_ibs: Mock):
        system = CleaningRobot()
        system.initialize_robot()
        mock_ibs.return_value = 15
        mock_input.return_value = 1
        self.assertEqual(system.execute_command(system.FORWARD), "(0,0,N)(0,1)")

    # User Story 5
    @patch.object(IBS, "get_charge_left")
    def test_charge_left_equal_or_less_than_10(self, mock_ibs: Mock):
        system = CleaningRobot()
        system.initialize_robot()
        mock_ibs.return_value = 7
        system.pos_x = 1
        system.pos_y = 1
        system.heading = "N"
        system.manage_cleaning_system()
        self.assertEqual(system.execute_command(system.FORWARD), "!(1,1,N)")

    # User Story 6
    @patch.object(IBS, "get_charge_left")
    def test_return_to_start_position(self, mock_ibs: Mock):
        system = CleaningRobot()
        mock_ibs.return_value = 20
        system.initialize_robot()
        system.pos_x, system.pos_y = 2, 2
        system.return_to_start()
        self.assertEqual(system.robot_status(), "(0,0,N)")

    # User Story 7
    @patch.object(IBS, "get_charge_left")
    def test_adjusting_cleaning_intensity(self, mock_ibs: Mock):
        system = CleaningRobot()
        mock_ibs.return_value = 50
        system.initialize_robot()
        system.detect_dirt_level("low")
        system.execute_command("f")
        system.detect_dirt_level("high")
        system.execute_command("f")
        self.assertEqual(system.cleaning_speed, "slow")




