__author__ = 'Konrad Kopciuch'

import sys
from Config import Config
from Repository.MongoTemplateRepository import MongoTemplateRepository
from SVM.templates_ranking import get_templates_ranking


def build_model(template_id, sequence, outpup_path):
    repo = MongoTemplateRepository()
    (template_id, template_sequence, template_secondary_structure) = repo.get_template_info(template_id)

    print template_sequence, template_secondary_structure

def main_build_model(sequence, svm_file, output_path):
    print 'Tworzenie ranking szablonow'
    template_ranking = get_templates_ranking(svm_file, sequence)
    print 'Zakonczono tworzenie ranking szablonow'

    for (template_id, probability) in template_ranking:
        print 'Budowanie modelu za pomoca szablonu: ', template_id
        result = build_model(template_id, sequence, output_path)
        if result:
            print 'model zapisany w pliku: ', output_path
            return
        else:
            print 'utworzenie modelu nie powiodlo sie, proba uzycia kolejnego szablonu'
    print 'Brak dostepnych szablonow'


if __name__ == '__main__':
    if len(sys.argv < 3):
        print 'Uzycie: main.py output_file sequence [svm_file]'
    else:
        output_file = sys.argv[1]
        sequence = sys.argv[2]
        if len(sys.argv) == 4:
            svm_file = sys.argv[3]
        else:
            config = Config('config.ini')
            svm_file = config.get_svm_file()

        main_build_model(sequence, svm_file, output_file)

