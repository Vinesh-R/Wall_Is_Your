from platform import system

if system().lower() == "windows" :
    import winsound
    platform = "windows"
    available = True

elif system().lower() in ["linux", "debian"] :
    import subprocess
    platform = "linux"
    available = True

else :
    platform = "unk"
    available = False

play = None
AudioProg = ""

audioList = {
    "aventurier" : "media/sounds/sword.wav",
    "gameOverA" : "media/sounds/game_over_a.wav",
    "mario" : "media/sounds/mario2.wav",
    "gameOverM" : "media/sounds/game_over_mario.wav",
    "Game Over" : "media/sounds/gameOver.wav",
    "victory" : "media/sounds/victory.wav"
}


def checkAudioProg() -> str:
    global available

    aplay = ["aplay", "--version"]
    pactl = ["paplay", "--version"]

    try :
        subprocess.call(aplay, stdout=subprocess.PIPE)
        return "aplay"

    except FileNotFoundError :
        pass

    try :
        subprocess.call(pactl, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "paplay"
    except FileNotFoundError:
        pass
        
    available = False
    return "Null"


def playWindow(sound:str) -> None :
    winsound.PlaySound(f"{audioList[sound]}", winsound.SND_FILENAME)

def aPlay(sound:str) -> None:
    cmd = ["aplay", "--quiet", f"{audioList[sound]}"]
    subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def playPaPlay(sound:str) -> None:
    cmd = ["paplay", f"{audioList[sound]}"]
    subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def playNone(sound) -> None :
    pass


def init() -> None:
    global play, AudioProg

    if platform == "linux" : AudioProg = checkAudioProg()

    if available :

        if platform == "windows" :
            play = playWindow

        elif AudioProg == "aplay" :
            play = aPlay

        elif AudioProg == "paplay" :
            play = playPaPlay

        else :
            play = playNone

    else :
        play = playNone
