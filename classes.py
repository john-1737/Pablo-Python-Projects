class Thing:
    pass

class Inanimate(Thing):
    pass

class Animate(Thing):
    pass

class Sidewalk(Inanimate):
    pass

class Animal(Animate):
    def breathe(self):
        print('breathing')
    def move(self):
        print('moving')
    def eat_food(self):
        print('eating food')

class Mammal(Animal):
    def feed_young_with_milk(self):
        print('feeding young')

class Giraffe(Mammal):
    def eat_leaves_from_trees(self):
        print('eating leaves')

class Elephant(Mammal):
    def eat_grass(self):
        print('eating grass')
    def drink_water_from_stream(self):
        print('drinking water')

ozwald = Giraffe()
gertrude = Giraffe()
reginald = Elephant()
harriet = Elephant()
ozwald.move()
gertrude.eat_leaves_from_trees()
reginald.eat_grass()
harriet.drink_water_from_stream()
