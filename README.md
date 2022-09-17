# k-means-constrained
This project tried to use k_means_constrained python library to cluster. 

The project extends glasfiber lines through every house in an area. 
We need to cluster the houses to express a distributor to each cluster. 
Each cluster must include maximum of 20 houses. The minimum doesn't matter. 
The clusters should be condensed and intensive and mustn't be shuffled.

The input is the adjacency matrix in a csv file (am.csv).

The provided picture (clustering_output.jpeg) shows the result of clustering by k_means_constrained python library.
As it is shown in the picture, the blue and green clusters are mixed. The yellow and red clusters seem ok.
The other picture (desired_output.jpeg) presents the favorite manner, but the library doesn't give such a clustering. 

I see this manner of wrong clustering in other datasets, as well.

It is the code:

import pandas as pd
from k_means_constrained import KMeansConstrained

am = pd.read_csv('am.csv')
db = KMeansConstrained(n_clusters = 4,size_max=20,random_state=0)
result = list(db.fit_predict(am))

The ESRI Shapefiles including Glasfiber lines, House points and the output are also shared just in case that somebody wants to visualize the output. But they are not necessary for debug. 


Versions:
- Python: 3.9.5
- Operating system: Windows 10
- k-means-constrained: 0.7.2
- numpy: 1.23.2
- scipy: 1.9.1
- ortools: 9.4.1874
- joblib: 1.1.0
- cython (if installed): not installed