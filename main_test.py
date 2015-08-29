__author__ = 'Konrad Kopciuch'

from Repository.MongoTemplateRepository import MongoTemplateRepository
from NeedlemanWunsch import NeedlemanWunsch, Alignment

def get_longest_and_average_sequence_length():
    repo = MongoTemplateRepository()
    max_length = 0
    sum_length = 0
    number_of_sequnces = 0
    for sequence in repo.get_all_unmodified_sequences():
        number_of_sequnces+=1
        current_length = len(sequence)
        sum_length += current_length
        max_length = max(max_length, current_length)
    return (max_length, sum_length/number_of_sequnces)

def align_query_sequence_to_database(query):
    repo = MongoTemplateRepository()
    for sequence in repo.get_all_unmodified_sequences():
        nw = NeedlemanWunsch(query, sequence)
        nw.align()
        print nw.get_score()


if __name__ == '__main__':
    #print get_longest_and_average_sequence_length()
    align_query_sequence_to_database("GCCGAUAUAGCUCAGUUGGUAGAGCAGCGCAUUCGUAAUGCGAAGGUCGUAGGUUCGACUCCUAUUAUCGGCACCA")