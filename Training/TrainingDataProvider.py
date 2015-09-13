__author__ = 'Konrad Kopciuch'

from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from RMSD.PredictionSignificance import get_pvalue
import Utils.FloatList as fl


def __get_template_id_from_filename(filename):
    '''
    Funkcja zwraca template id z pliku z szablonem
    :param filename: nazwa pliku z szablonem w formacie TEMPLATE_ID.pdb
    :return: TEMPLATE_ID
    '''
    return filename.split('.')[0]


def __get_trainings_chains_lenght():
    repo = MongoTrainingTemplateRepository()
    return repo.get_chains_lengths()


def __get_folds_dict(file_with_rmsd):
    '''
    Funkcja zwraca dwuwymiarowy slownik ktory dla query_id i template_id zawiera informacje czy zwoj jest taki sam
    :param file_with_rmsd: plik uzyskany za pomoca programu main_training_cross_rmsd z informacja o rmsd dla query, template
    :return: slownik dwuwymiarowy [QUERY_ID][TEMPLATE_ID] z informacja czy ten sam zwoj
    '''
    chains_lengths = __get_trainings_chains_lenght()

    output = dict()
    with open(file_with_rmsd, 'r') as f:
        for line in f:
            (query, template, rmsd) = line.split('\t')
            query_id = __get_template_id_from_filename(query)
            template_id = __get_template_id_from_filename(template)

            pvalue = get_pvalue(chains_lengths[query_id], float(rmsd))
            is_same_fold = pvalue < 0.01

            if not output.has_key(query_id):
                output[query_id] = dict()
            output[query_id][template_id] = is_same_fold
    return output


def get_train_data(file_with_rmsd, file_with_feature_vector):
    '''
    Funkcja zwraca dwie lista, jedna zawiera feature vector, a druga informacje czy odpowiada temu samemu zwojowi
    :param file_with_rmsd: plik uzyskany z programu main_training_cross_feature_vector
    :param file_with_feature_vector: plik uzyskany z programu main_training_cross_rmsd
    :return: dwie listy (data, target)
    '''
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
