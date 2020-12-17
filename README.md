# shelly_music

This project is aimed to provide a little bit of fun to your home automation. If you have a MIDI file laying around you can use it to controll you shelly's around the house to creat a light show. 

Everything is based on the [mido](https://mido.readthedocs.io/en/latest/) package. 

## How to use it

You will need to configure three parts 

1. the midi file you want to serve
2. the IPs of your shelly devices 
3. The ```mod``` parameter. This should be set to the same number has shellys you want to use. This way each note coming from midi will be converted to match one of the shellys. You will get the best result with more shellys

## Next Steps

- [ ] Allow for more settings like songs, tempo ...
- [ ] Scan the network for shellys 
- [ ] Make it into a python lib
- [ ] Build a home assistant integration