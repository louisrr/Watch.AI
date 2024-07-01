import torch
import torch.nn as nn

class HighResDiscriminator(nn.Module):
    def __init__(self):
        super(HighResDiscriminator, self).__init__()
        # Define layers capable of discriminating high-resolution images (4K resolution)
        self.model = nn.Sequential(
            # Input size: 3 x 2160 x 3840
            nn.Conv2d(3, 64, kernel_size=4, stride=2, padding=1),  # Output size: 64 x 1080 x 1920
            nn.LeakyReLU(0.2, inplace=True),

            # Second layer
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1),  # Output size: 128 x 540 x 960
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),

            # Third layer
            nn.Conv2d(128, 256, kernel_size=4, stride=2, padding=1),  # Output size: 256 x 270 x 480
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True),

            # Fourth layer
            nn.Conv2d(256, 512, kernel_size=4, stride=2, padding=1),  # Output size: 512 x 135 x 240
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2, inplace=True),

            # Fifth layer
            nn.Conv2d(512, 1024, kernel_size=4, stride=2, padding=1),  # Output size: 1024 x 67 x 120
            nn.BatchNorm2d(1024),
            nn.LeakyReLU(0.2, inplace=True),

            # Sixth layer
            nn.Conv2d(1024, 2048, kernel_size=4, stride=2, padding=1),  # Output size: 2048 x 33 x 60
            nn.BatchNorm2d(2048),
            nn.LeakyReLU(0.2, inplace=True),

            # Seventh layer to reduce dimensionality further if necessary
            nn.Conv2d(2048, 2048, kernel_size=4, stride=2, padding=1),  # Output size: 2048 x 16 x 30
            nn.BatchNorm2d(2048),
            nn.LeakyReLU(0.2, inplace=True),

            # Flatten and final fully connected layer
            nn.Flatten(),
            nn.Linear(2048 * 16 * 30, 1),  # Adjust the size according to the output of the last conv layer
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)

# Check for CUDA availability and set default device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# Instantiate the discriminator and move it to the GPU if available
discriminator = HighResDiscriminator().to(device)

# Create a dummy high-resolution image tensor and move it to the GPU if available
example_input = torch.randn(1, 3, 2160, 3840).to(device)  # Example with 4K resolution

# Generate the output using the discriminator
output = discriminator(example_input)
print("Output:", output)  # Outputs the probability of the input being a real image
