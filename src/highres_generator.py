import torch
import torch.nn as nn

class HighResGenerator(nn.Module):
    def __init__(self, input_dim, output_channels):
        super(HighResGenerator, self).__init__()
        # This example starts with a dense layer to project the input dimension into a smaller spatial dimension with more depth
        self.init_size = 8  # Smaller spatial dimension
        self.l1 = nn.Sequential(nn.Linear(input_dim, 512 * self.init_size ** 2))

        # Sequential model to upscale from initial smaller spatial dimension to 3840x2160 (4K)
        self.model = nn.Sequential(
            # First upsampling to 16x16
            nn.ConvTranspose2d(512, 256, 4, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            # Second upsampling to 32x32
            nn.ConvTranspose2d(256, 256, 4, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            # Third upsampling to 64x64
            nn.ConvTranspose2d(256, 128, 4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            # Fourth upsampling to 128x128
            nn.ConvTranspose2d(128, 128, 4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            # Fifth upsampling to 256x256
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            # Sixth upsampling to 512x512
            nn.ConvTranspose2d(64, 32, 4, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(True),
            # Seventh upsampling to 1024x1024
            nn.ConvTranspose2d(32, 32, 4, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(True),
            # Eighth upsampling to 2048x2048
            nn.ConvTranspose2d(32, 16, 4, stride=2, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(True),
            # Ninth upsampling to 4096x4096
            nn.ConvTranspose2d(16, 16, 4, stride=2, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(True),
            # Reduce to 3840x2160 (4K)
            nn.ConvTranspose2d(16, output_channels, 4, stride=1, padding=1),
            nn.Tanh()  # Using Tanh for output normalization (image values between -1 and 1)
        )

    def forward(self, z):
        # Project and reshape the input noise tensor `z` to the initial size
        out = self.l1(z)
        out = out.view(out.shape[0], 512, self.init_size, self.init_size)
        # Apply the sequential model to generate a high-resolution image
        img = self.model(out)
        # Crop to 4K resolution (3840x2160)
        img = img[:, :, :2160, :3840]
        return img

# Check for CUDA availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# Instantiate the generator and move it to the appropriate device (GPU if available)
input_dim = 100  # Example size of latent dimension
gen = HighResGenerator(input_dim=input_dim, output_channels=3).to(device)

# Create a dummy input tensor and move it to the GPU if available
z = torch.randn(1, input_dim).to(device)  # Example random noise vector

# Generate the image using the model
output_image = gen(z)
print("Output image shape:", output_image.shape)  # Should be (1, 3, 2160, 3840) for a single 4K image
