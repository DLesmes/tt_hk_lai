import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path
from app.settings import settings

class PromptManager:
    """Manages YAML-based prompt configurations with version control"""
    
    def __init__(self, config_dir: str = "app/config"):
        self.config_dir = Path(config_dir)
        self._prompts_cache = {}
    
    def load_prompt(self, prompt_file: str, version: str = "v1") -> Dict[str, Any]:
        """Load prompt configuration from YAML file"""
        cache_key = f"{prompt_file}_{version}"
        
        if cache_key in self._prompts_cache:
            return self._prompts_cache[cache_key]
        
        prompt_path = self.config_dir / prompt_file
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        if version not in config.get('versions', {}):
            raise ValueError(f"Version {version} not found in {prompt_file}")
        
        self._prompts_cache[cache_key] = config['versions'][version]
        return config['versions'][version]
    
    def substitute_parameters(self, prompt_config: Dict[str, Any], **kwargs) -> str:
        """Substitute parameters in the docs section"""
        docs_template = prompt_config.get('docs', '')
        try:
            return docs_template.format(**kwargs)
        except KeyError as e:
            # If a parameter is missing, replace with empty string
            missing_param = str(e).strip("'")
            return docs_template.replace(f"{{{missing_param}}}", "")
    
    def get_prompt_for_role(self, role: str, version: str = "v1", **kwargs) -> Dict[str, Any]:
        """Get prompt configuration for specific role"""
        prompt_file = f"{role}_agent.yml"
        prompt_config = self.load_prompt(prompt_file, version)
        
        # Create a copy to avoid modifying cached version
        prompt_config = prompt_config.copy()
        
        # Substitute parameters in docs
        if kwargs:
            prompt_config['docs'] = self.substitute_parameters(prompt_config, **kwargs)
        
        return prompt_config
    
    def clear_cache(self):
        """Clear the prompt cache"""
        self._prompts_cache.clear()
    
    def list_available_prompts(self) -> list:
        """List all available prompt files"""
        prompt_files = []
        for file_path in self.config_dir.glob("*_agent.yml"):
            prompt_files.append(file_path.name)
        return prompt_files

# Global prompt manager instance
prompt_manager = PromptManager() 