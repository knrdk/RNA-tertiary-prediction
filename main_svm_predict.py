__author__ = 'Konrad Kopciuch'

from SVM.templates_ranking import get_templates_ranking


def main_svm_predict(svm_file, query_sequence):
    ranking = get_templates_ranking(svm_file, query_sequence)
    for (templated_id, prob) in ranking:
        print templated_id, prob

if __name__ == '__main__':
    sequence = 'GGGCCCGUAGCUUAGCCAGGUCAGAGCGCCCGGCUCAUAACCGGGCGGUCGAGGGUUCGAAUCCCUCCGGGCCCACCA'
    main_svm_predict('data.svm', sequence)