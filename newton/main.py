
#estos imports son una mala practica, pero se necesitan completos ambos archivos y ademas las funciones de distancia
#deben ser cargadas en main para que el BallTree serializado pueda usarlas.

from newton.forest import *
from newton.knn import *
import numpy as np
from lru import LRU
from psutil import virtual_memory

class Newton:

    '''
    area_ids - np.array con ides de las areas.
    serialized_forests - str path a carpeta con forests serializados.
    serialized_tree - str path a carpeta con tree serializado
    data_dir - str path a carpeta con datos.
    n_forest_results - int cantidad de resultados obtenidos por el RF
    k - int cantidad de vecinos cercanos calculados por el BallTree
    '''

    def __init__(self, area_ids,serialized_forests,serialized_tree, data_dir, cache=4,n_forest_results=3, k=5):
        self.area_ids = area_ids
        self.balltree = Tree(serialized_tree,data_dir)
        self.active_forests = LRU(cache,callback=clear)
        self.n_forest_results = n_forest_results
        self.k = k
        self.serialized_forests = serialized_forests
        self.cache = cache

    '''
    area_id - int  id de area para recomendar
    scores - np.array (n,5) arreglo de puntajes para recomendar
    retorna np.array (n,n_forest_results,k) carreras recomendadas
    '''

    def get_recs(self, area_id, scores):
        prediction = self.predict(area_id,scores,self.n_forest_results)
        recommendations = []
        for carreer_set in prediction:
            recommendations.append(self.balltree.query(carreer_set,self.k))
        return np.array(recommendations)

    def predict(self, area_id, scores, n_results):
        if not self.active_forests.has_key(area_id):
            if get_mem_percentage() < 0.3:
                del self.active_forests[self.active_forests.peek_last_item()[0]]
            self.active_forests[area_id] = Forest(area_id, self.serialized_forests)
            #print(get_mem_percentage())
        forest = self.active_forests[area_id]
        #print(self.active_forests.items())
        return forest.get_class(forest.query(scores,n_results))

    def filter_recs(self, user, carreers):
        pass

def get_mem_percentage():
    mem = virtual_memory()
    return mem.available/mem.total

def clear(key,value):
    del value

if __name__ == '__main__':
    #Ejemplo de uso
    sisrec = Newton(np.array([i for i in range(1, 12)]),'forest/serialized','knn/serialized','data',3,5)
    print(sisrec.get_recs(1, [[800,700,0,700,720], [800,700,0,700,720]]))