

def load_constants(path):
    with open(path,'r') as file:
        values = list(map(lambda x: x[:-1],
                          file.readlines()))
        names = [name for name in values[2::4]]
        constants = [const for const in values[3::4]]
        const = {}

        for i,j in zip(names,constants):
            const[i] = eval(j)

        return const