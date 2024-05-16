import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GPTQConfig, pipeline
from pathlib import Path
#import textwrap
#from markdown import markdown
from app import config

model_path = Path('app/ai_model/model')
tokenizer_path = Path('app/ai_model/tokenizer')
HF_TOKEN = config.settings.HF_TOKEN
model = "google/gemma-2b-it"
device="cpu"
max_new_tokens=1024
do_sample: bool = True
temperature: float = 0.1
top_k: int = 10
top_p: float = 0.1

def get_model_tokenizer(HF_TOKEN: str = HF_TOKEN, 
                         model: str = model, 
                         device: str = device, 
                         quantized: bool = False,
                         # model_path: Path = model_path,
                         # tokenizer_path: Path = tokenizer_path
                         ):
  tokenizer = AutoTokenizer.from_pretrained(model, token=HF_TOKEN, device=device)

  if quantized:
    pass
    # quantization_config = GPTQConfig(
    #     bits=4,
    #     group_size=128,
    #     dataset="c4", # the original datasets used in GPTQ paper [‘wikitext2’,‘c4’,‘c4-new’,‘ptb’,‘ptb-new’]
    #     desc_act=False,
    #     tokenizer=tokenizer,
    #     batch_size=1,
    # )  
    # model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path="google/gemma-2b-it",
    #                                             token=HF_TOKEN,
    #                                             quantization_config=quantization_config,
    #                                             device_map=device
    #                                             ) # requires: !pip install -q accelerate optimum auto-gptq 
  else:
      model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path="google/gemma-2b-it", 
                                                  token=HF_TOKEN,
                                                  torch_dtype=torch.float16,
                                                  #device_map=device
                                                  ) 

  return model, tokenizer



class ChatState:
  """
  Manages the conversation history for a turn-based chatbot
  Follows the turn-based conversation guidelines for the Gemma family of models
  documented at https://ai.google.dev/gemma/docs/formatting
  Reference: https://ai.google.dev/gemma/docs/gemma_chat 
  But we use HF: https://huggingface.co/google/gemma-2b-it
  """

  def __init__(self, model, tokenizer):    # , system: str|None = None
    """
    """
    self.model = model
    self.tokenizer = tokenizer
    self.history = [] 
    self.llm_pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

  def generate(self, user_message):
    """
    """   
    self.history.append({"role": "user", "content": user_message}) 
    prompt = self.history 
    tokenized_prompt = self.llm_pipeline.tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
    response = self.llm_pipeline(
        tokenized_prompt,
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p
    )
    model_response = response[0]["generated_text"][len(tokenized_prompt):] #response[0]["generated_text"].replace(tokenized_prompt, "")  
    
    self.history.append({"role": "model", "content": model_response})
    return self.history

  def get_full_history_generator(self):
    """
    Yields elements of the chat history one by one (user message, model response).
    """
    for message in self.history:
      yield message



def get_chatmodel(model_path: Path = model_path,
                  tokenizer_path: Path = tokenizer_path):
  """ """
  if not (os.path.exists(model_path) and os.path.exists(tokenizer_path)
          and len(os.listdir(model_path))>0 and len(os.listdir(tokenizer_path))>0):
    model, tokenizer = get_model_tokenizer()
    model.save_pretrained(model_path) 
    tokenizer.save_pretrained(tokenizer_path) 

  model = AutoModelForCausalLM.from_pretrained(model_path)
  tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
  chat_model = ChatState(model, tokenizer)
  return chat_model

chat_model = get_chatmodel()

  



