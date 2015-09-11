__author__ = 'Konrad Kopciuch'

from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from RMSD.PredictionSignificance import get_pvalue
import Utils.FloatList as fl


def __get_template_id_from_filename(filename):
        return filename.split('.')[0]


def __get_trainings_chains_lenght():
    repo = MongoTrainingTemplateRepository()
    return repo.get_chains_lengths()


def __get_folds_dict(file_with_rmsd):
    chains_lengths = __get_trainings_chains_lenght()

    output = dict()
    with open(file_with_rmsd, 'r') as f:
        for line in f:
            (query, template, rmsd) = line.split('\t')
            query_id = __get_template_id_from_filename(query) #TODO: w pliku zapisywac juz id a nie filename
            template_id = __get_template_id_from_filename(template)

            pvalue = get_pvalue(chains_lengths[query_id], float(rmsd))
            is_same_fold = pvalue < 0.01

            if not output.has_key(query_id):
                output[query_id] = dict()
            output[query_id][template_id] = is_same_fold
    return output


def get_train_data(file_with_rmsd, file_with_feature_vector):
    folds_dict = __get_folds_dict(file_with_rmsd)

    data = []
    target = []

    with open(file_with_feature_vector, 'r') as f:
        for line in f:
            (query, template, fv) = line.split('\t')

            query_id = __get_template_id_from_filename(query)
            template_id = __get_template_id_from_filename(template)

            same_fold = folds_dict[query_id][template_id]
            data.append(fl.parse_from_string(fv))
            target.append(same_fold)

    return data, target
