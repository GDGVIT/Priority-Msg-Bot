import torch
import torch.nn as nn
from transformers import AlbertTokenizer, AlbertModel

class MessageClassifier(nn.Module):

    def __init__(self):
        super(MessageClassifier, self).__init__()
        self.fc = nn.Linear(768, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, embedding):
        x = self.fc(embedding)
        x = self.sigmoid(x)
        return x



class Albert:

    def __init__(self):
        super(Albert, self).__init__()
        self.tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
        big_model = AlbertModel.from_pretrained('albert-base-v2').eval()
        self.model = torch.quantization.quantize_dynamic(
                    big_model, {torch.nn.Bilinear}, dtype=torch.qint8
                    )

    def tokenize(self, text):
        inputs = self.tokenizer.encode_plus(

              text,

              max_length=300,

              add_special_tokens=True, # Add '[CLS]' and '[SEP]'

              return_token_type_ids=False,

              pad_to_max_length=True,

              return_attention_mask=True,
                         
              return_tensors='pt',  # Return PyTorch tensors

            )
        
        return inputs
    
    def get_embedding(self,text):

        inputs = self.tokenize(text)
        _, pooled_output = self.model(inputs["input_ids"], inputs["attention_mask"])
        return pooled_output
        

