import cx_Freeze

exe = [cx_Freeze.Executable("RecoverHiTek.py", base = "Win32GUI")] # <-- HERE

cx_Freeze.setup(
    name = "Mizatorian RecoverHiTek",
    version = "1.0",
    options = {"build_exe": {"packages": ["pygame", "random", "math", "sys", "io", "time"],  
        "include_files": ["assets/guitar1.mp3","assets/sfxr_bounce.wav","assets/sfxr_ohoh3.wav",
        "assets/hitek1.png","assets/hitek2.png","assets/hitek3.png",
        "assets/hitek4.png","assets/hitek5.png","assets/hitek6.png",
        "assets/bg.png","assets/bgmenu.png","assets/player.png",
        "assets/sfxr_score.wav","at01.ttf"]}},
    executables = exe
) 