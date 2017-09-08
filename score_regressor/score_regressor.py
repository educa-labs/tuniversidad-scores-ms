import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import BayesianRidge
from scipy.stats import norm
import os


# Bayesian regression models
class BayesianRegressor:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.model = BayesianRidge(normalize=True, copy_X=True)
        self.train = self.transform(self.X)

    def transform(self, X):
        return X

    def fit(self):
        self.model.fit(self.train, self.y)
        self.V = self.Vn()

    def score(self):
        return self.model.score(self.train, self.y)

    def plot(self, file=None):
        if file is not None:
            plt.ioff()
        else:
            plt.ion()
        fig, ax = plt.subplots(nrows=1, ncols=1)
        X_axis = np.linspace(self.X.min(), self.X.max() + 20, 100)
        X_axis_transformed = self.transform(X_axis)
        ax.scatter(self.X, self.y)
        ax.plot(X_axis, self.model.predict(X_axis_transformed))
        if file is not None:
            fig.savefig(file)
            plt.close(fig)
        else:
            fig.show()

    def Vn(self):
        try:
            return np.linalg.inv((1 / self.y.std() ** 2) * (self.train.T).dot(self.train))
        except np.linalg.LinAlgError:
            return np.linalg.pinv((1 / self.y.std() ** 2) * (self.train.T).dot(self.train))

    # computes estimator for the posterior variance
    def posterior_variance(self, x):
        x_t = self.transform(x)[0]
        return ((self.y.std() ** 2) + (x_t.T).dot(self.V).dot(x_t))

    # computes estimator for the posterior mean
    def posterior_mean(self, x):
        return self.model.predict(self.transform(x)[0].reshape(1, -1))[0]

    # return tuple of (posterior_mean,sqrt(posterior_variance))
    def posterior_distribution(self, x):
        return self.posterior_mean(x), np.sqrt(self.posterior_variance(x))

    def posterior_cdf(self, y_query, x):
        return norm.cdf(y_query, self.posterior_mean(x), np.sqrt(self.posterior_variance(x)))

    def print_stats(self, t, y_query):
        print("R^2:{}".format(self.score()))
        print("posterior std on t = {}: {:.2f}  ".format(t, np.sqrt(self.posterior_variance(t))))
        print("posterior mean on t = {}: {:.0f}".format(t, self.posterior_mean(t)))
        print(
            "goal of {} achieved with probability:{:.2f} ".format(y_query, (1 - self.posterior_cdf(y_query, t)) * 100))


class SqrtRegressor(BayesianRegressor):
    def transform(self, X):
        return np.array([np.ones(X.shape), np.sqrt(X)]).T


class LogRegressor(BayesianRegressor):
    def transform(self, X):
        X_add = X + 1
        return np.array([np.ones(X_add.shape), np.log(X_add)]).T


class CbrtRegressor(BayesianRegressor):
    def transform(self, X):
        return np.array([np.ones(X.shape), np.cbrt(X)]).T


# Model selector

def get_best(X, y):
    if y.std() == 0:
        return None
    models = [SqrtRegressor, CbrtRegressor, LogRegressor]
    trained_models = []
    for m in models:
        r = m(X, y)
        r.fit()
        if np.all(r.model.coef_ >= 0):
            trained_models.append(r)
    return max(trained_models, key=lambda x: x.score()) if trained_models != [] else None


if __name__ == '__main__':
    import pandas as pd
    # Model testing
    data = pd.read_csv('tests/convergence.csv')
    y = data['score']
    X = data['date']
    plt.scatter(X, y)

    models = [SqrtRegressor, CbrtRegressor, LogRegressor]
    for m in models:
        res = m(X, y)
        res.fit()
        res.plot()
        t = 90
        goal = 750
        x = np.array([t, ])
        res.print_stats(x, goal)
    get_best(X, y)

    # Info psu data testing

    files = os.listdir('data')
    subjects = [1, 2, 3, 6]
    files_tuples = list(map(lambda x: tuple(map(lambda y: int(y), x.split(".")[0].strip().split(","))), files))
    average_hash = {x: 0 for x in subjects}
    for subject in subjects:
        filtered = list(filter(lambda x: x[1] == subject, files_tuples))
        total = 0
        succeses = 0
        for f in filtered:
            data = pd.read_csv('data/{},{}.csv'.format(f[0], f[1]))
            y = data['score']
            X = data['date']
            psu_day = data['psu_day'][0]
            model = get_best(X, y)
            if model is not None:
                #success += 1
                succeses += 1
                # model.plot('data/{}.png'.format(f))
                model.print_stats(np.array([90, ]), 850)
                prediction = model.posterior_mean(np.array([psu_day, ]))
                print(prediction)
                total += prediction
        average_hash[subject] = total / succeses
    print(average_hash)
