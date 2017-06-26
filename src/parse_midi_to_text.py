import os
import midi

pattern = midi.read_midifile("./midi/original/original_song.mid")
chunk_str_list = []

chunk_str = "rs_" + str(pattern.resolution)
chunk_str_list.append(chunk_str)

for i, chunk in enumerate(pattern[1]):

  chunk_str = ""

  if (chunk.name == "Note On"):
    chunk_str = chunk_str + str(chunk.tick) + "_" + "no" + "_" + str(chunk.pitch) + \
                  "_" + str(chunk.velocity)

    chunk_str_list.append(chunk_str)

  elif (chunk.name == "Set Tempo"):
    chunk_str = chunk_str + str(chunk.tick) + "_" + "st" + "_" + str(int(chunk.bpm)) + "_" + str(int(chunk.mpqn))
    chunk_str_list.append(chunk_str)

  elif (chunk.name == "Control Change"):
    chunk_str = chunk_str + str(chunk.tick) + "_" + "cc" + "_" + str(chunk.channel)  + "_" + \
                    str(chunk.data[0]) + "_" + str(chunk.data[1])
    chunk_str_list.append(chunk_str)


if not os.path.exists("./miditext/"):
  os.mkdir("./miditext/")
  os.mkdir("./miditext/original/")
elif not os.path.exists("./miditext/original/"):
  os.mkdir("./miditext/original/")

f = open('./miditext/original/original-song.txt', 'w')
for elm in chunk_str_list:
  f.write(str(elm) + "\n")
f.close()
