import numpy as np
import pandas as pd
from sklearn.externals import joblib


def categorical_distance(c_j, c_k):
    return int(not c_j == c_k)


def continuous_distance(x_j, x_k, r_i):
    return np.divide(np.absolute(x_j - x_k), r_i)


def gower_distance(X_j, X_k, **kwargs):
    distance = 0
    for col in kwargs['categorical']:
        distance += np.dot(kwargs['W_i'][kwargs['column_hash'][col]], categorical_distance(X_j[kwargs['column_hash'][col]], X_k[kwargs['column_hash'][col]]))
    for col in kwargs['continuous']:
        distance += np.dot(kwargs['W_i'][kwargs['column_hash'][col]],
                           continuous_distance(X_j[kwargs['column_hash'][col]], X_k[kwargs['column_hash'][col]], kwargs['R_i'][kwargs['column_hash'][col]]))
    distance += kwargs['W_i'][11] * (1 - np.absolute(kwargs['similarity_matrix'][int(X_j[kwargs['column_hash']['ID']]), int(X_k[kwargs['column_hash']['ID']])]))

    return distance


class Tree:

    def __init__(self,serialized_dir,data_dir):
        self.balltree = joblib.load('{}/balltree'.format(serialized_dir))
        self.data = np.array(pd.read_csv('{}/carreers_scaled.csv'.format(data_dir)))
        self.ids = np.load('{}/ids.npy'.format(data_dir))
        self.reversed_ids = np.zeros(self.ids.shape,dtype='int32')
        for i in range(self.ids.shape[0]):
            self.reversed_ids[self.ids[i]] = i

    def query(self, ids_points, k=5):
        q = self.data[self.reversed_ids[ids_points]]
        result = self.balltree.query(q, k=k, return_distance=False)
        return np.array(list(map(lambda x: self.ids[x],result)))

if __name__ == '__main__':
    #Ejemplo de uso

    id_query = np.array([4])
    tree = Tree('serialized','../data')
    print(tree.query(id_query,5))

