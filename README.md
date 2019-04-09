# Dancing Lights

Supporting Dance Performances for Deaf and Hard of Hearing People through Lighting Effects [paper](https://drive.google.com/file/d/110YDLC42UPF5E4cwvmgw3WnwZKq_24PJ/view)

## File Description

```plain
.
├── main.py         main script
├── recorder.py     sound recording by pyaudio
├── tempo.py        beat detection by aubio
└── mhci.ino        script for controlling lighting with Arduino
```

## Environment

python 2.7.15 with [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/) and [aubio](https://aubio.org)
Arduino library [Adafruit_NeoPixel](https://github.com/adafruit/Adafruit_NeoPixel)

## Usage

This program first identifies beats from a given song; then it records sound and matches the current playing location to the original sound file. If matching is successful, it lights LED at beats through Arduino.

So files of music to be matched should be included in the same folder, and add command in line 100 in main.py to target the file. After Arduino board is connected and the music is played, execute the program by

```bash
./python main.py
```

Then type the command you set to match the music, and wait for LED to be lightened. Type `stop` to exit the program.

## Lighting Pattern

Lighting pattern is casually designed in `mhci.ino`.