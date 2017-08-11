# score_regressor

Para ver ejemplos del funcionamiento ver lineas 105 a 120 de score_regressor.py

Tips: X debería ser un arreglo de ints en que 0 representa la fecha del primer ensayo y n representa n diás pasados 
a partir de eso e y un arreglo de puntajes.

## Clases

```python
class BayesianRegressor
```

Esta clase es un wrapper de la clase BayesianRidgeRegressor de sklearn. Permite obtener un modelo de regresión de la
 forma Y = AX+B.
 
#### Métodos

```python
__init__(self,X,y)
```
Args:
* X: array, dimensión (n) - Datos correspondientes a la variable independiente o predictoras.
* y: array, dimensión (n) - Datos correspondientes a la variriable dependiente  o a predecir.

Retorna:

Objeto de la clase.


```python
fit()
```
Entrena al  modelo con lo datos entregados a ``__init__``.

Retorna: None

```python
score()
```
Retorna: float - el valor R^2 de la regresión.


```python
plot(file=None)
```
Crea scatter plot de los datos y curva de regresión.

Args:
* file: string - Archivo donde guardar el gráfico. Si es None se despliega y no se guarda.

```python
posterior_mean(self,x)
```

Equivalente a el método predict de sklearn.

Args:

* x: array, dimension(n) - valores para los cuales se quiere la media de la distribución normal estimada.

Retorna: array, dimensión(n) -  medias de las distribuciónes estimadas en los puntos en x.

```python
posterior_variance(self,X)
```

Idem al método anterior pero calcula la varianza.

```python
posterior_distribution(self,x)
```
Retorna: Tupla de floats equivalente a :
```python
self.posterior_mean(x), np.sqrt(self.posterior_variance(x))
```

```python
posterior_cdf(self,y_query,x)
```
Args:

* y_query: int - punto en el dominio de self.y
* x: array - punto en el dominio de self.x

Retorna: float- proabilidad de que y sea menor a y_query. Formalmente : P(y<=y_query | x)

Tip: si x es unidimensional debes pasar una array así: ```np.array([90,])```

```python
print_stats(self, t, y_query)
```

printea estadísticas del modelo y sobre la consulta de y_query en el punto t (array).


#### Atributos

* `X` datos X pasados inicialmente
* `y` datos y pasados inicialmente
* `model` objeto BayessianRidgeRegression de sklearn
* `train` datos de entrenamiento de la regresion. Distinto de `x`



```python
class SqrtRegressor
```

Hereda de BayesianRegressor. Entrega una curva de la familia y= Asqrt(x) + B

```python
class CbrtRegressor
```

Hereda de BayesianRegressor. Entrega una curva de la familia y= Acbrt(x) + B


```python
class LogRegressor
```

Hereda de BayesianRegressor. Entrega una curva de la familia y= Aln(x) + B



## Funciones

```python
get_best(X, y)
```
Args:
* X: array, dimensión (n) - Datos correspondientes a la variable independiente o predictoras.
* y: array, dimensión (n) - Datos correspondientes a la variriable dependiente  o a predecir.

Retorna: Objeto de la familia BayesianRegressor ya entrenado con el modelo óptimo. retorna None si es que no hay modelo válido.

