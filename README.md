# Deep Improvisation

Improvisation like jazz song created by Deep LSTM Neural Network.

[Demo Link (SoundCloud)](https://soundcloud.com/tsyworks/sets/deep-imprivisation)

![screenshot](https://github.com/tatsuyah/deep-improvisation/blob/master/img/jazz.png)


## Usage

  #### 1. Set up environment (conda recommended)

  ```
  pip install -r requirements.txt
  ```

  #### 2. Parse MIDI file to text

  ```
  python ./src/parse_midi_to_text.py
  ```

  #### 3. Train the model (GPU recommended)

  ```
  python ./src/training.py
  ```

  #### 4. Generate music

  ```
  python ./src/generate_music.py
  ```

## Note

 MIDI format is usually consist of multiple track and this repository is currently not supporting automatic detection which track is main part of the song. So you may have to choose track as index of the pattern in `parse_midi_to_text.py`.


## License

MIT © [Tatsuya Hatanaka](https://github.com/tatsuyah)
