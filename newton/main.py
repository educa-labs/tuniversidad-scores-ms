
#estos imports son una mala practica, pero se necesitan completos ambos archivos y ademas las funciones de distancia
#deben ser cargadas en main para que el BallTree serializado pueda usarlas.

from newton.forest import *
from newton.knn import *
import numpy as np


class Newton:

    '''
    area_ids - np.array con ides de las areas.
    serialized_forests - str path a carpeta con forests serializados.
    serialized_tree - str path a carpeta con tree serializado
    data_dir - str path a carpeta con datos.
    n_forest_results - int cantidad de resultados obtenidos por el RF
    k - int cantidad de vecinos cercanos calculados por el BallTree
    '''

    def __init__(self, area_ids,serialized_forests,serialized_tree, data_dir, n_forest_results=3, k=5):
        self.area_ids = area_ids
        self.balltree = Tree(serialized_tree,data_dir)
        self.active_forests = {x: None for x in area_ids}
        self.n_forest_results = n_forest_results
        self.k = k
        self.serialized_forests = serialized_forests

    '''
    area_id - int  id de area para recomendar
    scores - np.array (n,5) arreglo de puntajes para recomendar
    retorna np.array (n,n_forest_results,k) carreras recomendadas
    '''

    def get_recs(self, area_id, scores):
        if self.active_forests[area_id] is None:
            self.active_forests[area_id] = Forest(area_id, self.serialized_forests)
        forest = self.active_forests[area_id]
        prediction = forest.get_class(forest.query(scores,self.n_forest_results))
        recommendations = []
        for carreer_set in prediction:
            recommendations.append(self.balltree.query(carreer_set,self.k))
        return np.array(recommendations)

    def filter_recs(self, user, carreers):
        pass


if __name__ == '__main__':
    #Ejemplo de uso
    sisrec = Newton(np.array([i for i in range(1, 12)]),'forest/serialized','knn/serialized','data',3,5)
    print(sisrec.get_recs(1, [[800,700,0,700,720], [800,700,0,700,720]]))