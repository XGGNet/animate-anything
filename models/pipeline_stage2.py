transparent_unet_pretrained_model_path: "./output/latent/transparent_unet"
transparent_VAE_pretrained_model_path: "./output/latent/transparent_VAE"


motion_mask: True
motion_strength: True
in_channels: 5 # 5 or 9

output_dir: "output/stage_2_eval"

# Adds offset noise to training. See https://www.crosslabs.org/blog/diffusion-with-offset-noise
# If this is enabled, rescale_schedule will be disabled.
offset_noise_strength: 0.1
use_offset_noise: False

# Uses schedule rescale, also known as the "better" offset noise. See https://arxiv.org/pdf/2305.08891.pdf
# If this is enabled, offset noise will be disabled.
rescale_schedule: True

# When True, this extends all items in all enabled datasets to the highest length. 
# For example, if you have 200 videos and 10 images, 10 images will be duplicated to the length of 200. 
extend_dataset: False

# Caches the latents (Frames-Image -> VAE -> Latent) to a HDD or SDD. 
# The latents will be saved under your training folder, and loaded automatically for training.
# This both saves memory and speeds up training and takes very little disk space.
cache_latents: False

# If you have cached latents set to `True` and have a directory of cached latents,
# you can skip the caching process and load previously saved ones. 
cached_latent_dir: null #/path/to/cached_latents

# Train the text encoder for the model. LoRA Training overrides this setting.
train_text_encoder: False

# https://github.com/cloneofsimo/lora (NOT Compatible with webui extension)
# This is the first, original implementation of LoRA by cloneofsimo.
# Use this version if you want to maintain compatibility to the original version.

# https://github.com/ExponentialML/Stable-LoRA/tree/main (Compatible with webui text2video extension)
# This is an implementation based off of the original LoRA repository by Microsoft, and the default LoRA method here.
# It works a different by using embeddings instead of the intermediate activations (Linear || Conv).
# This means that there isn't an extra function when doing low ranking adaption.
# It solely saves the weight differential between the initialized weights and updates. 

# "cloneofsimo" or "stable_lora"
lora_version: "cloneofsimo"

# Use LoRA for the UNET model.
use_unet_lora: False

# Use LoRA for the Text Encoder. If this is set, the text encoder for the model will not be trained.
use_text_lora: False

# LoRA Dropout. This parameter adds the probability of randomly zeros out elements. Helps prevent overfitting.
# See: https://pytorch.org/docs/stable/generated/torch.nn.Dropout.html
lora_unet_dropout: 0.1

lora_text_dropout: 0.1

# https://github.com/kabachuha/sd-webui-text2video
# This saves a LoRA that is compatible with the text2video webui extension.
# It only works when the lora version is 'stable_lora'.
# This is also a DIFFERENT implementation than Kohya's, so it will NOT work the same implementation.
save_lora_for_webui: True

# The LoRA file will be converted to a different format to be compatible with the webui extension.
# The difference between this and 'save_lora_for_webui' is that you can continue training a Diffusers pipeline model
# when this version is set to False
only_lora_for_webui: False

# Choose whether or not ito save the full pretrained model weights for both checkpoints and after training.
# The only time you want this off is if you're doing full LoRA training.
save_pretrained_model: True

# The modules to use for LoRA. Different from 'trainable_modules'.
unet_lora_modules:
  - "UNet3DConditionModel"
  #- "ResnetBlock2D"
  #- "TransformerTemporalModel"
  #- "Transformer2DModel"
  #- "CrossAttention"
  #- "Attention"
  #- "GEGLU"
  #- "TemporalConvLayer"

# The modules to use for LoRA. Different from `trainable_text_modules`.
text_encoder_lora_modules:
  - "CLIPEncoderLayer"
  #- "CLIPAttention"

# The rank for LoRA training. With ModelScope, the maximum should be 1024. 
# VRAM increases with higher rank, lower when decreased.
lora_rank: 16

# You can train multiple datasets at once. They will be joined together for training.
# Simply remove the line you don't need, or keep them all for mixed training.

# 'image': A folder of images and captions (.txt)
# 'folder': A folder a videos and captions (.txt)
# 'json': The JSON file created with automatic BLIP2 captions using https://github.com/ExponentialML/Video-BLIP2-Preprocessor
# 'video_json': a video foler and a json caption file
# 'single_video': A single video file.mp4 and text prompt
dataset_types: 
  #- 'single_video'
  #- 'folder'
  # - 'image'
  - 'video_blip'
  # - 'video_json'

# Training data parameters
train_data:
  width: 384
  height: 384
  use_bucketing: False
  return_mask: True
  return_motion: True
  sample_start_idx: 0
  fps: 8
  n_sample_frames: 8

  json_path: ''


# Validation data parameters.
validation_data:

  # A custom prompt that is different from your training dataset. 
  prompt: ""

  prompt_image: ""

  # Whether or not to sample preview during training (Requires more VRAM).
  sample_preview: True

  # The number of frames to sample during validation.
  num_frames: 8

  # Height and width of validation sample.
  width: 384
  height: 384

  # Number of inference steps when generating the video.
  num_inference_steps: 25

  # CFG scale
  guidance_scale: 9

# Learning rate for AdamW
learning_rate: 3.0e-05
lr_scheduler: "cosine"
lr_warmup_steps: 20
# Weight decay. Higher = more regularization. Lower = closer to dataset.
adam_weight_decay: 0

# Optimizer parameters for the UNET. Overrides base learning rate parameters.
extra_unet_params: null
  #learning_rate: 1e-5
  #adam_weight_decay: 1e-4

# Optimizer parameters for the Text Encoder. Overrides base learning rate parameters.
extra_text_encoder_params: null
  #learning_rate: 1e-4
  #adam_weight_decay: 0.2

# How many batches to train. Not to be confused with video frames.
train_batch_size: 8
image_batch_size: 48
gradient_accumulation_steps: 4
# Maximum number of train steps. Model is saved after training.
max_train_steps: 2000

# Saves a model every nth step.
checkpointing_steps: 200

# How many steps to do for validation if sample_preview is enabled.
validation_steps: 50

# Which modules we want to unfreeze for the UNET. Advanced usage.
trainable_modules:
  - "all"
  # If you want to ignore temporal attention entirely, remove "attn1-2" and replace with ".attentions"
  # This is for self attetion. Activates for spatial and temporal dimensions if n_sample_frames > 1
  - "attn1"
  - ".attentions"
  
  # This is for cross attention (image & text data). Activates for spatial and temporal dimensions if n_sample_frames > 1
  - "attn2"
  - "conv_in"
  
  #  Convolution networks that hold temporal information. Activates for spatial and temporal dimensions if n_sample_frames > 1
  - "temp_conv"
  - "motion"


# Which modules we want to unfreeze for the Text Encoder. Advanced usage.
trainable_text_modules: null

# Seed for validation.
seed: null

# Whether or not we want to use mixed precision with accelerate
mixed_precision: "fp16"

# This seems to be incompatible at the moment.
use_8bit_adam: False 

# Trades VRAM usage for speed. You lose roughly 20% of training speed, but save a lot of VRAM.
# If you need to save more VRAM, it can also be enabled for the text encoder, but reduces speed x2.
gradient_checkpointing: True
text_encoder_gradient_checkpointing: False

# Xformers must be installed for best memory savings and performance (< Pytorch 2.0)
enable_xformers_memory_efficient_attention: False

# Use scaled dot product attention (Only available with >= Torch 2.0)
enable_torch_2_attn: True
