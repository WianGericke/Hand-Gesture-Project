Design Doc for a general gesture controller for mac

This document will outline the design and thinking process behind the general gesture controller

OVERVIEW
The gesture controller will work through three main layers, accompanied by gesture specifications for the shape of each gesture, as well as individual profiles of the shape of a user's hands in order to ensure that the user can easily utilize the functionality of the gesture controller without interruption from stray hands.

MAIN LAYERS
1. CAPTURE - the capture layer lives in the background, an invisible capture layer that opens the webcam and allows for a place for the ANALYZER (layer 2) to live. This layer is essentially a housing layer that operates the camera and allows for other pieces of software to live on and operate from.

2. ANALYZER - This is where the brunt of the software will live. This layer ingests the camera feed frame-by-frame and performs the processing, identifying handlandmarks, angles and distances between landmarks, and processes that information into different gestures which are then sent to DISPATCH (layer 3).
    
The ANALYZER will perform a few different roles in order to facilitate the different types of gestures that can be utilized to execute other functions. One of these roles is the ANALYZER's ability to distinguish between once off gestures (such as for a pause or song skip) and continuous gestures (such as for a pinch and twist to adjust volume).

Because of this, the gesture ANALYZER will be able to differentiate between "states" of each gesture, it must be able to tell whether this pinch for volume control is the first pinch that has been detected, or if it is a continuation of a previous pinch, so that we can continuosly adjust volume as the user is twisting their hand.

Finally, each gesture will be exported from the ANALYZER via a "ping" which will be a message export that we utulize to ensure that the dispatch is taking the appropriate action when a gesture is detected.
These gesture pings will contain as much information as possible about the gesture including:
    - Gesture Type: single, continuous, etc
    - Gesture Meaning: "point" "fist" "thumbs-up" "pinch" etc
        - Most of these gestures will be configurable to be either a single gesture or coninuous so that we can remap,
        for example, volume control to use a pointed finger swiping left and right to adjust volume as opposed to the original pinch and twist. Gesture type will be an [int] which will be fed through an [enum] to map to specific actions.
    - Handedness: Whether a gesture comes from the right or left hand
    - Time: a timestamp so that continuous gestures are easier to work with
    - Confidence: simple confidence score for the detected gesture, used to ensure that the software is sure of intent for things like turning the laptop off
    - Generally, continuous gestures will also ping with handlandmark angles and/or landmark proximity to facilitate continuous gesture controls.

Each item in a ping will belong to a named field to ensure code readability and ease of use.

The ANALYZER will also feature some "debouncing" mechanism. this will allow for the analyzer to not cut continuous gestures short if the gesture is accidentally not detected for a few frames, this is to ensure that there is no "jitter" when using gesture control. 

EXAMPLE GESTURE PING:
    - PING: [[TYPE:1], [MEANING:PINCH_START], [HANDEDNESS:left], [CONFIDENCE:0.98], [ANGLE:45deg], [TIME:19:32:47]]
    - PING: [[TYPE:1], [MEANING:PINCH_UPDATE], [HANDEDNESS:left], [CONFIDENCE:0.96], [ANGLE:55deg], [TIME:19:32:48], [ANGLE_DELTA:+10deg_diff]]
    - PING: [[TYPE:1], [MEANING:PINCH_END], [HANDEDNESS:left], [CONFIDENCE:0.98], [ANGLE:57deg], [TIME:19:32:49], [ANGLE_DELTA:+12deg_diff]]

3. DISPATCH - This layer takes pings from the ANALYZER (layer 2) and maps specific gestures to some sort of function that can be determined by the user.
    For example, the user can configure the software such that:
        - A closed fist held to the camera for 3 seconds locks their laptop
        - A pinch and wrist twist will adjust volume
        - swiping their whole hand over the screen swaps between apps on their laptop
        - swiping with two fingers skips the current song
        - two fingers held up pauses their song
The dispatch layer very specifically takes just gesture pings in from the analyzer layer and converts them into some sort of action, in this way it is essentially a closed box, however, the settings can be configured in order to ensure that each gesture can be handpicked for whatever the user would like it to do. This does also mean that gestures may be used as hotkeys to launch specific apps or to open certain files.

GESTURE SPECIFICATIONS/PROFILES
Each gesture profile will consist of a list of angles and handlandmarks such that they can be easily categorized by the ANALYZER layer. it will be a simple list of angles and handlandmarks, no executable code within the file. files should be able to be swapped out so that if the ANALYZER is ever reused, gestures that aren't in use can be removed so that the analyzer doesn't recognize gestures that serve no purpose. Each gesture spec will also contain information on how long the gesture must be held before the corresponding ping and subsequently action take place. This can range from instant to multiple seconds/minutes if the user desires.

More specifically, each gesture will contain information on handlandmarks that must be in close proximity or the angles between them to qualify as a gesture.

USER PROFILE & HAND RECOGNITION
When the user first calibrates the hand gesture controller, the software will create a profile of sorts of the user's hand shape. This profile will consist of palm size, size of finger segments, and ratios between those numbers. This is to ensure that false positive hand signals do not mistakenly operate the user's computer.

OPEN QUESTIONS
1. How and where does debouncing occur? what is the threshhold?
2. Exact mechanism for profiling the user's hand shape to ensure accurate use
3. How to ensure that profiling each gesture, to see if it comes from the user, doesn't take too long. If profiling takes too long, the software may feel slow to respond, taking away from the feel of gesturing at the laptop to get things done.


Gesture Analyzer tool V1 scope:
    - CAPTURE (layer 1)                 (invisible layer to operate camera)
    - ANALYZER (layer 2)                (analyzation layer for action ping)
    - DISPATCH (layer 3)                (matching pings to real actions)
    - gesture specs (data, YAML)        (gesture maps)
    - gesture to action map (data, YAML)(gesture to action map)

Gesture Ananlyzer tool future scope:
    - user hand profile + calibration routine
    - GUI for visualizing tracking + configuring mappings
    - default/override settings split