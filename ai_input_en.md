# English Document: Auto Perceive Input Method Status by Sound.md
```markdown
# Auto Perceive Chinese & English Input Method Status via Sound

## Introduction
In daily work and typing scenarios, people usually mix Chinese and English input frequently.
It is easy to get confused about the current input method status when you are distracted or not looking at the screen, which causes wrong input content and reduces typing efficiency greatly.

To solve this common problem, this lightweight background solution is designed:
Automatically enable retro keystroke sound reminder when using English input method, and keep silent when switching to Chinese input method. Users can easily tell input mode only by hearing without checking the screen.

## Working Principle
1. Get keyboard input device nodes from system directory:
`/sys/class/input/event*`

2. Open the device file `/dev/input/event*` and read original keyboard input events in blocking mode.

3. Identify input method switch action through event rules:
4. Once switch action is detected, execute shell script to detect real-time input method status.

5. Control background buckle keystroke sound process automatically:
- Chinese Input Mode: Stop buckle process, mute all typing sound
- English Input Mode: Start buckle process, play retro keystroke sound

## Core Shell Script
```bash
#!/bin/bash
# Input method status detect & sound control script
for x in `seq 5`;do
    i=`fcitx5-remote`
    if [ "y""$i" == "y1" ];then
        # Close keystroke sound in Chinese mode
        killall -9 buckle
    else
        # Start keystroke sound in English mode
        if [ -z $(pidof buckle) ];then
            buckle &
        fi
    fi
    sleep 0.2
done
Running Process
Background program silently monitors global keyboard underlying events
Capture hotkey action of switching input method
Verify stable input method status repeatedly
Automatically turn on or off keystroke sound program
Distinguish input status simply by auditory feedback
Features & Advantages
Low CPU & memory consumption, smooth background operation
Realize blind typing judgment without screen watching
Developed based on native Linux input interface, stable and reliable
Simple code structure, convenient for secondary development
Completely local offline operation, safe and privacy-friendly
Adapt to most mainstream Linux desktop systems
