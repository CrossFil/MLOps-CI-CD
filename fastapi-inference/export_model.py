import torch
import torchvision.models as models

# load the model
model = models.mobilenet_v2(weights='DEFAULT')
model.eval()

# perform tracing (convert to TorchScript)
example = torch.rand(1, 3, 224, 224)
traced_script_module = torch.jit.trace(model, example)

# save the file
traced_script_module.save("model.pt")
print("✅ Model successfully saved as model.pt")
