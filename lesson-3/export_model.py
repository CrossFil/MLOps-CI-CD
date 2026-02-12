import torch
import torchvision.models as models

# Загружаем модель
model = models.mobilenet_v2(weights='DEFAULT')
model.eval()

# Делаем трассировку (превращаем в TorchScript)
example = torch.rand(1, 3, 224, 224)
traced_script_module = torch.jit.trace(model, example)

# Сохраняем в файл
traced_script_module.save("model.pt")
print("✅ Модель успешно сохранена как model.pt")
