"""
HTML邮件模板引擎
"""
import html
import json
from pathlib import Path
from typing import Dict, List, Optional


class TemplateEngine:
    """HTML模板引擎"""
    
    def __init__(self):
        self.template_dir = Path(__file__).parent
        self.meta_file = self.template_dir / 'template_meta.json'
        self._cache = {}
        self._meta = self._load_meta()
    
    def _load_meta(self) -> Dict:
        """加载模板元数据"""
        try:
            with open(self.meta_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def list_templates(self) -> List[Dict]:
        """
        列出所有可用模板
        
        Returns:
            模板信息列表
        """
        templates = []
        for name, meta in self._meta.items():
            template_file = self.template_dir / f"{name}.html"
            if template_file.exists():
                templates.append({
                    'name': name,
                    'display_name': meta.get('display_name', name),
                    'description': meta.get('description', ''),
                    'required_vars': meta.get('required_vars', []),
                    'optional_vars': meta.get('optional_vars', []),
                })
        return templates
    
    def load_template(self, template_name: str) -> str:
        """
        加载模板内容（带缓存）
        
        Args:
            template_name: 模板名称（不含.html）
            
        Returns:
            HTML模板字符串
        """
        if template_name in self._cache:
            return self._cache[template_name]
        
        template_file = self.template_dir / f"{template_name}.html"
        if not template_file.exists():
            raise FileNotFoundError(f"模板文件不存在: {template_name}")
        
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._cache[template_name] = content
        return content
    
    def render(self, template_name: str, variables: Dict[str, str]) -> str:
        """
        渲染模板
        
        Args:
            template_name: 模板名称
            variables: 变量字典
            
        Returns:
            渲染后的HTML字符串
        """
        html_template = self.load_template(template_name)
        
        # 安全替换变量（HTML转义防止XSS）
        for key, value in variables.items():
            safe_value = html.escape(str(value)) if value else ''
            html_template = html_template.replace(f'{{{key}}}', safe_value)
        
        # 将未替换的变量替换为空或默认值
        import re
        html_template = re.sub(r'\{[^}]+\}', '', html_template)
        
        return html_template
    
    def validate_variables(self, template_name: str, variables: Dict) -> tuple:
        """
        验证变量是否完整
        
        Returns:
            (is_valid, missing_vars)
        """
        meta = self._meta.get(template_name, {})
        required = meta.get('required_vars', [])
        
        missing = [var for var in required if not variables.get(var)]
        
        return len(missing) == 0, missing
    
    def clear_cache(self):
        """清除缓存"""
        self._cache.clear()
