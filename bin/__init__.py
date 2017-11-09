#!/usr/bin/env python3
import tools

if __name__ == '__main__':
    const = tools.load_constants('constants.config')

    # loader test
    for i in const.keys():
        print('{}\n{} = {}\n'.format(type(const[i]),i, const[i]))
