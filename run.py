"""
Missing features?
1. multi user!

"""
import json
from flask import Flask, render_template
from models import CoffeeMachine

app = Flask(__name__)

data_file = open('coffee_machine.json')
cm = CoffeeMachine(json.load(data_file))
data_file.close()
print(cm.__dict__)


@app.route("/")
def index():
    return render_template('layout.html')


@app.route("/cm/interface")
def interface():
    if cm.status == "ready":
        return render_template('interface.html', attributes=cm.get_attr())
    elif cm.status == "serve":
        return render_template('coffee.html', attributes=cm.get_attr())
    else:
        return render_template('machine.html', attributes=cm.get_attr())


@app.route("/cm")
def coffee_machine():
    print json.dumps(cm.__dict__)
    return json.dumps(cm.__dict__)


@app.route("/cm/<size>/<density>")
def update(size, density):
    cm.set_size(size)
    cm.set_density(density)
    data_file = open('coffee_machine.json', 'w')
    data_file.write(json.dumps(cm.__dict__))
    return coffee_machine()


@app.route("/cm/click/size")
def click_size():
    # send message to DM: user asked for next size!
    return next_size()

@app.route("/cm/size")
def next_size():
    cm.next_size()
    data_file = open('coffee_machine.json', 'w')
    data_file.write(json.dumps(cm.__dict__))
    return coffee_machine()


@app.route("/cm/click/density")
def click_density():
    # send message to DM: user asked for next density!
    return next_density()


@app.route("/cm/density")
def next_density():
    cm.next_density()
    data_file = open('coffee_machine.json', 'w')
    data_file.write(json.dumps(cm.__dict__))
    return coffee_machine()


@app.route("/cm/reset")
def reset():
    cm.reset()
    return coffee_machine()


@app.route("/cm/turn_on")
def turn_on():
    cm.turn_on()
    return coffee_machine()


@app.route("/cm/serve")
def serve():
    # serve the coffee?
    cm.serve()
    return coffee_machine()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
