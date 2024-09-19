<p align="center"><img src="logo.png" width="128" height="128"></p>

# About
This app launches Minecraft and then joins the 2B2T server at the specified time. It's open source, you can inspect the code and decide whether it's clean or not or even build it yourself.
- Screenshot:
<img src="screenshot.png" width="256" >

# Requirements
**This settings are required to make the app work:**
- Launcher: Minecraft Launcher (The Minecraft Launcher window should be maximized and the game profile should be selected.) (Don't worry if you have installed the Minecraft in a different than the default directory, the app lets you choose it if it can't find it.)
- Video Settings > GUI Scale: 2 (Might work on other scales but it has been tested on this scale.)
- Both Minecraft Launcher and Minecraft Client languages should be English (US).
- If you have a Minecraft Client custom theme that changes the visuals of the buttons, disable it.

Adjust these settings before **running the scheduler**.

> [!IMPORTANT]
> Both Minecraft Launcher and Minecraft Client languages should be English (US). If you don't set them into English, the app won't recognise the buttons to click. Also the game profile (version or maybe the cheat client e.g. "fabric-1.21.1") must be selected in the Minecraft Launcher before running the app in order to make it work properly. Make sure the buttons in the client are in default style.

> [!NOTE]
> The app was tested in GUI Scale: 2, default button styles (no themes). Even with the change of these variables the app could work but haven't been tested yet.

# Usage
- Download [2B2T-Scheduler.exe](https://github.com/cagritaskn/2b2t-join-scheduler/releases/download/releasev1.1/2B2T-Scheduler.exe).
- Set the requirements in the **Requirements** title above for app to work properly.
- Open the [2B2T-Scheduler.exe](https://github.com/cagritaskn/2b2t-join-scheduler/releases/download/releasev1.1/2B2T-Scheduler.exe) and specify the time then click on **Activate**.

# Running the app as a Python script
Clone the repository, go into the directory where schedulerapp.py is located, open a command prompt in it's directory and run the command:
```
python schedulerapp.py
```

Or you can turn it into an exe by opening a command prompt in it's directory (the directory where schedulerapp.py is located) and running the command:

```
pyinstaller schedulerapp.spec
```

# Contact
If you face any issues or errors you can contact me at:
Discord: "kegrisko." (The ID has a dot at the end)

# Dupe
This project works well with the cactus dupe. (Planning on adding the popbob bed dupe later.)

# License
This code is licensed under the GNU General Public License v3. **You can only use this code in open-source clients that you release under the same license! Using it in closed-source/proprietary clients is not allowed.**
