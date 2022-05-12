


with open('river.ppm', 'w') as f:
    f.write('P3\n')
    f.write('1000 560\n')
    f.write('255\n')
    for i in range(560):
        for j in range(250):
            f.write('20 150 50 ')
        for j in range(500):
            f.write('45 160 220 ')
        for j in range(250):
            f.write('20 150 50 ')
        f.write('\n')
