# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline
import argparse
from gradio_client import Client
import torch._dynamo

# torch._dynamo.config.suppress_errors = True
# torch._dynamo.disable()

# def LLama_model(prompt):
#     model_id = "openai-community/gpt2"

#     # Load tokenizer and model
#     tokenizer = AutoTokenizer.from_pretrained(model_id)
#     model = AutoModelForCausalLM.from_pretrained(
#         model_id,
#         torch_dtype=torch.bfloat16,
#     ).to('cpu')

#     # Apply the chat template
#     messages = [
#         {"role": "user", "content": prompt},
#     ]
#     prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
#     chat_input = tokenizer(prompt, return_tensors="pt").to('cpu')

#     # Generate response
#     chat_outputs = model.generate(**chat_input, max_new_tokens=1000).to('cpu')
#     response = tokenizer.decode(chat_outputs[0], skip_special_tokens=True) # Decode only the response part
#     #print("\nAssistant Response:", response)

#     return response

# def bitnet(prompt):
    # model_id = "microsoft/bitnet-b1.58-2B-4T"
    # # Load tokenizer and model
    # tokenizer = AutoTokenizer.from_pretrained (model_id)
    # model = AutoModelForCausalLM. from_pretrained(
    # model_id,)
    # # Apply the chat template
    # messages = [
    # {"role": "user", "content": prompt}]
    # prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True) 
    # chat_input = tokenizer (prompt, return_tensors="pt")
    # # Generate response
    # chat_outputs = model.generate (**chat_input, max_new_tokens=500)
    # response = tokenizer.decode(chat_outputs[0], skip_special_tokens=True) 
    # return response
    
# def bitnet_Colab(prompt):
#     client = Client("https://d9da784f2bff68fb65.gradio.live",hf_token='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')
#     result = client.predict(
#         prompt=prompt,
#         api_name="/predict"
#     )

#     return result


from groq import Groq

client = Groq(
    api_key="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",
)
def llama(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content

# inp=input()
# print(bitnet_Colab(inp))

#Token: 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

#Example: Rule 1: Dont run in the hallway. Rule 2: Dont bring bags. Rule 3: Dont wear headphones. Caption: Children are running in the hallway with bags. Which rules have been violated in the caption according to the mentioned rules and why?  
#Example: Rule 1: Dont run in the hallway. Rule 2: Dont bring bags. Rule 3: Dont wear headphones. Caption: Children are running in the grass. Which rules have been violated in the caption according to the mentioned rules and why? If no rules are viloated just reply "No viloation of rules." Make your answer short and dont assume anything. 

# import requests
# from huggingface_hub import InferenceClient,ChatCompletionOutput
# # Your Hugging Face API token

# def hugf_Model(prompt):
#     API_TOKEN = "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"
#     messages = [
#         {
#             "role": "user",
#             "content": prompt,
#         }
#     ]

#     client = InferenceClient(
#         provider="novita",
#         model="deepseek-ai/DeepSeek-Prover-V2-671B",
#         api_key=API_TOKEN,
#     )
#     return client.chat_completion(messages, max_tokens=500)['choices'][0]['message']['content']


# ipt=input()

# print(hugf_Model(ipt))
