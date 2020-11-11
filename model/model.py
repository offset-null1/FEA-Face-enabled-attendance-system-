import torch
from torchvision import models


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = models.resnet18(pretrained=True)
for param in model.parameters():
    param.requires_grad=False

net = torch.nn.Sequential(list(model.children())[:-1])trace_input = torch.rand(1,3,224,224) #random input just to trace
script_module = torch.jit.trace(net, trace_input)
script_module.save('resnet18_finetune.pt') 
