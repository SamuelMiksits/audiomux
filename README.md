# Audiomux

View/switch sinks and sources through pactl with a lot less typing and or headache. 

## Requirements
- Audio server such as pipewire/pulseaudio
- The command ```pactl``` (from package ```pulseaudio-utils``` in Debian)

Example output from my system:

![Audiomux output figure](/images/example.png)


## Usage

Launch the application with ```python3 /path/to/audiomux.py```

### Navigation

- Move down with k/down arrow.

- Move up with j/up arrow.

There are a couple of special navigation options:

- Go directly to a line number. If the number is single digit, enter the number and press enter. If the number is double digit, only press the two numbers.

- If you wish to go up a single digit amount of lines at once, you can do so with for instance '5j' if you want to go 5 lines down and '3k' if you want to go up 3 lines (this cannot be done with arrow keys).

### Set device

- Set device active device with 's', this issues the ```pactl set-default-(sink|source)``` command for the highlighted device.


## Older version

Here is the output from the old CLI for my system:

```
Active sink/source:
Default sink: CA0132 Sound Core3D [Sound Blaster Recon3D / Z-Series / Sound BlasterX AE-5 Plus] Analog Stereo
Default source: Meteor condenser microphone Analog Stereo
------------------------------
Selectable sinks/sources:
Sinks: 
1. CA0132 Sound Core3D [Sound Blaster Recon3D / Z-Series / Sound BlasterX AE-5 Plus] Analog Stereo
2. Starship/Matisse HD Audio Controller Digital Stereo (IEC958)
3. Navi 21/23 HDMI/DP Audio Controller Digital Stereo (HDMI 3)
4. Meteor condenser microphone Analog Stereo
Sources: 
5. Monitor of CA0132 Sound Core3D [Sound Blaster Recon3D / Z-Series / Sound BlasterX AE-5 Plus] Analog Stereo
6. CA0132 Sound Core3D [Sound Blaster Recon3D / Z-Series / Sound BlasterX AE-5 Plus] Analog Stereo
7. Monitor of Starship/Matisse HD Audio Controller Digital Stereo (IEC958)
8. Starship/Matisse HD Audio Controller Analog Stereo
9. Monitor of Navi 21/23 HDMI/DP Audio Controller Digital Stereo (HDMI 3)
10. Monitor of Meteor condenser microphone Analog Stereo
11. Meteor condenser microphone Analog Stereo
Select sink/source with number, 'e' for exit, any input to refresh list
```

I think that this version is a lot uglier, but can be a bit more powerful. Go to release v0.1.0 if you prefer this version