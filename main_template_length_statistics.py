__author__ = 'Konrad Kopciuch'

from Repository.MongoTemplateRepository import MongoTemplateRepository
from NeedlemanWunsch.NeedlemanWunsch import *

def get_longest_and_average_sequence_length():
    repo = MongoTemplateRepository()
    max_length = 0
    sum_length = 0
    number_of_sequnces = 0
    for id, sequence, resolution in repo.get_all_unmodified_sequences():
        number_of_sequnces+=1
        current_length = len(sequence)
        print current_length
        sum_length += current_length
        max_length = max(max_length, current_length)
    return (max_length, sum_length/number_of_sequnces)


if __name__ == '__main__':
    longest, average = get_longest_and_average_sequence_length()
    print "Najdluzsza: ", longest
    print "Srednia: ", average
