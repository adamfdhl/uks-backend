import numpy as np
from gensim.models.fasttext import FastText
from nltk.tokenize import word_tokenize
from nltk import RegexpTokenizer
import tensorflow as tf
import tensorflow.keras.backend as K
from keras.models import load_model

base_path = "/Users/adamfdhl/Documents/Adam/College/Code/semantic-similarity"
global model_embedding
global deep_module

def diff_sentence_length(sentence_1, sentence_2):
  len_sentence_1 = len(sentence_1)
  len_sentence_2 = len(sentence_2)

  return abs(len_sentence_1 - len_sentence_2)/(len_sentence_1 + len_sentence_2)

def cosine_similarity(sentence_1, sentence_2):
  # tokenization
  list_1 = word_tokenize(sentence_1.lower())
  list_2 = word_tokenize(sentence_2.lower())

  # into set of words
  set_1 = {w for w in list_1}
  set_2 = {w for w in list_2}

  vector_1 = []
  vector_2 = []

  # form a set containing keywords of both strings  
  rvector = set_1.union(set_2)  
  for w in rvector: 
    if w in set_1: 
      vector_1.append(1)
    else: vector_1.append(0)
    if w in set_2: 
      vector_2.append(1)
    else: vector_2.append(0)
  c = 0

  # calculate cosine  
  for i in range(len(rvector)): 
    c+= vector_1[i]*vector_2[i] 
  cosine = c / float((sum(vector_1)*sum(vector_2))**0.5) 
  return cosine

def shallow_module(sentence_1, sentence_2):
  diff_length = diff_sentence_length(sentence_1, sentence_2)
  cosine = cosine_similarity(sentence_1, sentence_2)

  return cosine - diff_length

def to_vector(sentence, feature_size = 300, max_len=100):
  tokenized_sentence = word_tokenize(sentence)

  tokenizer = RegexpTokenizer(r"\w+")
  words = tokenizer.tokenize(sentence)

  words = tokenizer.tokenize(sentence)
  clean_words = [word for word in words if word.isalpha()]
  fix_words = [word for word in clean_words if len(word) > 1]
  sentence_embeddings = []

  for word in fix_words:
    sentence_embeddings.append(model_embedding.wv[word])
    if (len(sentence_embeddings) >= max_len):
      break
      
  sentence_embeddings = sentence_embeddings + [[0] * feature_size
                for _ in range(max(0, max_len - len(sentence_embeddings)))
                ]
  sentence_embeddings = np.array(sentence_embeddings).astype(np.float32)

  return sentence_embeddings

def compute_pearson(y_true, y_pred):
  # Pearson's correlation coefficient = covariance(X, Y) / (stdv(X) * stdv(Y))
  fs_pred = y_pred - np.mean(y_pred)
  fs_true = y_true - np.mean(y_true)
  covariance = np.mean(fs_true * fs_pred)

  stdv_true = np.std(y_true)
  stdv_pred = np.std(y_pred)

  return covariance / (stdv_true * stdv_pred)

def pearson_correlation(y_true, y_pred):
  x = y_true
  y = y_pred
  mx = K.mean(x)
  my = K.mean(y)
  xm, ym = x-mx, y-my
  r_num = K.sum(tf.multiply(xm,ym))
  r_den = K.sqrt(tf.multiply(K.sum(K.square(xm)), K.sum(K.square(ym))))
  r = r_num / r_den

  r = K.maximum(K.minimum(r, 1.0), -1.0)
  return r

#https://stackoverflow.com/questions/46619869/how-to-specify-the-correlation-coefficient-as-the-loss-function-in-keras
def correlation_coefficient_loss(y_true, y_pred):
  x = y_true
  y = y_pred
  mx = K.mean(x)
  my = K.mean(y)
  xm, ym = x-mx, y-my
  r_num = K.sum(tf.multiply(xm,ym))
  r_den = K.sqrt(tf.multiply(K.sum(K.square(xm)), K.sum(K.square(ym))))
  r = r_num / r_den

  r = K.maximum(K.minimum(r, 1.0), -1.0)
  return K.square(1 - r)

model_embedding = FastText.load(base_path + "/Models/Word Embedding/idwiki.model")
deep_module = load_model(base_path + "/Models/model_32_02_05", custom_objects = {
    "correlation_coefficient_loss": correlation_coefficient_loss,
    "pearson_correlation": pearson_correlation
  })

def get_lextical_similarity(sentence_1, sentence_2):
  lexical_similarity = []
  result = shallow_module(sentence_1, sentence_2)
  lexical_similarity.append(result)
  lexical_similarity = np.array(lexical_similarity).astype(np.float32)
  return lexical_similarity

def preprocess_sentence(sentence):
  embedded_sentence = to_vector(sentence)
  embedded_sentence = [embedded_sentence]
  embedded_sentence = np.array(embedded_sentence).astype(np.float32)
  return embedded_sentence

def integration_module(sentence_1, sentence_2, proportion_semantic, shared_parameter):
  embedded_sentence_1 = preprocess_sentence(sentence_1)
  embedded_sentence_2 = preprocess_sentence(sentence_2)
  lexical_similarity = get_lextical_similarity(sentence_1, sentence_2)
  semantic_similarity = deep_module.predict([embedded_sentence_1, embedded_sentence_2]).reshape(-1)
  result = shared_parameter * semantic_similarity[0] + proportion_semantic * lexical_similarity
  return result[0]
