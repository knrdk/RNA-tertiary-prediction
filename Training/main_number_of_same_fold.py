__author__ = 'rna'

from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from RMSD.PredictionSignificance import get_pvalue

repo = MongoTrainingTemplateRepository()
chains_lengths = repo.get_chains_lengths()

all, same_fold = 0, 0
with open('/home/rna/RNA/TrainingResults.txt','r') as f:
    for line in f:
        all +=1
        (query, template, rmsd) = line.split('\t')
        query = query.split('.')[0]
        pvalue = get_pvalue(chains_lengths[query], float(rmsd))
        is_same_fold = pvalue < 0.01
        if is_same_fold:
            same_fold += 1
        print query, chains_lengths[query], rmsd, is_same_fold

print all, same_fold

