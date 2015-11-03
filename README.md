# Talking Coffee Machine Simulator (TCMS)
A web based talking coffee machine simulator


# What
This is a simulator of an imaginary coffee machine with web API service. This machine only can serve one person at the same time. Multiple users at the same time can confuse the current version.

The current version of coffee machine understands two features for coffee: density and size. 

# How
The state of this coffee machine is stored in `coffee_machine.json` and all of it's funcitonality are implemented in as `CoffeeMachine` class in `models.py`. The `run.py` will fire the web interface and all web services. 

# API

#### The web interface
`/`

It will retrun the functioning machine user interface.

#### Status check in JSON
`/cm`

It will respond the coffe machine status in JSON format such as:
```
  {
    "_valid_size": [1, 2, 3],
    "density": 3,
    "_valid_density": [1, 2, 3],
    "size": 1,
    "status": "ready"
  }
```

#### Set the size and density at the same time
`/cm/<size>/<density>`

#### Set the size 
`/cm/size/<size>`

#### Set the density
`/cm/density/<density>`

#### The 'push button action' as next size (loop through sizes):
`/cm/size`

#### The 'push button action' as next density (loop through density):
`/cm/density`

#### Turn on action:
`/cm/turn_on`
It resets all parameters then it sets `status` to `ready`.

#### Reset action:
`/cm/reset`
It resets all parameters then it sets `status` to `standby`.

#### Serve action:
`/cm/serve`
It sets `status` to `serve` then it resets all parameters.
