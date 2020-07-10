import gc
import onnx
import json
import onnxruntime as rt
from model import Albert


from flask import Flask
from flask import request, Response
from flask import jsonify

class App(Flask):

    def __init__(self, name):
        super(App, self).__init__(name)
        
        self.model  = rt.InferenceSession('./states/message_classifier.onnx')
        self.albert = Albert()
        print("Worker started")

app = App(__name__)

# model = MessageClassifier().to(device)
# model.eval()
# model.load_state_dict(torch.load('./states/weights.pt', map_location='cpu'))
# output = model(embedding)
# print(float(output))

# model  = rt.InferenceSession('./states/message_classifier.onnx')
# ort_inputs  = {model.get_inputs()[0].name: embedding.detach().cpu().numpy()}
# ort_outs = model.run(None, ort_inputs)
# print(ort_outs[0])


@app.route('/parse', methods=["POST"])
def parse_message():

    content  = request.get_json()
    
    message  = content['text']
    embedding = app.albert.get_embedding(message)
    ort_inputs  = {app.model.get_inputs()[0].name: embedding.detach().cpu().numpy()}
    ort_outs = app.model.run(None, ort_inputs)
 
    label = 1 if float(ort_outs[0][0])>0.65 else 0

    response = {
        'status':'success',
        'class':label,
        'confidence': round(float(ort_outs[0][0]),2)
    }
    gc.collect()

    return jsonify(response)
