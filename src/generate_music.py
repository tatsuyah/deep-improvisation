from __future__ import print_function
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import os
import midi


model = load_model("./model/model.h5")
model.load_weights("./model/weights.h5")

f = open('./miditext/original/original-song.txt', 'r')
music_as_chunks = []
for elm in f:
  music_as_chunks.append(elm.rstrip("\n"))
f.close()
resolution = 1440
music_as_chunks = music_as_chunks[1:]

unique_chunks = sorted(list(set(music_as_chunks)))
chunk_indices = dict((c, i) for i, c in enumerate(unique_chunks))
indices_chunk = dict((i, c) for i, c in enumerate(unique_chunks))

maxlen = 15
start_index = random.randint(0, len(music_as_chunks) - maxlen - 1)

def sample(preds, temperature=1.0):
  preds = np.asarray(preds).astype('float64')
  preds = np.log(preds) / temperature
  exp_preds = np.exp(preds)
  preds = exp_preds / np.sum(exp_preds)
  probas = np.random.multinomial(1, preds, 1)
  return np.argmax(probas)

sampled_chunks = random.sample(music_as_chunks, maxlen)
generated =  []
part_of_song = music_as_chunks[0: maxlen]
generated.extend(part_of_song)
sys.stdout.write(str(generated))

chunk_length = 1000
for i in range(chunk_length):
  x = np.zeros((1, maxlen, len(unique_chunks)))
  for t, chunk in enumerate(part_of_song):
    x[0, t, chunk_indices[chunk]] = 1.

  preds = model.predict(x, verbose=0)[0]
  distributions = [0.2,  0.6, 1.0, 1.4]
  weight = [0.3, 0.5, 0.1, 0.1]
  distribution = np.random.choice(distributions, p=weight)
  next_index = sample(preds, distribution)
  next_char = indices_chunk[next_index]

  generated.extend([next_char])
  part_of_song = part_of_song[1:]
  part_of_song.extend([next_char])

  sys.stdout.flush()
print()

if not os.path.exists("./midi/"):
  os.mkdir("./midi/")
  os.mkdir("./midi/generated/")
elif not os.path.exists("./midi/generated/"):
  os.mkdir("./midi/generated")
file = "./midi/generated/generated-song.mid"

pattern = midi.Pattern(resolution=resolution)

track = midi.Track()
pattern.append(track)

for chunk in generated:
  chunk_info = chunk.split("_")
  event_type = chunk_info[1]

  if event_type == "no":
    tick = int(chunk_info[0])
    pitch = int(chunk_info[2])
    velocity = int(chunk_info[3])

    e = midi.NoteOnEvent(tick=tick, channel=0, velocity=velocity, pitch=pitch)
    track.append(e)

  elif event_type == "st":
    tick = int(chunk_info[0])
    bpm = int(chunk_info[2])
    mpqn = int(chunk_info[3])
    ev = midi.SetTempoEvent(tick=tick, bpm=bpm, mpqn=mpqn)
    track.append(ev)

  elif event_type == "cc":
    control = int(chunk_info[3])
    value = int(chunk_info[4])
    e = midi.ControlChangeEvent(channel=0, control=control, value=value)
    track.append(e)

end_event = midi.EndOfTrackEvent(tick=1)
track.append(end_event)

midi.write_midifile(file, pattern)
