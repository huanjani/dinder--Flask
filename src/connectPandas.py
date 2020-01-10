import pandas as pd
from scipy.spatial.distance import squareform, pdist
import numpy as np
import psycopg2
from sqlalchemy import create_engine
import itertools

engine = create_engine('postgres+psycopg2://janicehuang@localhost/dinder')

# Method to compute Jaccard similarity index between two sets
def compute_jaccard(ing1_recipes, ing2_recipes):
    intersection = ing1_recipes.intersection(ing2_recipes)
    union = ing1_recipes.union(ing2_recipes)
    jaccard = len(intersection)/float(len(union))
    return jaccard

sql = 'select i.ingredient_id, ri.recipe_id from (select ri.ingredient_id from ingredients i, recipe_ingredients ri where i.id=ri.ingredient_id group by ri.ingredient_id having count(ri.ingredient_id)>5000) as i, recipe_ingredients as ri where i.ingredient_id=ri.ingredient_id limit 100'

df = pd.read_sql_query(sql, con=engine, coerce_float=False, params=None, parse_dates=None)

dummies = pd.get_dummies(df['recipe_id'])
df = pd.concat([df, dummies], axis=1)
grp = df.groupby('ingredient_id').sum()
dist = pdist(grp, metric="jaccard")
s_dist = squareform(dist)
np.fill_diagonal(s_dist, np.nan)
sim = np.subtract(1, s_dist)
sim_df = pd.DataFrame(sim, columns=grp.index, index=grp.index)


print(sim_df)