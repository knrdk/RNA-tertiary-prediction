__author__ = 'Konrad Kopciuch'

from Repository.MongoTemplateRepository import MongoTemplateRepository


def get_longest_and_average_sequence_length():
    repo = MongoTemplateRepository()
    min_length = float("inf")
    max_length = 0
    sum_length = 0
    number_of_sequnces = 0
    for db_id, sequence, resolution, template_id in repo.get_all_unmodified_sequences():
        number_of_sequnces+=1
        current_length = len(sequence)
        sum_length += current_length
        max_length = max(max_length, current_length)
        min_length = min(min_length, current_length)
    average = 0
    if number_of_sequnces != 0:
        average = sum_length/number_of_sequnces
    return min_length, max_length, average

def main():
    shortest, longest, average = get_longest_and_average_sequence_length()
    print "Najkrotsza: ", shortest
    print "Najdluzsza: ", longest
    print "Srednia: ", average



if __name__ == '__main__':
    main()