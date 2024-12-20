class trip:
    def driving(self):
        print('driving')
    def sleeping(self):
        print('sleeping')
class camping(trip):
    def setup(self):
        print('setting up tent')
    def dinner(self):
        print('cooking dinner')
    def campingtrip(self):
        print('Let\'s go camping!')
        self.driving()
        self.setup()
        self.dinner()
        self.sleeping()

personwholikescamping = camping()
personwholikescamping.campingtrip()

    