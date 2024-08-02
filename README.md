<div align="center">
    <img src="/images/masks_base_banner_01.png" alt="Logo">
</div>

<center>

![Python 3.12.3](https://img.shields.io/badge/python-3.12.3-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) 
![Last Commit](https://img.shields.io/github/last-commit/kleer001/cuesubplot) 
![GitHub Stars](https://img.shields.io/github/stars/kleer001/cuesubplot?style=social)

</center>

# ***cuesubplot:*** **Procedurally craft chat responses, simply and reliably!**

## :speech_balloon: What? 
Cuesubplot is a browser based, hard-coded (not generalized __yet__ :sweat_smile:) network for creating lists and building on them in a way that is stable and  **reliable**. All from the comfort of your favorite local LLM API.


# :bulb: Why?

<details>
  <summary>Enhance LLM Capabilities & Streamline Workflow</summary>

- Develop a solution that enables (local) LLMs to generate long and complex multistep outputs effectively, such as detailed learning programs or comprehensive critiques.

- Eliminate the need for manual copy-pasting in workflows to improve efficiency and maintain the quality of generated content while trying new things.

</details>

<details>
  <summary>Create a Custom Solution</summary>

- Leverage insights from experts like Jonathan Mast to design a tailored programming solution that integrates the strengths of LLMs and utilizes innovative tools like [Gradio](https://www.gradio.app/) and inspiration from [Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

</details>

<details>
  <summary>Contribute to the Community</summary>

- Actively participate in the local LLM evolution among programmers and users who share a passion for generating text and exploring the capabilities of LLMs and enhancing the ease of the chat workflow.

</details>



> ## :zap: How? 
> ## **1** - Set a ***[Role](https://platform.openai.com/docs/guides/prompt-engineering/tactic-ask-the-model-to-adopt-a-persona)***
> ## **2** - Create a ***[List](https://mathworld.wolfram.com/LissajousCurve.html)***
> ## **3** - [***Riff***](https://www.collinsdictionary.com/dictionary/english/riff) on the list

## :rocket: Start (automagically)

<code>curl -fsSL https://raw.githubusercontent.com/kleer001/cuesubplot/master/install.sh | bash ; cd cuesubplot </code>
 

## :sparkles: Start (manual) 
* Make sure you have **git** installed (and **python3**)
* **Copy** the repo  
<code>git clone https://github.com/kleer001/cuesubplot ; cd cuesubplot </code>
* **Create** a local venv
* <code> python3 -m venv venv </code>
* **Activate** it
* <code> source venv/bin/activate </code>
* **Install** the dependencies  
<code> pip install -r requirements.txt </code>
* **Run** the program  
<code> python3 src/stage.py</code>


## :package: Currently supported LLMS platforms 
*in  settings.cfg*  

| LLM Platform | URL             | Endpoint             |
|--------------|-----------------|----------------------|
| [Ollama](https://ollama.ai/)       | localhost:11434 | /api/generate        |
| [LM Studio](https://lmstudio.ai/)    | localhost:1234  | /v1/chat/completions |
| [GPT4All](https://gpt4all.io/)      | localhost:4891  | /v1/completions      |
| [LocalAI](https://localai.io/)      | localhost:8080  | /v1/chat/completions |
| [llama.cpp](https://github.com/ggerganov/llama.cpp)    | localhost:8080  | /completion          |
| [oobabooga](https://github.com/oobabooga/text-generation-webui)    | localhost:5000  | /v1/chat/completions |

* Please suggest more free local LLMs if you like. And feel free to change your local settings.cfg to fit your own purposes. The structure should be self-evident from the examples in it.  
* Support for Chat-GPT, Perplexity, Claude, and other paid platforms is imminent, though not guaranteed. 

## :walking: GUI WALK THROUGH 
### :eyes: STAGE 
* 1 - At ***Role*** enter a role you want the LLM to take, a perspective, personality.   
This will be added as a prefix promptlet to the rest of the prompts you'll create.   
* 2 - At ***List generation*** enter the list you would like to generate. For best results use the phrasing something like
**"give me an ordered list of ..."**  

*I've done my best to be able to handle many types of list formats than an LLM can generate. 
But they can be very clever and create an edge case I hadn't anticipated. In that case feel free to hit submit again and wish for the best.*  
* 3 - Hit the ***Submit*** button to generate your list.   
* 4 - At ***Riff on the list*** enter a prompt to process items you've created.
* 5 - Once you're happy with your Riffing promptlet feel free to process the rest of your items.  



![Tab 1, The Stage](/images/Stage_01.png "Tab 1, The Stage")

### :writing_hand: FILES 

Here we can Save, Load, and clear the Stage.   
* **Save Results**: The files are named automagically based on your prompts, the date, and time.  
*  **Saved File**: The automatically generated file name once saved.  
* **File to Open**: You'll need to select a file to open first. Drop file or Click to upload.  
* **Open File**: You'll need to select a file to open first. Drop file or Click to upload. After that you can open it.  
* **File Status**: Feedback is important in any creative venture.

![Tab 2, Files](/images/Library_01.png "Tab 2, Files")


### :performing_arts: A FULL STAGE 

![Tab 1, The Stage](/images/FullStage_01.png "Tab 1, The Stage")

### :chart_with_upwards_trend: THE FLOW CHART

This, of course, leaves out important parts, but aims at addressing the important creative process flow.  
Like, there's a lot of work that goes into separating the results of the List cue results into separate list items that can be addressed individually.   
And there's nothing about the LLM settings or the APIs.  

![Program Flow, more or less](/images/flowChart_01.png "Flowchart")


### :brain: THE SETTINGS 

*Will be based on the local LLM the program detects that is currently running*

Please see <code> findLLM.py & settings.cfg </code>

If there are more than one running it will pick the first one it finds.   
* Model: Not all local LLMs let you specify the model through the API. Some require the user to load the model before the api will return a query.  
* Messy: Off by default. Messy on will display all the of the hidden Process Buttons, List Item text boxes, and Riffing Results. Gradio cannot create them on the fly. So, they're hidden until they're needed.  
* Maximum number of items: Default of 5. The number of List Items that are created with the interface (hidden by default).  
* Max Tokens, Temperature, etc... : Settings based on the API call of your specific LLM  



## :bug: COMMON PROBLEMS: 

**Q:** Why isn't my LLM responding?   
**A:** Please double-check that it's properly serving up API goodness.   
The settings.cfg file contains multiple popular local LLMs and their API end points.   
The findLLM.py uses that list to quickly search your system for a recognizable local LLM.  
If you run 'python3 findLLM' and it can't find anything then we need to turn on your local LLM.

**Q:**: My LLM is recognized. Why am I not getting output from cuesubplot?     
**A:** It might be that your local LLM hasn't loaded a model to working with.  
Please make sure that you have loaded up a model file that we can send a request to.   

**Q:** Anything else?  
**A:** We're still in early Alpha release, so, it's probably a bug and should be squashed. Please submit an issue, and we'll put it in the pile to be processed.   

## :wrench: CREDITS: 

stopwords.data file from: 
https://countwordsfree.com/stopwords

## :art: Inspirations 

### People

- [Allison Parrish](https://www.decontextualize.com) (thematically)  
- [Kate Compton](https://github.com/galaxykate) (structurally)  
- [Kurt Schwitters](https://en.wikipedia.org/wiki/Kurt_Schwitters) (graphically)  
- [Rick Rubin](https://en.wikipedia.org/wiki/Rick_Rubin) (musically)  
- [Jonathan Mast](https://jonathanmast.com/) (promptly)  
- [Douglas Hofstadter](https://en.wikipedia.org/wiki/Douglas_Hofstadter) (subconsciously)  

My family, friends, and other loved ones  
 *the ones still extant and those sadly extinct* :heart: 

## 🤝 Acknowledgments

I would like to express my gratitude to the following platforms and software for their inspiration and contributions:

- [ChatGPT](https://chatgpt.com/)
- [Perplexity](https://www.perplexity.ai/)
- [Claude](https://claude.ai/)
- [Houdini](https://www.sidefx.com/products/houdini/)
- [Nuke](https://www.foundry.com/products/nuke)
