import axios from 'axios';
import http from '../config/axios';

interface UserInfo {
    id: string;
    name: string;
    idPhoto: string;  // Base64格式的证件照
}

class UserService {
    private static instance: UserService;
    private currentUser: UserInfo | null = null;
    private baseUrl = '/api/user';

    private constructor() { }

    public static getInstance(): UserService {
        if (!UserService.instance) {
            UserService.instance = new UserService();
        }
        return UserService.instance;
    }

    // 获取当前用户信息
    public async getCurrentUser(): Promise<UserInfo> {
        if (this.currentUser) {
            return this.currentUser;
        }

        try {
            // 这里应该调用后端API获取用户信息
            const response = await fetch('http://localhost:5000/api/user/current', {
                credentials: 'include'  // 包含cookies
            });

            if (!response.ok) {
                throw new Error('Failed to fetch user info');
            }

            this.currentUser = await response.json();
            return this.currentUser;
        } catch (error) {
            console.error('获取用户信息失败:', error);
            throw error;
        }
    }

    // 获取用户证件照
    public async getIdPhoto(): Promise<string> {
        try {
            const user = await this.getCurrentUser();
            return user.idPhoto;
        } catch (error) {
            console.error('获取证件照失败:', error);
            throw error;
        }
    }

    // 更新用户信息
    public async updateUser(userInfo: Partial<UserInfo>): Promise<UserInfo> {
        try {
            const response = await fetch('http://localhost:5000/api/user/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify(userInfo)
            });

            if (!response.ok) {
                throw new Error('Failed to update user info');
            }

            this.currentUser = await response.json();
            return this.currentUser;
        } catch (error) {
            console.error('更新用户信息失败:', error);
            throw error;
        }
    }

    async uploadIdPhoto(file: File): Promise<string> {
        try {
            // 检查文件类型
            if (!file.type.match(/^image\/(jpeg|jpg|png)$/)) {
                throw new Error('只支持 JPG 和 PNG 格式的图片');
            }

            // 检查文件大小（限制为5MB）
            if (file.size > 5 * 1024 * 1024) {
                throw new Error('图片大小不能超过5MB');
            }

            // 将文件转换为Base64
            const base64Data = await this.fileToBase64(file);

            // 发送到临时存储接口
            const response = await http.post(`${this.baseUrl}/upload-id-photo`, {
                photo: base64Data
            });

            if (response.data.success) {
                return base64Data; // 返回Base64数据供前端显示
            } else {
                throw new Error(response.data.error || '上传失败');
            }
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (error.response?.status === 413) {
                    throw new Error('图片文件太大');
                } else {
                    throw new Error(error.response?.data?.error || '网络错误，请重试');
                }
            }
            throw error;
        }
    }

    private fileToBase64(file: File): Promise<string> {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                const base64String = reader.result as string;
                // 移除 Data URL 的前缀（例如："data:image/jpeg;base64,"）
                const base64Data = base64String.split(',')[1];
                resolve(base64Data);
            };
            reader.onerror = (error) => reject(error);
        });
    }
}

export const userService = UserService.getInstance();
export type { UserInfo }; 