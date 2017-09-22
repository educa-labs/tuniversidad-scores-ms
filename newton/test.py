from newton.main import *
import pandas as pd
import numpy as np




if __name__ == '__main__':
    data_file = 'data/carreras2.csv'
    carreers = pd.read_csv(data_file, index_col=0)
    carreers = carreers[['Nombre','Universidad']]
    sisrec = Newton(np.array([i for i in range(1, 12)]), 'forest/serialized', 'knn/serialized', 'data', 3, 5)

    test_scores = [[800, 700, 0, 700, 720],
                   [560, 550, 0, 600, 620],
                   [730, 750, 600, 660, 719],
                   [450, 450, 0, 0, 650],
                   [600, 750, 750, 0, 680],
                   [620, 640, 680, 0, 720]
                   ]

    for i in range(1,12):
        recs = sisrec.get_recs(i, test_scores)
        print("Area {}".format(i))
        for j in range(len(test_scores)):
            print(test_scores[j])
            rec = recs[j]
            recomendations = []
            for k in range(rec.shape[0]):
                for l in range(rec.shape[1]):
                    recomendations.append("{} {}".format(carreers['Nombre'][rec[k, l]], carreers['Universidad'][rec[k, l]]))
            for r in recomendations:
                print(r)