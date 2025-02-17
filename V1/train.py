from seq2seq import seq2seq
import numpy as np
import json
import pickle


def get_token():
    with open('data/input_token.json') as f:
        inp_vocab = json.load(f)
    with open('data/output_token.json') as f:
        out_vocab = json.load(f)

    return inp_vocab, out_vocab


def get_convs():
    ff = pickle.load(open('data/convs_from.pkl', 'rb'))
    ft = pickle.load(open('data/convs_to.pkl', 'rb'))
    convs_from = []
    convs_to = []
    for (q, a) in zip(ff, ft):
        if len(q) < 100 and len(a) < 100:
            convs_from.append(q)
            convs_to.append(a)
    return convs_from, convs_to


input_token, output_token = get_token()
convs_from, convs_to = get_convs()
print(convs_from[0:3])
print(convs_to[0:3])
MAX_ENC_LEN = max([len(txt) for txt in convs_from])
MAX_DEC_LEN = max([len(txt) for txt in convs_to])
NUM_ENC_TOKENS = len(input_token)
NUM_DEC_TOKENS = len(output_token)
print(f'input:{NUM_ENC_TOKENS}')
print(f'output:{NUM_DEC_TOKENS}')
print(f'max enc:{MAX_ENC_LEN}')
print(f'max dec:{MAX_DEC_LEN}')
print(f'input sentences:{len(convs_from)}')
print(f'output sentences:{len(convs_to)}')
print(len(convs_from) * MAX_ENC_LEN * NUM_ENC_TOKENS*4)
encoder_input_data = np.zeros(
    (len(convs_from), MAX_ENC_LEN, NUM_ENC_TOKENS),
    dtype='float32')
decoder_input_data = np.zeros(
    (len(convs_from), MAX_DEC_LEN, NUM_DEC_TOKENS),
    dtype='float32')
decoder_target_data = np.zeros(
    (len(convs_from), MAX_DEC_LEN, NUM_DEC_TOKENS),
    dtype='float32')

for i, (input_text, target_text) in enumerate(zip(convs_from, convs_to)):
    for t, char in enumerate(input_text):
        encoder_input_data[i, t, input_token[char]] = 1.
    for t, char in enumerate(target_text):
        decoder_input_data[i, t, output_token[char]] = 1.
        if t > 0:
            decoder_target_data[i, t - 1, output_token[char]] = 1.
parameters = [convs_from, convs_to, input_token, output_token, NUM_ENC_TOKENS, NUM_DEC_TOKENS,
              MAX_ENC_LEN, MAX_DEC_LEN]
pickle.dump(parameters, open('parameters.pkl', 'wb'))

s2s = seq2seq()
s2s.create_models(NUM_ENC_TOKENS, NUM_DEC_TOKENS)
s2s.train(encoder_input_data, decoder_input_data,
          decoder_target_data, epochs=150)
