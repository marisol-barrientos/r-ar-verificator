#
# This file is part of r-ar-verificator.
#
# r-ar-verificator is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# r-ar-verificator is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with r-ar-verificator (file COPYING in the main directory). If not, see
# http://www.gnu.org/licenses/.
"""

"""

# Required Inputs for testing:
import spacy
from typing import List, Union, Any

# spaCy vectorizer and similarity function
nlp = spacy.load("en_core_web_md")


def activity_similarity_check_one_spacy(sentences_descr: List[str], sentences_log: List[str]) -> \
        tuple[list[Any], list[Union[str, list[str]]], list[Union[str, list[str]]], list[Union[int, Any]], list[
            Union[str, list[str]]], list[Union[int, Any]], list[Union[int, Any]]]:
    # Returns:
    # similarity_matrix
    # most_similar_sentences
    # corresponding_sentence_description
    # corresponding_sentence_log
    # corresponding_similarity_scores
    return __similarity_check_spacy(sentences_descr=sentences_descr, sentences_log=sentences_log)


# Approach of V2
def resource_activity_similarity_check_two_spacy(resources_descr: List[str], resources_matched_log: List[str]):

    # Calculate similarity
    resources_checked_descr = []
    resources_checked_log = []
    similarity_scores = []
    index = len(resources_descr)
    for i in range(index):
        # Transform resource of description and log into vector
        doc_descr = nlp(resources_descr[i])
        doc_log = nlp(resources_matched_log[i])

        # Similarity result
        similarity = doc_descr.similarity(doc_log)
        similarity_scores.append(similarity)
        # Resource checked log
        resources_checked_log.append(resources_matched_log[i])
        # Resource checked description
        resources_checked_descr.append(resources_descr[i])

    # Return similarity score and tuple of
    return resources_checked_log, resources_checked_descr, similarity_scores


def __similarity_check_spacy(sentences_descr: List[str], sentences_log: List[str]) -> \
        tuple[list[Any], list[Union[str, list[str]]], list[Union[str, list[str]]], list[Union[int, Any]], list[
            Union[str, list[str]]], list[Union[int, Any]], list[Union[int, Any]]]:
    # length of amount descr
    similarity_matrix = []

    for sent_log in sentences_log:
        sim_list = []
        doc_log = nlp(sent_log)
        for sent_descr in sentences_descr:
            doc_descr = nlp(sent_descr)
            sim_list.append(doc_log.similarity(doc_descr))
        similarity_matrix.append(sim_list)

    # 3. Refine this output process:
    most_similar_sentences = []
    corresponding_sentence_log = []
    corresponding_id_log = []
    corresponding_sentence_description = []
    corresponding_id_description = []
    corresponding_similarity_scores = []

    # Count to get the current process event from event log which is compared
    count_row = 0
    # Go through the similarity matrix
    for row in similarity_matrix:
        count_column = 0
        similarity_index = 0
        similarity_value = 0
        # Go through for every sentence the similarity to every sentence in the event log
        for value_sim in row:
            # Store the position and value of the most similar sentence
            if value_sim >= similarity_value:
                similarity_value = value_sim
                similarity_index = count_column
            count_column = count_column + 1

        # Add results
        most_similar_sentences.append(sentences_descr[similarity_index])
        corresponding_sentence_description.append(sentences_descr[similarity_index])
        corresponding_id_description.append(similarity_index + 1)
        corresponding_similarity_scores.append(similarity_value)

        corresponding_sentence_log.append(sentences_log[count_row])
        corresponding_id_log.append(count_row + 1)
        # Increase count for description list
        count_row = count_row + 1

    # Matrix of similarity scores, list of similar sentences, list of highest similarity score
    return similarity_matrix, most_similar_sentences, corresponding_sentence_description, corresponding_id_description, corresponding_sentence_log, corresponding_id_log, corresponding_similarity_scores
