import torch
import sys
from PIL import Image
from torchvision import transforms

def predict(image_path):
    try:
        # Загрузка
        model = torch.jit.load("model.pt")
        model.eval()
        
        # Подготовка фото
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        input_image = Image.open(image_path).convert('RGB')
        input_tensor = preprocess(input_image).unsqueeze(0)

        # Прогон через нейросеть
        with torch.no_grad():
            output = model(input_tensor)

        # Вычисление Топ-3
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top3_prob, top3_catid = torch.topk(probabilities, 3)

        print(f"🧠 Результаты для {image_path}:")
        for i in range(top3_prob.size(0)):
            print(f"   ID {top3_catid[i].item()}: {top3_prob[i].item()*100:.2f}%")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 inference.py <путь_к_картинке>")
    else:
        predict(sys.argv[1])
