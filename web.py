from flask import Flask, request
from solver import Solver, WrongInputException, CanNonSolveException

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def main():
    """
    Sample code to show Rush hour solver on web.
    Templates are not used for simplicity.
    """
    if request.method == 'POST':
        board_str = request.form['board']

        if board_str:
            try:
                solver = Solver()
                solver.load_data(board_str)
                moves = solver.solve()
                response = solver.print_steps(solver.cars, moves)
            except CanNonSolveException as e:
                return "Can not solve this board</br><a href='/'>Try another board</a>"
            except WrongInputException as e:
                return "Can not load this board</br><a href='/'>Try another board</a>"

            return "<pre>{}</pre></br><a href='/'>Try another board</a>".format(response)

    resp_text = '''
        <form method="POST">
            <h2>Rush hour solver online</h2>
            <p>
            </p>
            <textarea name='board' rows="6">
....AA
..BBCC
rr..EF
GGHHEF
...IEF
...IJJ
            </textarea>
            <br/>
            <input type="submit" value="Submit (will take some time)" />
        </form>
    '''
    return resp_text

if __name__ == "__main__":
    app.run()
