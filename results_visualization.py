#%%
import pandas as pd
import seaborn as sns
import pickle
#%%
#### VANILLA ########
pr_result = pickle.load(open('./output_data/page_rank_score_history.pkl', 'rb'))
full_data=pd.DataFrame()
for node in pr_result[0].keys():
    data = pd.Series([pr_result[node] for pr_result in pr_result])
    full_data[node] = data
sns.lineplot(data=full_data, legend=True)

#%%
###### ADD WEIGHTS #######
pr_result = pickle.load(open('./output_data//page_rank_weights_score_history.pkl', 'rb'))
full_data=pd.DataFrame()
for node in pr_result[0].keys():
    data = pd.Series([pr_result[node] for pr_result in pr_result])
    full_data[node] = data
sns.lineplot(data=full_data, legend=True)

#%%
####  PERSONALIZATION ########

pr_result = pickle.load(open('./output_data//page_rank_weights_perso_score_history.pkl', 'rb'))
full_data=pd.DataFrame()
for node in pr_result[0].keys():
    data = pd.Series([pr_result[node] for pr_result in pr_result])
    full_data[node] = data
sns.lineplot(data=full_data, legend=True)
# %%
