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
In this file a sentence similarity transformer will be implemented based on the word to vec technology of BERT
The sentences (Resource-Activity-Pairs) will be compared all possible from the process execution log
"""

# Required Inputs for testing:
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Any, Union

# BERT and Cosine Similarity of sklearn:
# Initialisation of BERT model
model = SentenceTransformer('bert-base-nli-mean-tokens')


def activity_similarity_check_one_bert(sentences_descr: List[str], sentences_log: List[str]) -> \
        tuple[list[Any], list[Union[str, list[str]]], list[Union[str, list[str]]], list[Union[int, Any]], list[
            Union[str, list[str]]], list[Union[int, Any]], list[Union[int, Any]]]:
    # Returns:
    # similarity_matrix
    # most_similar_sentences
    # corresponding_sentence_description
    # corresponding_sentence_log
    # corresponding_similarity_scores
    return __similarity_check_bert(sentences_descr=sentences_descr, sentences_log=sentences_log)


# Approach of V2
def resource_activity_similarity_check_two_bert(resources_descr: List[str], resources_matched_log: List[str]):

    # Apply bag of words from vectors_log and count the inverse frequency of tokens
    list_descr_matrix = model.encode(resources_descr, batch_size=1)
    list_log_matrix = model.encode(resources_matched_log, batch_size=1)

    # Calculate similarity
    resources_checked_descr = []
    resources_checked_log = []
    similarity_scores = []
    index = list_descr_matrix.shape[0]
    for i in range(index):
        # Similarity result
        similarity = cosine_similarity([list_descr_matrix[i]], [list_log_matrix[i]])[0][0]
        similarity_scores.append(similarity)
        # Resource checked log
        resources_checked_log.append(resources_matched_log[i])
        # Resource checked description
        resources_checked_descr.append(resources_descr[i])

    # Return similarity score and tuple of
    return resources_checked_log, resources_checked_descr, similarity_scores


def __similarity_check_bert(sentences_descr: List[str], sentences_log: List[str]) -> \
        tuple[list[Any], list[Union[str, list[str]]], list[Union[str, list[str]]], list[Union[int, Any]], list[
        Union[str, list[str]]], list[Union[int, Any]], list[Union[int, Any]]]:

    # Apply bag of words from vectors_log and count the inverse frequency of tokens
    vectors_log = model.encode(sentences_log, batch_size=1)
    vectors_descr = model.encode(sentences_descr, batch_size=1)

    # 2. Calculate cosine similarity:
    similarity_matrix = []
    # Every vector in the list of sentences is looped
    for vector_log in vectors_log:
        # Check every log vector with the list of description vectors
        # similarity_matrix format:
        # Columns: Similarity with every Activity in the Description
        # Rows: Stands for Activities in Log
        similarity_matrix.append(cosine_similarity([vector_log], vectors_descr[0:])[0])

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
        corresponding_id_description.append(similarity_index+1)
        corresponding_similarity_scores.append(similarity_value)

        corresponding_sentence_log.append(sentences_log[count_row])
        corresponding_id_log.append(count_row+1)
        # Increase count for description list
        count_row = count_row + 1

    # Matrix of similarity scores, list of similar sentences, list of highest similarity score
    return similarity_matrix, most_similar_sentences, corresponding_sentence_description, corresponding_id_description, corresponding_sentence_log, corresponding_id_log, corresponding_similarity_scores

