from copy import deepcopy

VERTICAL = 'vertical'
HORIZONTAL = 'horizontal'
SIZE = {'x': 6, 'y': 6}

class WrongInputException(Exception):
    pass


class CanNonSolveException(Exception):
    pass


class Car(object):
    orientantion = None # VERTICAL or HORIZONTAL
    character = None
    start = None # {'x': x, 'y': y}
    stop = None # {'x': x, 'y': y}
    is_red_car = None # red car we need to free out

    def __init__(
            self, orientantion, character, start, stop, is_red_car=None):
        self.orientantion = orientantion
        self.character = character
        self.start = start
        self.stop = stop
        self.is_red_car = is_red_car

    def get_points(self):
        """
        Returns set of points that car takes
        """
        points = []
        car = self
        x_start, y_start = car.start['x'], car.start['y']
        x_stop, y_stop = car.stop['x'], car.stop['y']
        character = car.character
        if self.orientantion == VERTICAL:
            for y in range(y_start, y_stop+1):
                points.append({'x': x_start, 'y': y, 'character': character})
        if self.orientantion == HORIZONTAL:
            for x in range(x_start, x_stop+1):
                points.append({'x': x, 'y': y_start, 'character': character})

        return points

    def can_move(self, direction, length, matrix):

        flag = True

        if self.orientantion == HORIZONTAL:
            if direction in ['up', 'down']:
                flag = False

        if self.orientantion == VERTICAL:
            if direction in ['left', 'right']:
                flag = False

        # check if there are some other cars on the way
        # or board ending
        car = deepcopy(self)
        car.move(direction, length)
        for point in car.get_points():
            if point['y'] < 0 or point['x'] < 0:
                flag = False
            try:
                character = matrix[point['y']][point['x']]
                if character != '.' and character != self.character:
                    flag = False
            except IndexError:
                flag = False
        del car

        return flag

    def move(self, direction, length):
        if direction == 'up':
            self.start['y'] -= length
            self.stop['y'] -= length

        if direction == 'down':
            self.start['y'] += length
            self.stop['y'] += length

        if direction == 'left':
            self.start['x'] -= length
            self.stop['x'] -= length

        if direction == 'right':
            self.start['x'] += length
            self.stop['x'] += length

    def __repr__(self):
        return "{} ({}->{})".format(self.character, self.start, self.stop)


class Solver(object):

    def __init__(self, size={'x': 6, 'y': 6}):
        super(Solver, self).__init__()
        self.size = size
        self.cars = []
        self.steps = []

    def generate_cars_vertical(self, matrix):
        """
        Go through line by line and generate cars
        """
        data = []
        for x in range(self.size['x']):
            car_data = {'character': None}
            for y in range(self.size['y']):
                item = matrix[y][x]

                if item != car_data['character'] or y == self.size['y'] - 1:
                    # We have start/stop point here
                    if car_data['character']:
                        car_data['stop'] = {'x': x, 'y': y-1}
                        if y == self.size['y'] - 1 and item == car_data['character']:
                            car_data['stop'] = {'x': x, 'y': y}

                        if car_data['stop']['y'] - car_data['start']['y'] > 0:
                            if car_data['character'] != '.':
                                car_obj = Car(
                                    VERTICAL,
                                    car_data['character'],
                                    car_data['start'],
                                    car_data['stop'],
                                    is_red_car=(car_data['character'] == 'r')
                                )
                                self.cars.append(car_obj)

                    car_data = {
                        'start': {'x': x, 'y': y},
                        'character': item,
                    }

    def generate_cars_horizontal(self, matrix):
        """
        Go through line by line and generate cars
        """
        data = []
        for y, line in enumerate(matrix):
            car_data = {'character': None}
            for x, item in enumerate(line):
                if item != car_data['character'] or x == self.size['x'] - 1:
                    # We have start/stop point here
                    if car_data['character']:
                        car_data['stop'] = {'x': x-1, 'y': y}
                        if x == self.size['x'] - 1 and item == car_data['character']:
                            car_data['stop'] = {'x': x, 'y': y}

                        if car_data['stop']['x'] - car_data['start']['x'] > 0:
                            if car_data['character'] != '.':
                                car_obj = Car(
                                    HORIZONTAL,
                                    car_data['character'],
                                    car_data['start'],
                                    car_data['stop'],
                                    is_red_car=(car_data['character'] == 'r')
                                )
                                self.cars.append(car_obj)

                    car_data = {
                        'start': {'x': x, 'y': y},
                        'character': item,
                    }

    def str_to_matrix(self, init_data):
        matrix = []
        for line in init_data.split("\n"):
            line = line.replace(' ', '')
            if not line:
                continue
            matrix_line = []
            for item in line:
                matrix_line.append(item)
            matrix.append(line)
        return matrix
 
    def load_data(self, init_data):
        """
        We assume that there is no case 
        when car be readed as vertical and horizontal at the same time
        Also we assume that ther is no cars on the way of red car that can't be moved to side
        """
        matrix = self.str_to_matrix(init_data)
        self.generate_cars_horizontal(matrix)
        self.generate_cars_vertical(matrix)
        self.check_data(self.cars)

    def check_data(self, cars):
        """
        - check if red car on board
        - check if we have only cars in size > 1
        - check if it's possible to have solution
        """
        if not filter(lambda x: x.is_red_car, cars):
            raise WrongInputException("No red car found")

        if filter(lambda car: len(list(car.get_points())) < 2, cars):
            raise WrongInputException("Car should take at least two cells")

        return

    def get_all_states(self, cars):
        states = []
        for car in cars:
            for direction in ['up', 'down', 'left', 'right']:
                if car.can_move(direction, 1, self.cars_to_matrix(cars)):
                    new_cars = deepcopy(cars)
                    new_car = filter(lambda x: x.character == car.character, new_cars)[0]
                    new_car.move(direction, 1)
                    try:
                        self.cars_to_matrix(cars)
                    except Exception as e:
                        import pdb;pdb.set_trace()
                    states.append([[[car.character, direction]], new_cars])

        return states

    def solve(self):
        '''
        Take initial board and get all possible next boards,
        for each board take all next boards
        iterate untill solved
        '''
        Q = []
        cars = self.cars
        visited = []
        Q.insert(0, [[], cars])
        while len(Q) != 0:
            moves, cars = Q.pop()

            if self.is_solved(cars):
                return moves
                
            for new_moves, new_cars in self.get_all_states(cars):
                if hash(str(new_cars)) not in visited:
                    Q.insert(0, [moves + new_moves, new_cars])
                    visited.append(hash(str(new_cars)))

        raise CanNonSolveException('Can not solve')

    def is_solved(self, cars):
        """
        Moment when red car is on the right side
        """
        red_car = filter(lambda x: x.is_red_car, cars)[0]
        if red_car.stop['x'] == self.size['x']-1:
            return True
        return False
           
    def print_steps(self, cars, moves):
        output = ''
        output += '\n\nSOLUTION\n'
        output += "; ".join(["{} {}".format(move[0], move[1]) for move in moves])
        cars = deepcopy(cars)
        for move in moves:
            car = filter(lambda x: x.character == move[0], cars)[0]
            output += '\nMOVE {} {}\n'.format(move[0], move[1])
            car.move(move[1], 1)
            output += self.print_data(cars)
        output += '\nEND of SOLUTION\n\n'
        print output
        return output

    def cars_to_matrix(self, cars):
        data = []
        for y in range(self.size['y']):
            line = []
            for x in range(self.size['x']):
                line.append('.')
            data.append(line)

        for car in cars:
            for point in car.get_points():
                data[point['y']][point['x']] = point['character']

        return data

    def print_data(self, cars):
        matrix = self.cars_to_matrix(cars)

        output = ''
        for line in matrix:
            output += " ".join(line) + '\n'
        print output
        return output


if __name__ == '__main__':

    board_data = '''
        ....AA
        ..BBCC
        rr..EF
        GGHHEF
        ...IEF
        ...IJJ
    '''

    solver = Solver()
    solver.load_data(board_data)
    print 'Loaded data'
    solver.print_data(solver.cars)
    print 'Looking for solution.. (may take several secods)'
    moves = solver.solve()
    solver.print_steps(solver.cars, moves)
