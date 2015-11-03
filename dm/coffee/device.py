from tdm.tdmlib import DeviceWHQuery, DeviceAction 
from urllib2 import Request,urlopen 
import json

coffee_database = {
    'espresso': {
        'size': 1,
        'density': 3,
    },
    'americano': {
        'density': 2,
    },
    'coffee': {},
    'buttons': {},
}

class CoffeeDevice:
    def __init__(self):
        self.valid_int_sizes = [1, 2, 3]
        self.valid_int_densities = [1, 2, 3]

        self.valid_sizes = ["big", "medium", "small", "bigger", "smaller"]
        self.valid_densities = ["dark", "mild", "light", "darker", "lighter"]

        self.string_to_size = {"big": lambda x: 3, "medium": lambda x:2, "small": lambda x:1, "bigger": lambda x:  x + 1, "smaller": lambda x:  x - 1}
        self.string_to_density = {"dark": lambda x: 3, "mild": lambda x: 2, "light": lambda x: 1, "darker": lambda x:  x + 1, "lighter": lambda x:  x - 1}

        self.size_to_string = {1: "small", 2: "medium", 3: "big"} 
        self.density_to_string = {1: "light", 2: "mild", 3: "dark"} 
        
        # default value
        data = self.read()
        self.size, self.density, self.status = data['size'], data['density'], data['status']

    class ChangeSize(DeviceAction):
        PARAMETERS = [
            "size_to_select",
        ]

        def perform(self, size):
            if size in self.device.valid_sizes:
                # conver the string to integer
                new_size = self.device.string_to_size[size](self.device.size)
                if new_size in self.device.valid_int_sizes:
                    size = new_size
                    self.device.size = size
            
            # now go and set the params on the machine!
            data = self.device.setParams(self.device.size, self.device.density)
            # we can monitor the change in size and density

            # make sure that we are in the same page!
            self.device.size = data['size']
            self.device.density = data['density']
            self.device.status = data['status']

            return True

    class ChangeDensity(DeviceAction):
        PARAMETERS = [
            "density_to_select",
        ]

        def perform(self, density):
            if density in self.device.valid_densities:
                # conver the string to integer
                new_density = self.device.string_to_density[density](self.device.density)
                if new_density in self.device.valid_int_densities:
                    density = new_density
                    self.device.density = density

            # now go and set the params on the machine!
            data = self.device.setParams(self.device.size, self.device.density)
            # we can monitor the change in size and density

            # make sure that we are in the same page!
            self.device.size = data['size']
            self.device.density = data['density']
            self.device.status = data['status']
            
            return True

    class what_to_serve(DeviceWHQuery):
        # the default value for coffee_to_select is just 'coffee'
        PARAMETERS = [
            "size_to_select=''",
            "density_to_select=''",
            "coffee_to_select=''",
            "what_to_serve=''",
        ]

        def perform(self, size, density, name, what):
            if what in ['p%s%s' % (s,d) for s in self.device.valid_int_sizes for d in self.device.valid_int_densities]:
                size = what[1]
                density = what[2]
                name = "coffee"

            # hadle the coffee type
            if name == '' and size == '' and density == '':
                return []

            if name not in coffee_database:
                name = "coffee"

            if (name == 'coffee' and size == '' and density == '') or name == 'buttons':
                # read form machine
                data = self.device.read()
                size, density = data['size'], data['density']
                self.device.size, self.device.density = size, density

            # read from coffee database, if a coffe type has specific feature set that
            if 'size' in coffee_database[name]:
                size = coffee_database[name]['size']
                self.device.size = size

            if 'density' in coffee_database[name]:
                density = coffee_database[name]['density']
                self.device.density = density

            # REPEAT SET PARAMETERS
            # we don't know when error happens :-)
            size = self.device.apply_size(size)
            density = self.device.apply_density(density)

            if size not in self.device.valid_int_sizes or density not in self.device.valid_int_densities:
                print size, density
                return []

            # now go and set the params on the machine!
            data = self.device.setParams(self.device.size, self.device.density)
            # we can monitor the change in size and density

            # make sure that we are in the same page!
            self.device.size = data['size']
            self.device.density = data['density']
            self.device.status = data['status']

            return ["p%s%s" % (self.device.size, self.device.density)]


    class size_to_select(DeviceWHQuery):
        PARAMETERS = [
            "size_to_select=''",
        ]

        def perform(self, size):
            size = self.device.apply_size(size)
                        
            return [self.device.size]

    class density_to_select(DeviceWHQuery):
        PARAMETERS = [
            "density_to_select=''",
        ]

        def perform(self, density):
            density = self.device.apply_density(density)
            
            return [self.device.density]

    class Serve(DeviceAction):
        PARAMETERS = [
            "what_to_serve",
        ]

        def perform(self, what):
            self.device.serve()
            # we can monitor the change in size and density
            return True

    class TurnOn(DeviceAction):
        def perform(self):
            if self.device.status != "ready":
                self.device.turn_on()

            print "status", self.device.status

            return True

    class Reset(DeviceAction):
        def perform(self):
            data = self.device.reset()

            self.device.size = data['size']
            self.device.density = data['density']
            self.device.status = data['status']
            # we can monitor the change in size and density
            return True

    def apply_size(self, size):
        if size in self.valid_sizes:
            # conver the string to integer
            size = self.string_to_size[size](self.size)
            self.size = size

        return size

    def apply_density(self, density):
        if density in self.valid_densities:
            # conver the string to integer
            density = self.string_to_density[density](self.density)
            self.density = density
            
        return density

    def serve(self):
        url = 'http://130.241.217.75:5000/cm/serve'
        print url
        return self.load_json(url)

    def turn_on(self):
        url = 'http://130.241.217.75:5000/cm/turn_on'
        print url
        return self.load_json(url)

    def reset(self):
        url = 'http://130.241.217.75:5000/cm/reset'
        print url
        return self.load_json(url)

    def read(self):
        url = 'http://130.241.217.75:5000/cm'
        print url
        return self.load_json(url)

    def setParams(self, size, density):
        url = 'http://130.241.217.75:5000/cm/%s/%s' % (size, density)
        print url
        return self.load_json(url)

    # def load_json(self, url):
    #     return {"size":0, "density":0, "status": "ready"}

    def load_json(self, url):
        request = Request(url)
        response = urlopen(request)
        data = response.read()
        return json.loads(data)


"""            
    class SetParameters(DeviceAction):
        PARAMETERS = ["size_to_select", "density_to_select"]

        def perform(self, size, density):
            # we don't know when error happens :-)
            if size in self.device.sizes:
                size = self.device.sizes[size](self.device.size)

            if density in self.device.densities:
                density = self.device.densities[density](self.device.density)

            # now go and set the params on the machine!
            data = self.device.setParams(size, density)
            # we can monitor the change in size and density

            # make sure that we are in the same page!
            self.device.size = data['size']
            self.device.density = data['density']

            return True

    class GetSize(DeviceWHQuery):

        def perform(self):
            self.device.sync()
            return [self.device.size]

    class GetDensity(DeviceWHQuery):

        def perform(self):
            self.device.sync()
            return [self.device.density]


    def sync(self):
        data = self.getParams()
        self.size = data['size']
        self.density = data['density']

    def getParams(self):
        url = 'http://130.241.217.75:5000/cm/'
        print url
        request = Request(url)
        response = urlopen(request)
        data = response.read()
        return json.loads(data)


"""