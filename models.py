class CoffeeMachine:
    def __init__(self, config=None):
        self._valid_size = [1, 2, 3]
        self._valid_density = [1, 2, 3]
        self.size = 0
        self.density = 0
        self.status = "standby"

        if config is not None:
            self.set_size(config['size'])
            self.set_density(config['density'])
            self.status = config['status']

        # clear the message
        self.message = ""

    def set_size(self, size):
        if self.status != "ready":
            self.message = "Err! the machine is not ready!"
            # error code for invalid size
            return 1

        size = int(size)

        if size in self._valid_size:
            self.size = size
            # success
            return 0
        else:
            self.message = "Warning! Invalid size!"
            # error code for invalid size
            return 1

    def set_density(self, density):
        if self.status != "ready":
            self.message = "Err! the machine is not ready!"
            # error code for invalid size
            return 1

        density = int(density)

        if density in self._valid_density:
            self.density = density
            # success
            return 0
        else:
            self.message = "Warning! Invalid density!"
            # error code for invalid density
            return 1

    def next_size(self):
        if self.size not in self._valid_size:
            self.set_size(self._valid_size[0])
        else:
            index = self._valid_size.index(self.size)
            if index + 1 == len(self._valid_size):
                self.set_size(self._valid_size[0])
            else:
                self.set_size(self._valid_size[index + 1])

    def next_density(self):
        if self.density not in self._valid_density:
            self.set_density(self._valid_density[0])
        else:
            index = self._valid_density.index(self.density)
            if index + 1 == len(self._valid_density):
                self.set_density(self._valid_density[0])
            else:
                self.set_density(self._valid_density[index + 1])

        print self.density

    def get_attr(self):
        return {"size": self.size, "density": self.density}

    def get_status(self):
        return self.status

    def reset(self):
        self.size = 0
        self.density = 0
        self.status = "standby"
        self.message = ""

    def turn_on(self):
        if self.status != "ready":
            self.size = 0
            self.density = 0
            self.status = "ready"
            self.message = ""

    def serve(self):
        self.status = "serve"
        self.size = 0
        self.density = 0
        self.message = ""

