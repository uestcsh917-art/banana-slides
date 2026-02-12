"""
Lazyllm framework implementation for image editing and generation

Support models:
- qwen-image-edit
- qwen-image-edit-plus
- qwen-image-edit-plus-2025-10-30
- ...

- doubao-seedream-4-0-250828
- doubao-seededit-3-0-i2i-250628
- doubao-seedream-4.5
- ...
"""
import tempfile
import os
import logging
from typing import Optional, List
from PIL import Image
from .base import ImageProvider
from ..lazyllm_env import ensure_lazyllm_namespace_key

logger = logging.getLogger(__name__)

class LazyLLMImageProvider(ImageProvider):
    """Image generation using Lazyllm framework"""
    def __init__(self, source: str = 'doubao', model: str = 'doubao-seedream-4-0-250828'):
        """
        Initialize GenAI image provider

        Args:
            source: image_editing model provider, support qwen,doubao,siliconflow now.
            model: Model name to use
            type: Category of the online service. Defaults to ``llm``.
        """
        try:
            import lazyllm
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "lazyllm is required when AI_PROVIDER_FORMAT=lazyllm. "
                "Please install backend dependencies including lazyllm."
            ) from exc

        ensure_lazyllm_namespace_key(source, namespace='BANANA')
        self.client = lazyllm.namespace('BANANA').OnlineModule(
            source=source,
            model=model,
            type='image_editing',
        )

    def generate_image(self, prompt: str = None, 
                       ref_images: Optional[List[Image.Image]] = None, 
                       aspect_ratio = "16:9", 
                       resolution = "1920*1080",
                       enable_thinking: bool = False,
                       thinking_budget: int = 0
                       ) -> Optional[Image.Image]:
        resolution_map = {
            "1K": "1920*1080",
            "2K": "2048*1080",
            "4K": "3840*2160"
        }
        if resolution in resolution_map:
            resolution = resolution_map[resolution]
        # Convert a PIL Image object to a file path: When passing a reference image to lazyllm, you need to input a path in string format.
        file_paths = None
        temp_paths = []
        decode_query_with_filepaths = None
        try:
            from lazyllm.components.formatter import decode_query_with_filepaths as _decoder
            decode_query_with_filepaths = _decoder
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "lazyllm is required when AI_PROVIDER_FORMAT=lazyllm. "
                "Please install backend dependencies including lazyllm."
            ) from exc
        if ref_images:
            file_paths = []
            for img in ref_images:
                with tempfile.NamedTemporaryFile(prefix='lazyllm_ref_', suffix='.png', delete=False) as tmp:
                    temp_path = tmp.name
                img.save(temp_path)
                file_paths.append(temp_path)
                temp_paths.append(temp_path)
        try:
            response_path = self.client(prompt, lazyllm_files=file_paths, size=resolution)
            image_path = decode_query_with_filepaths(response_path) # dict
            if not image_path:
                logger.warning('No images found in response')
                raise ValueError()
            if isinstance(image_path, dict):
                files = image_path.get('files')
                if files and isinstance(files, list) and len(files) > 0:
                    image_path = files[0]
                else:
                    logger.warning('No valid image path in response')
                    return None
            try:
                with Image.open(image_path) as image:
                    result = image.copy()
                logger.info(f'Successfully loaded image from: {image_path}')
                return result
            except Exception as e:
                logger.error(f'Failed to load image: {e}')
            logger.warning('No valid images could be loaded')
            return None
        finally:
            for temp_path in temp_paths:
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
