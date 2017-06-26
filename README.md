# deep improvisation

## Usage

  #### 1. Set up environment (conda recommended)

  ```
  pip install -r requirements.txt
  ```

  #### 2. Parse MIDI file to text

  ```
  python parse_midi_to_text.py
  ```

  #### 3. Train the model (GPU recommended)

  ```
  python training.py
  ```

  #### 4. Generate music

  ```
  python generate_music.py
  ```

## Note

 MIDI format is usually consist of multiple track and this repository is currently not supporting automatic detection which track is main part of the song. So you may have to choose track as index of the pattern in `parse_midi_to_text.py`.


## License

MIT © [Tatsuya Hatanaka](https://github.com/tatsuyah)
