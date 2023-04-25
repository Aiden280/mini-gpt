import torch
from transformers import AutoTokenizer
import json
from gpt_model.gpt_decoder import GPTDecoder

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Load the saved state dictionary
state_dict = torch.load('models/taa.pt', map_location=torch.device('cpu'))

with open('config.json', 'r') as f:
    config = json.load(f)

tokenizer = AutoTokenizer.from_pretrained('gpt2')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model = GPTDecoder(
        vocab_size=tokenizer.vocab_size,
        d_model=config['d_model'],
        n_head=config['n_head'],
        d_ff=config['d_ff'],
        n_layer=config['n_layer'],
        max_seq_len=config['seq_len'],
        dropout=config['dropout'],
        padding_token_id=tokenizer.pad_token_id,
        device=device
    )

def chatbot(input_text):
    # Tokenize input text
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    # Generate response
    response = model.generate(
        input_ids=input_ids,
        max_length=50,
        temperature=0.8,
        repetition_penalty=1.2,
        do_sample=True,
        top_k=0,
        top_p=0.9,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id
    )

    # Decode response tokens and return as string
    return tokenizer.decode(response[0], skip_special_tokens=True)

while True:
    user_input = input("You: ")
    response = chatbot(user_input)
    print("Chatbot:", response)