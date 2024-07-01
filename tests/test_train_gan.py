# test_train_gan.py
import pytest
import torch
import torch.nn as nn
from unittest.mock import patch, MagicMock
from my_script import train_gan  # Replace with the actual name of your script

@pytest.fixture
def mock_highres_models():
    with patch('my_script.HighResGenerator') as MockGenerator, \
         patch('my_script.HighResDiscriminator') as MockDiscriminator:
        
        mock_generator = MockGenerator.return_value
        mock_discriminator = MockDiscriminator.return_value
        
        yield mock_generator, mock_discriminator

@pytest.fixture
def mock_torch_components():
    with patch('my_script.optim.Adam') as MockAdam, \
         patch('my_script.nn.BCELoss') as MockBCELoss, \
         patch('my_script.DataLoader') as MockDataLoader, \
         patch('my_script.datasets.ImageFolder') as MockImageFolder, \
         patch('my_script.save_image') as MockSaveImage:
        
        mock_adam = MockAdam.return_value
        mock_bceloss = MockBCELoss.return_value
        mock_dataloader = MockDataLoader.return_value
        mock_imagefolder = MockImageFolder.return_value
        mock_saveimage = MockSaveImage
        
        yield mock_adam, mock_bceloss, mock_dataloader, mock_imagefolder, mock_saveimage

def test_train_gan_initialization(mock_highres_models, mock_torch_components):
    mock_generator, mock_discriminator = mock_highres_models
    mock_adam, mock_bceloss, mock_dataloader, mock_imagefolder, mock_saveimage = mock_torch_components
    
    # Mock the dataset and dataloader to contain one batch of images
    mock_imagefolder.__len__.return_value = 1
    mock_dataloader.__iter__.return_value = iter([torch.randn(4, 3, 2160, 3840), None])
    
    # Call the training function with minimal epochs and batch size
    train_gan(epochs=1, batch_size=4, dataset_path='data/4k_dataset', learning_rate=0.0002, beta1=0.5, beta2=0.999)
    
    # Check if the models were initialized
    mock_generator.to.assert_called_once()
    mock_discriminator.to.assert_called_once()
    
    # Check if the optimizers were created
    mock_adam.assert_any_call(mock_generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
    mock_adam.assert_any_call(mock_discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))
    
    # Check if the loss function was created
    mock_bceloss.assert_called_once()

def test_train_gan_training_loop(mock_highres_models, mock_torch_components):
    mock_generator, mock_discriminator = mock_highres_models
    mock_adam, mock_bceloss, mock_dataloader, mock_imagefolder, mock_saveimage = mock_torch_components
    
    # Mock the dataset and dataloader to contain one batch of images
    mock_imagefolder.__len__.return_value = 1
    mock_dataloader.__iter__.return_value = iter([(torch.randn(4, 3, 2160, 3840), None)])
    
    # Call the training function with minimal epochs and batch size
    train_gan(epochs=1, batch_size=4, dataset_path='data/4k_dataset', learning_rate=0.0002, beta1=0.5, beta2=0.999)
    
    # Check if the forward pass of the generator and discriminator was called
    mock_generator.assert_called()
    mock_discriminator.assert_called()
    
    # Check if the backward pass and optimizer step was called
    mock_adam.zero_grad.assert_called()
    mock_adam.step.assert_called()

    # Check if images were saved
    mock_saveimage.assert_called()

