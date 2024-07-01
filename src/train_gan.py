import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.utils import save_image
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# Import the generator and discriminator
from highres_generator import HighResGenerator
from highres_discriminator import HighResDiscriminator

def train_gan(epochs, batch_size, dataset_path, learning_rate=0.0002, beta1=0.5, beta2=0.999):
    # Set device to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Initialize the generator and discriminator
    generator = HighResGenerator(input_dim=100, output_channels=3).to(device)
    discriminator = HighResDiscriminator().to(device)

    # Set up optimizers for both G and D
    optimizer_G = optim.Adam(generator.parameters(), lr=learning_rate, betas=(beta1, beta2))
    optimizer_D = optim.Adam(discriminator.parameters(), lr=learning_rate, betas=(beta1, beta2))

    # Loss function
    adversarial_loss = nn.BCELoss()

    # Load data
    transform = transforms.Compose([
        transforms.Resize((2160, 3840)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5])
    ])
    dataset = datasets.ImageFolder(root=dataset_path, transform=transform)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Training loop
    for epoch in range(epochs):
        for i, (imgs, _) in enumerate(dataloader):
            # Adversarial ground truths
            valid = torch.ones(imgs.size(0), 1, device=device)
            fake = torch.zeros(imgs.size(0), 1, device=device)

            # Configure input
            real_imgs = imgs.to(device)
            z = torch.randn(imgs.size(0), 100, device=device)

            # -----------------
            #  Train Generator
            # -----------------
            optimizer_G.zero_grad()
            generated_imgs = generator(z)
            g_loss = adversarial_loss(discriminator(generated_imgs), valid)
            g_loss.backward()
            optimizer_G.step()

            # ---------------------
            #  Train Discriminator
            # ---------------------
            optimizer_D.zero_grad()
            real_loss = adversarial_loss(discriminator(real_imgs), valid)
            fake_loss = adversarial_loss(discriminator(generated_imgs.detach()), fake)
            d_loss = (real_loss + fake_loss) / 2
            d_loss.backward()
            optimizer_D.step()

            # Print progress
            print(f"[Epoch {epoch}/{epochs}] [Batch {i}/{len(dataloader)}] [D loss: {d_loss.item()}] [G loss: {g_loss.item()}]")

            # Save Images periodically
            if i % 100 == 0:
                save_image(generated_imgs.data[:25], f"outputs/{epoch}_{i}.png", nrow=5, normalize=True)

if __name__ == "__main__":
    train_gan(epochs=25, batch_size=4, dataset_path='data/4k_dataset')
