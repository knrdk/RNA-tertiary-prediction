__author__ = 'Konrad Kopciuch'

from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from RMSD.PredictionSignificance import get_pvalue

'''
Uruchomienie skryptu zwraca informacje o parach (TEMPLATE, TRAINING STRUCTURE) dla ktorych stwierdzono ze przyjmuja ten sam zwoj
'''
def main():
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
                print query, chains_lengths[query], rmsd, is_same_fold, pvalue

    print all, same_fold

if __name__ == '__main__':
    main()

