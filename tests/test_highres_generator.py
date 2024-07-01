import pytest
import torch
import torch.nn as nn
from my_script import HighResGenerator  # Replace with the actual name of your script

@pytest.fixture
def model():
    input_dim = 100
    output_channels = 3
    return HighResGenerator(input_dim, output_channels)

def test_high_res_generator_initialization(model):
    """Test the initialization of the HighResGenerator model."""
    assert isinstance(model, nn.Module), "Model should be an instance of nn.Module"
    assert len(model.model) > 0, "Model layers should be defined"

def test_high_res_generator_forward_pass(model):
    """Test the forward pass of the HighResGenerator model."""
    # Create a dummy input tensor
    input_dim = 100
    example_input = torch.randn(1, input_dim)  # Example random noise vector

    # Ensure the model runs without errors
    output = model(example_input)
    assert output.shape == (1, 3, 2160, 3840), "Output shape should be (1, 3, 2160, 3840)"
    assert isinstance(output, torch.Tensor), "Output should be a tensor"
    assert output.dtype == torch.float32, "Output tensor should be of type float32"

def test_high_res_generator_cuda(model):
    """Test if the HighResGenerator model can be moved to CUDA."""
    if torch.cuda.is_available():
        model.cuda()
        input_dim = 100
        example_input = torch.randn(1, input_dim).cuda()
        output = model(example_input)
        assert output.is_cuda, "Output should be on CUDA"
        assert output.shape == (1, 3, 2160, 3840), "Output shape should be (1, 3, 2160, 3840)"
    else:
        pytest.skip("CUDA is not available")

