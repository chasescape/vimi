import re
from typing import Optional, Dict, Any

def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_username(username: str) -> bool:
    """验证用户名格式"""
    # 用户名长度在3-20之间，只能包含字母、数字、下划线
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return bool(re.match(pattern, username))

def validate_password(password: str) -> bool:
    """验证密码强度"""
    # 密码长度至少6位
    return len(password) >= 6

def validate_text(text: str) -> bool:
    """验证文本内容是否有效
    
    Args:
        text: 要验证的文本内容
        
    Returns:
        bool: 如果文本有效返回True，否则返回False
    """
    if not text or not isinstance(text, str):
        return False
        
    # 去除空白字符后检查长度
    text = text.strip()
    if len(text) == 0:
        return False
        
    # 文本长度限制（例如：不超过5000字）
    if len(text) > 5000:
        return False
        
    # 检查是否包含基本的可打印字符
    if not any(char.isprintable() for char in text):
        return False
        
    return True

def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """验证文件扩展名"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def validate_file_size(file_size: int, max_size_mb: int = 10) -> bool:
    """验证文件大小"""
    max_size_bytes = max_size_mb * 1024 * 1024  # 转换为字节
    return file_size <= max_size_bytes

def validate_date_format(date_str: str) -> bool:
    """验证日期格式 (YYYY-MM-DD)"""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, date_str))

def validate_phone_number(phone: str) -> bool:
    """验证手机号格式"""
    pattern = r'^1[3-9]\d{9}$'  # 中国大陆手机号格式
    return bool(re.match(pattern, phone))

def validate_id_number(id_number: str) -> bool:
    """验证身份证号格式"""
    pattern = r'^\d{17}[\dXx]$'  # 18位身份证号
    return bool(re.match(pattern, id_number))

def validate_url(url: str) -> bool:
    """验证URL格式"""
    pattern = r'^https?:\/\/([\w\d\-]+\.)+\w{2,}(\/[\w\d\-\._\?\,\'\/\\\+&amp;%\$#\=~]*)?$'
    return bool(re.match(pattern, url))

def validate_image_file(filename: str) -> bool:
    """验证图片文件格式"""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return validate_file_extension(filename, allowed_extensions)

def validate_audio_file(filename: str) -> bool:
    """验证音频文件格式"""
    allowed_extensions = {'mp3', 'wav', 'ogg', 'm4a'}
    return validate_file_extension(filename, allowed_extensions)

def validate_video_file(filename: str) -> bool:
    """验证视频文件格式"""
    allowed_extensions = {'mp4', 'avi', 'mov', 'wmv'}
    return validate_file_extension(filename, allowed_extensions)

def validate_document_file(filename: str) -> bool:
    """验证文档文件格式"""
    allowed_extensions = {'pdf', 'doc', 'docx', 'txt', 'rtf'}
    return validate_file_extension(filename, allowed_extensions)
