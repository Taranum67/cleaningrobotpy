from unittest import TestCase
from unittest.mock import Mock, patch, call

from mock import GPIO
from mock.ibs import IBS
from src.cleaning_robot import CleaningRobot


class TestCleaningRobot(TestCase):

    #User Story 1
    def test_initialize_robot(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        self.assertEqual(robot.pos_x, 0)
        self.assertEqual(robot.pos_y, 0)
        self.assertEqual(robot.heading, 'N')

    def test_robot_status(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        status = robot.robot_status()
        self.assertEqual(status, "(0,0,N)")

    def test_robot_status_after_update(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        robot.pos_x = 2
        robot.pos_y = 3
        robot.heading = 'S'
        status = robot.robot_status()
        self.assertEqual(status, "(2,3,S)")



