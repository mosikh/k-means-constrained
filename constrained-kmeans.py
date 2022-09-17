import pandas as pd
from k_means_constrained import KMeansConstrained

am = pd.read_csv('am.csv')
db = KMeansConstrained(n_clusters = 4,size_max=20,random_state=0)
result = list(db.fit_predict(am))

#######---------------------------------------------------------------------------------------------------
