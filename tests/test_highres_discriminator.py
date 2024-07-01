# test_high_res_discriminator.py
import pytest
import torch
import torch.nn as nn
from my_script import HighResDiscriminator  # Replace with the actual name of your script

@pytest.fixture
def model():
    return HighResDiscriminator()

def test_high_res_discriminator_initialization(model):
    """Test the initialization of the HighResDiscriminator model."""
    assert isinstance(model, nn.Module), "Model should be an instance of nn.Module"
    assert len(model.model) > 0, "Model layers should be defined"

def test_high_res_discriminator_forward_pass(model):
    """Test the forward pass of the HighResDiscriminator model."""
    # Create a dummy high-resolution image tensor
    example_input = torch.randn(1, 3, 2160, 3840)  # Example with 4K resolution

    # Ensure the model runs without errors
    output = model(example_input)
    assert output.shape == (1, 1), "Output shape should be (1, 1)"
    assert isinstance(output, torch.Tensor), "Output should be a tensor"
    assert output.dtype == torch.float32, "Output tensor should be of type float32"

def test_high_res_discriminator_cuda(model):
    """Test if the HighResDiscriminator model can be moved to CUDA."""
    if torch.cuda.is_available():
        model.cuda()
        example_input = torch.randn(1, 3, 2160, 3840).cuda()
        output = model(example_input)
        assert output.is_cuda, "Output should be on CUDA"
    else:
        pytest.skip("CUDA is not available")
