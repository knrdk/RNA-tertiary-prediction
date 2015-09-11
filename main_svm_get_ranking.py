__author__ = 'Konrad Kopciuch'

from SVM.templates_ranking import get_templates_ranking

def __print_ranking(ranking):
    for (template_id, prob) in ranking:
        print template_id, prob

def __write_ranking(ranking, output_file):
    with open(output_file, 'w') as f:
        for (template_id, prob) in ranking:
            line = str(template_id) + '\t' + str(prob) + '\n'
            f.write(line)


def main_svm_predict(svm_file, query_sequence, output_file, print_ranking = True):
    ranking = get_templates_ranking(svm_file, query_sequence)

    if print_ranking:
        __print_ranking(ranking)

    __write_ranking(ranking, output_file)


if __name__ == '__main__':
    sequence = 'GGGCCCGUAGCUUAGCCAGGUCAGAGCGCCCGGCUCAUAACCGGGCGGUCGAGGGUUCGAAUCCCUCCGGGCCCACCA'
    main_svm_predict('data.svm', sequence, 'ranking.txt')