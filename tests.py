import unittest

from solver import Solver, Car, VERTICAL, HORIZONTAL


class TestCar(unittest.TestCase):

    def test_init_horizontal(self):
        car = Car(
            orientantion=HORIZONTAL,
            character='A',
            start={'x': 0, 'y': 0},
            stop={'x': 2, 'y': 0}
        )
        self.assertEqual(len(car.get_points()), 3)

    def test_init_vertical(self):
        car = Car(
            orientantion=VERTICAL,
            character='A',
            start={'x': 1, 'y': 2},
            stop={'x': 1, 'y': 5}
        )
        self.assertEqual(len(car.get_points()), 4)

    def test_can_move(self):
        car = Car(
            orientantion=HORIZONTAL,
            character='A',
            start={'x': 0, 'y': 0},
            stop={'x': 2, 'y': 0}
        )
        matrix = [['.' for y in range(0, 6)] for x in range(0, 6)]

        self.assertTrue(car.can_move('right', 1, matrix))

        self.assertFalse(car.can_move('left', 1, matrix))
        self.assertFalse(car.can_move('up', 1, matrix))
        self.assertFalse(car.can_move('down', 1, matrix))


class TestSolver(unittest.TestCase):

    def test_no_red_car(self):

        board_str = '''
        ....AA
        ..BBCC
        ....EF
        GGHHEF
        ...IEF
        ...IJJ'''

        solver = Solver()
        with self.assertRaises(Exception) as context:
            solver.load_data(board_str)
        self.assertTrue('No red car found' in context.exception)

    def test_unsolvable(self):

        board_str = '''
        ....AA
        ..BBCF
        rr..EF
        GGHHEF
        ...IEF
        ...IJJ'''

        solver = Solver()
        solver.load_data(board_str)
        with self.assertRaises(Exception) as context:
            solver.solve()
        self.assertTrue('Can not solve' in context.exception)

    def test_solve6x6(self):

        board_str = '''
        ....AA
        ..BBCC
        rr..EF
        GGHHEF
        ...IEF
        ...IJJ'''

        solver = Solver()
        solver.load_data(board_str)
        moves = solver.solve()
        print solver.format_steps(solver.cars, moves)

    def test_solve6x6_2(self):

        board_str = '''
        aaobcc
        ..ob..
        rro...
        deeffp
        d..k.p
        hh.k.p
        '''

        solver = Solver()
        solver.load_data(board_str)
        moves = solver.solve()
        print solver.format_steps(solver.cars, moves)

    def test_solve8x7(self):
        """
        This test takes more time due to bigger board
        """

        board_str = '''
        ....AA..
        QZ......
        QZ......
        rr..EF..
        GGHHEF..
        ...IEF..
        ...IJJ..'''

        solver = Solver(size={'x': 8, 'y': 7})
        solver.load_data(board_str)
        moves = solver.solve()
        print solver.format_steps(solver.cars, moves)


if __name__ == '__main__':
    unittest.main()
