# Instruct_Pix2Pix_PyQt5UI

这个程序是基于 InstructPix2Pix 模型的图像编辑工具，允许用户通过自然语言指令来编辑图像。

## 环境要求

- Python 3.7+
- CUDA 兼容的 NVIDIA GPU（推荐至少 6GB 显存）
- Anaconda 或 Miniconda

## 安装步骤

1. 克隆或下载此仓库到本地。
  
2. 创建并激活一个新的 Conda 环境：
  
  ```
  conda create -n instruct_pix2pix python=3.8
  conda activate instruct_pix2pix
  ```
  
3. 安装 PyTorch 和 CUDA：
  
  注意：PyTorch 和 CUDA 版本需要匹配。请访问 [PyTorch 官网](https://pytorch.org/get-started/locally/) 选择适合您系统的安装命令。
  
  例如，对于 CUDA Version: 12.5 ，您可以使用：
  
  ```
  pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
  ```
  
4. 安装其他依赖：
  
  ```
  pip install diffusers transformers accelerate safetensors
  pip install PyQt5
  ```
  
5. 验证安装：
  打开 Python 解释器并运行：
  
  ```python
  import torch
  print(torch.cuda.is_available())
  print(torch.version.cuda)
  ```
  
  如果输出 `True` 和您的 CUDA 版本号，则安装成功。
  

## 使用方法

1. 在命令行中激活 Conda 环境：
  
  ```
  conda activate instruct_pix2pix
  ```
  
2. 运行程序：
  
  ```
  python edit_image.py
  ```
  
3. 在打开的 GUI 界面中：
  
  - 点击 "Select Image" 选择要编辑的图片。
  - 在 "Edit instruction" 输入框中输入编辑指令。
  - 调整参数（可选）：
    - Number of inference steps：推理步数，影响生成质量和时间。
    - Image guidance scale：控制结果与原图的相似度。
    - Guidance scale：控制结果对文本提示的遵循程度。
  - 点击 "Edit Image" 开始处理。
4. 处理完成后，编辑后的图像将显示在界面上，并保存为 "edited_image.jpg"。
  

## 参数说明

- **Number of inference steps**
  
  - 默认值：10
  - 范围：1-100
  - 说明：较高的值可能会提高质量，但会增加处理时间。
- **Image guidance scale**
  
  - 默认值：1.0
  - 范围：0.0-5.0
  - 说明：较高的值会使结果更接近原始输入图像。
- **Guidance scale**
  
  - 默认值：7.5
  - 范围：0.0-20.0
  - 说明：较高的值会使图像更严格地遵循文本提示。

## 常见问题

1. CUDA 错误：
  确保您的 NVIDIA 驱动程序是最新的，并且 PyTorch 的 CUDA 版本与您系统的 CUDA 版本匹配。
  
2. 内存不足：
  如果遇到内存错误，尝试减小图像尺寸或降低参数值。我是rtx4060，5G显存，可以处理512*512的图像，好像还能稍大一些。
  
3. 生成质量问题：
  尝试调整参数，特别是增加 inference steps（20往往比10的效果好一些） 和调整 guidance scales。
  

## 注意事项

- 第一次运行时，程序会下载 InstructPix2Pix 模型，这可能需要一些时间。
- 图像处理可能需要几秒到几分钟，取决于您的硬件和参数设置。
- 这个模型主要用于颜色调整、风格转换和简单的元素添加/删除。它不适合复杂的空间重排，如调换图片中物体的位置。

## 使用技巧

1. 使用清晰、具体的语言描述您想要的变化。
2. 对于复杂的编辑，考虑将任务分解为多个小步骤。
3. 实验不同的提示词和参数设置，找到最佳组合。
4. 对于特定区域的编辑，在提示中明确指出区域位置。
5. <mark>请使用英文提示词</mark>。

## 许可证

本项目采用GNU通用公共许可证第3版（GNU GPLv3）开源。详情请见[LICENSE](LICENSE)文件。

本项目基于MIT许可的InstructPix2Pix。原始InstructPix2Pix版权归Timothy Brooks, Aleksander Holynski, Alexei A. Efros所有。

注意：本项目使用了基于Stable Diffusion的InstructPix2Pix模型。使用时请遵守相关许可条款。
