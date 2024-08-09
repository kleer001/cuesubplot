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


[X] PM directly people on reddit, 
[] work discord, 
[] instagram? for alpha testers, see positive responses to oobabooga post.

[X] Post to sub reddits when -polished and ready for alpha-:

[] https://www.reddit.com/r/MistralAI/ (get .cfg working first)
[] https://www.reddit.com/r/OpenAI/ (get .cfg working first)
[] https://www.reddit.com/r/SideProject/
[] 
[]

[X] https://www.reddit.com/r/MachineLearning/  
[X] https://www.reddit.com/r/artificial/  
[X] https://www.reddit.com/r/Oobabooga/ ?  
[X] https://www.reddit.com/r/MediaSynthesis/  
[X] https://www.reddit.com/r/ArtificialInteligence/  
[X] https://www.reddit.com/r/LocalLLaMA/  
[X] https://www.reddit.com/r/ollama/  


And Facebook: 

https://www.facebook.com/groups/opensourcellms

And 2 Discords... Whatever they are? 

Twitter: 


1. **General AI and LLM Hashtags**:
   - #AI
   - #MachineLearning
   - #ArtificialIntelligence
   - #LLM (Large Language Model)
   - #DeepLearning
   - #NLP (Natural Language Processing)

2. **Open Source Software Hashtags**:
   - #OpenSource
   - #OSS (Open Source Software)
   - #FOSS (Free and Open Source Software)
   - #CodeForGood

3. **Community and Collaboration Hashtags**:
   - #DevCommunity
   - #OpenSourceCommunity
   - #AICommunity
   - #CollaborativeCoding

4. **Software Development Hashtags**:
   - #SoftwareDevelopment
   - #Coding
   - #Programming
   - #DevOps

5. **Fun and Engaging Hashtags**:
   - #TechForGood
   - #CodeMonkey (playful reference to coding)
   - #AIRevolution
   - #FutureOfAI

6. **Specific to Your Project**:
   - #CueSubPlot
   - #Chatbots
   - #LLMApplications
   - #AIChat


Citations:
[1] https://eugeneyan.com/writing/llm-bio/
[2] https://www.reddit.com/r/MachineLearning/comments/1afdxxd/p_ai_filter_local_llms_for_social_media_curation/
[3] https://aiascendant.substack.com/p/oss-vs-openai
[4] https://www.guardrailsai.com/blog/from-traditional-machine-learning-governance-to-llm-centric-ai-governance
[5] https://deepgram.com/ai-apps/twitter-bio-generator
[6] https://www.encora.com/insights/proprietary-vs-open-source-llms
[7] https://hdsr.mitpress.mit.edu/pub/aelql9qy/release/2
[8] https://srinstitute.utoronto.ca/news/gen-ai-llms-explainer


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


# Initial Alpha user email: 

thegreatpotatogod
Cool-Hornet4434
Flying_Madlad
cmdywrtr27



Thanks for your friendly feedback over at /r/Oobabooga! (about a month ago)

I'm launching the alpha version of my software 'cuesubplot' this week and thought you might be interested in joining. It simplifies expanding on list creation from prompts without the copy-pasting hassle. Kind of like a limited Automatic1111 for text. And yes, it's totally compatible with Oobabooga's API :)

The alpha will run for about a week before the survey comes out. Any feedback will be appreciated.

You can find the repository over at https://github.com/kleer001/cuesubplot

Please let me know if you're interested and would like to help out!

Best,
kleer001

typeform survey: 
https://zhjj6b3nj66.typeform.com/to/zAnky1FB

youtube video: 
https://youtu.be/nygwTchbaDs

title: Prototype procedural chat interface (works with 6+ LLM chat APIs). 



 I'm bubbling with excitement to present ***cuesubplot***. 

* It saves copy pasting when you want to create lists based off a prompt and then apply the same prompt to the items in that list. 

* I got tired of opening another document to save the list then copy paste each time I wanted to explore the prompts. 

* It will be leaving alpha by in a week or so. I would love feedback. **However, I understand everyone's got their own busy life.** 

* The only perk of use would be trying something new and helping out an fellow ambitious LLM user, and helping potentially more LLM users that want to explore procedural text generation. 

Check it out please over at: https://github.com/kleer001/cuesubplot

---

*If you do try it out please PM me so I can bother you with a* ***very short*** *survey once you've kicked the tires a little. It'd be a great help!*