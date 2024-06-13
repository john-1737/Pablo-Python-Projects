def moon_weight(weight, increase, yearlength):
    moonweight = 50 * 0.165
    for year in range(1,yearlength + 1):
        print(f'Year {year} : {moonweight} pounds')
        moonweight = (year * increase + weight) * 0.165

moon_weight(50,2,10)