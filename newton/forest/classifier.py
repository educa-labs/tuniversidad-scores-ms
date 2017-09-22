import numpy as np
from sklearn.externals import joblib


class Forest:

    def __init__(self, area_id,serialized_dir):
        self.area_id = area_id
        self.classifier = joblib.load('{}/{}_data'.format(serialized_dir,area_id))

    def query(self, points, n_results):
        predicted = self.classifier.predict_proba(points)
        result = []
        for i in range(predicted.shape[0]):
            best = np.argpartition(predicted[i],-n_results)[-n_results:]
            result.append(best)
        return np.array(result)

    def get_class(self,indexes):
        return np.array([self.classifier.classes_[index] for index in indexes])


if __name__ == '__main__':
    # Ejemplo de uso
    rf = Forest(10,'serialized')
    q = rf.query([[800,700,0,700,720],[800,700,0,700,720]],4)
    print(q)
    print(rf.get_class(q))