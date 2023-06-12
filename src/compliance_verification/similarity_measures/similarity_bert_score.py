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
import re

import numpy as np
import transformers
import logging

from bert_score import BERTScorer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

REPLACE_BY_SPACE = re.compile('[/(){}\[\]\|@,;]')
REMOVE_ADDITION_SPACES = re.compile('[\s+]')
REMOVE_SYMBOLS = re.compile('[^0-9a-z #+_]')
REMOVE_NUM = re.compile('[\d+]')
STOPWORDS = set(stopwords.words('english'))


def clean_text(txt):
    lematizer = WordNetLemmatizer()
    txt = str(txt).lower()
    txt = REMOVE_ADDITION_SPACES.sub(' ', txt)
    txt = REPLACE_BY_SPACE.sub(' ', txt)
    txt = REMOVE_NUM.sub('', txt)
    txt = REMOVE_SYMBOLS.sub('', txt)
    txt = ' '.join(word for word in txt.split() if word not in STOPWORDS)
    txt = ' '.join(word for word in txt.split() if (len(word) >= 2 and len(word) <= 20))
    txt = txt.replace(' not ', ' ')
    txt = ' '.join([lematizer.lemmatize(word) for word in txt.split()])
    # txt = ' '.join([stemmer.stem(word) for word in txt.split()])
    return txt


def load_transformers():
    transformers.tokenization_utils.logger.setLevel(logging.ERROR)
    transformers.configuration_utils.logger.setLevel(logging.ERROR)
    transformers.modeling_utils.logger.setLevel(logging.ERROR)


def get_sentence_similarities(activities, sentence_with_time):
    load_transformers()
    sentence_with_time = clean_text(sentence_with_time)
    clean_sentence_with_time = len(activities) * [sentence_with_time]
    clean_activities = []
    for activity in activities:
        clean_activities.append(clean_text(activity))
    scorer = BERTScorer(lang="en", rescale_with_baseline=True)
    P, R, F1 = scorer.score(clean_activities, clean_sentence_with_time)
    activities_sorted_by_similarity = np.vstack((activities, F1)).T
    activities_sorted_by_similarity = sorted(activities_sorted_by_similarity, key=lambda x: float(x[1]), reverse=True)
    return activities_sorted_by_similarity


def main():
    activities_sorted_by_similarity = ''.join(str(activity_similarity) for activity_similarity in get_sentence_similarities(['sales department member', 'finance department', 'sales'], 'sales department'))
    print(activities_sorted_by_similarity)


if __name__ == '__main__':
    main()
