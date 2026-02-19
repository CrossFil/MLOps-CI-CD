import torch
import sys
from PIL import Image
from torchvision import transforms

def predict(image_path):
    try:
        # load
        model = torch.jit.load("model.pt")
        model.eval()
        
        # foto perp
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        input_image = Image.open(image_path).convert('RGB')
        input_tensor = preprocess(input_image).unsqueeze(0)

        # Neural network forward pass
        with torch.no_grad():
            output = model(input_tensor)

        # Calculate Top 3 predictions
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top3_prob, top3_catid = torch.topk(probabilities, 3)

        print(f"🧠 Results for {image_path}:")
        for i in range(top3_prob.size(0)):
            print(f"   ID {top3_catid[i].item()}: {top3_prob[i].item()*100:.2f}%")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 inference.py <image_path>")
    else:
        predict(sys.argv[1])
