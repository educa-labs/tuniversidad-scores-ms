#!/usr/bin/env bash

scp -i "/home/ironcadiz/.ssh/gc_p" -r newton/data 35.185.42.34:/home/felipe/tuniversidad-scores-ms/newton/data
scp -i "/home/ironcadiz/.ssh/gc_p" -r newton/forest/serialized 35.185.42.34:/home/felipe/tuniversidad-scores-ms/newton/forest/serialized
scp -i "/home/ironcadiz/.ssh/gc_p" -r newton/knn/serialized 35.185.42.34:/home/felipe/tuniversidad-scores-ms/newton/knn/serialized