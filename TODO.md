### To Do & Was Done

# Meta 

[] Get codacity badge (login, upload, etc)  
https://docs.codacy.com/getting-started/codacy-quickstart/#signing-up

# Code1

[] Create and test setup script

[] finish Readme.md for release

# Wishlist (next version)

[] Make new repository of **UseFullTools** with scripts in utilities/

[] Get rid of Files tab and make buttons at tope, using Emojis for Save, Open, and New:

💾 📂 🗑️


# Marketing

[  ] PM directly people on reddit, work discord, instagram? for alpha testers, see positive responses to oobabooga post.

[  ] Post to sub reddits when polished and ready for beta:

https://www.reddit.com/r/MachineLearning/

https://www.reddit.com/r/artificial/

https://www.reddit.com/r/Oobabooga/ ?

https://www.reddit.com/r/MediaSynthesis/

https://www.reddit.com/r/ArtificialInteligence/

https://www.reddit.com/r/LocalLLaMA/

https://www.reddit.com/r/ollama/

https://www.reddit.com/r/LocalLLaMA/

[] Email your project heroes (living)

[]- [Allison Parrish](https://www.decontextualize.com) (thematically)

aparrish@nyu.edu

[]- [Kate Compton](https://github.com/galaxykate) (structurally)
 
[]- [Rick Rubin](https://en.wikipedia.org/wiki/Rick_Rubin) (musically)
 
[]- [Jonathan Mast](https://jonathanmast.com/) (promptly)
 
[]- [Douglas Hofstadter](https://en.wikipedia.org/wiki/Douglas_Hofstadter) (subconsciously)

### Progress

[] Spit and polish for general consumption

### Completed


[X] Setup workflow with pycharm and github

[X] Hardcoded Integration with 5 APIs, install and test (this isn't the best way to do this)  

[X] **Ollama**
* kill with: systemctl stop ollama.service

[X] **LM Studio**, installed, running and DL models, working
( run appimage with the --no-sandbox-option)

* run: ~/Downloads/LM_Studio-0.2.27.AppImage --no-sandbox

[X] **GPT4All**, dled, installed, and... works

[X] **LocalAI**, dled, installed, running, fixing, works

* kill with: systemctl stop local-ai.service

[X] **oobabooga**, that was difficult

[X] Fix text edge case where list starts with somthing other than a number like: 

(it wasn't working because we weren't using the fucntion!)

I like food, and here are some good ones

1. potatoes they're great

2. love french fries too!

3. [X] add custom LLM API location and POST/GET template?! Put it in settings.cfg

[X] make adaptive llm finder, POST/GET template, and API key handler 

Screen Recording to Anim gif pipeline: 

(basic pipeline, not in cement)

1) record with SimnpleScreenRecorder
2) create a pallet with ffmpeg

ffmpeg -i video.mkv -vf "fps=8,scale=320:-1:flags=lanczos,palettegen=max_colors=32" -y palette_32.png

3) create a gif with ffmpeg"

ffmpeg -i video.mkv -i palette4.png -filter_complex "fps=4,paletteuse" -y output_video.gif

4) optimize with gifsicle

gifsicle -O3 output_video.gif -o output_video_1.gif