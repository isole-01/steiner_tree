from mst_v2 import *
import glob
import pathlib

if __name__ == "__main__":
    path = str(pathlib.Path().absolute()) + "\PUC"
    files = [f for f in glob.glob(path + "**/*.stp")]

    for f in files:
        g = Graph()
        g.read_file(f)
        mst = Kruskal(g)
        result = mst.apply()

        s = Steiner(result, g)
        final = s.apply()

        # print(f)
        # print("Kruskal: ", mst.weight)
        # if 'hc12p' in f:
        #     fl = open('amir.txt', 'w')
        #     fl.write(str(g.terminals))
        #     fl.write('\n')
        #     fl.write(str(final[0]))

        fileResult = open(f.split('.')[0] + '.out', 'w')
        edges = final[0]

        # print("Cost: ", final[1],'\n')

        fileResult.write('Cost ' + str(final[1]) + '\n')
        fileResult.write('Edges ' + str(len(edges)) + '\n')
        for edge in edges:
            fileResult.write('E ' + str(edge[0]) + ' ' + str(edge[1]) + '\n')
