#!/usr/bin/env python3
import tools
from tools import debug
from numerical import Simulation

if __name__ == '__main__':
    const = tools.load_constants('constants.config')

    # loader test
    for i in const.keys():
        print('{} = {}\n'.format(i, const[i]))
    
    S = Simulation(const)
    S.initialize()
    S.run(10)


