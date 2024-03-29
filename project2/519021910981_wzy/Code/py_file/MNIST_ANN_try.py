import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision.datasets import MNIST
from torchvision.transforms import Compose, ToTensor, Normalize
from torch.utils.data import DataLoader


BATCH_SIZE = 512
# 一次输入量
EPOCHS = 2
# 总共训练批次
gpu_abailable = torch.cuda.is_available()
print(gpu_abailable)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 判断是否使用GPU


# 拿数据
def get_dataloader(train, batch_size=BATCH_SIZE):
    transform_fn = Compose([
        ToTensor(),
        Normalize(mean=(0.1307,), std=(0.3081,))
    ])  # mean和std的形状与通道数相同

    dataset = MNIST(download=True, root='./data',
                    train=train, transform=transform_fn)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return data_loader


train_loader = get_dataloader(train=True)
test_loader = get_dataloader(train=False)


# Create ANN Model
class ANNModel(nn.Module):

    def __init__(self):
        super(ANNModel, self).__init__()

        # Linear function 1: 784 --> 500
        self.fc1 = nn.Linear(1*28*28, 500)

        # Linear function 2: 500 --> 150
        self.fc2 = nn.Linear(500, 150)

        # Linear function 3: 150 --> 10
        self.fc3 = nn.Linear(150, 10)

    def forward(self, input):

        # reshape input
        x = input.view([-1, 1*28*28])

        # Linear function 1
        x = self.fc1(x)

        # Non-linearity 1
        x = F.relu(x)

        # Linear function 2
        x = self.fc2(x)

        # Non-linearity 2
        x = F.relu(x)

        # Linear function 3
        out = self.fc3(x)

        out = F.log_softmax(out, dim=1)

        return out


# 连接到GPU
model = ANNModel().to(DEVICE)
# 创建优化器并传入参数
#learning_rate = 0.02
#optimizer = optim.SGD(model.parameters(), lr=learning_rate)
optimizer = optim.Adam(model.parameters())


def train(model, device, train_loader, optimizer, epoch):
    # 将模型转为train模式
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        # 重置优化器梯度
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        # backward传播
        loss.backward()
        # 更新参数
        optimizer.step()
        if((batch_idx) % 30) == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))


def test(model, device, test_loader):
    # 将模型转为test模式
    model.eval()
    # loss
    test_loss = 0
    # 正确数
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


# 进行两次训练，第二次训练取第一次训练得出的hyperparameters
for epoch in range(1, EPOCHS+1):
    train(model, DEVICE, train_loader, optimizer, epoch)
    test(model, DEVICE, test_loader)
