import api from './index'
import axios from '../config/axios'

export const aiApi = {
    // 开始面试
    startInterview: (data: any) => {
        return api.post('/interview/start', data)
    },

    // 发送面试答案
    sendAnswer: (data: any) => {
        return api.post('/interview/answer', data)
    },

    // 获取面试分析
    getAnalysis: (interviewId: string) => {
        return api.get(`/interview/analysis/${interviewId}`)
    },

    // 获取实时反馈
    getFeedback: (data: any) => {
        return api.post('/interview/feedback', data)
    }
}

interface FaceVerifyResponse {
    success: boolean;
    result?: {
        score: number;
        matched: boolean;
    };
    error?: string;
}

// 人脸验证API
export const verifyFace = async (imageData: string): Promise<FaceVerifyResponse> => {
    try {
        const response = await axios.post<FaceVerifyResponse>('/api/proxy/xf-yun/face/verify', {
            image: imageData
        });
        return response.data;
    } catch (error) {
        console.error('人脸验证请求失败:', error);
        throw new Error('人脸验证失败，请重试');
    }
};

interface FaceLocation {
    x: number;
    y: number;
    width: number;
    height: number;
}

interface FaceProperties {
    expression: string;
    gender: string;
    glass: string;
    hair: string;
    beard: string;
    mask: string;
}

interface Face {
    score: number;
    location: FaceLocation;
    properties: FaceProperties;
}

interface FaceDetectionResponse {
    success: boolean;
    face_count: number;
    faces: Face[];
    error?: string;
}

// 人脸检测API
export const detectFace = async (imageData: string): Promise<FaceDetectionResponse> => {
    try {
        // 从Data URL中提取base64数据
        const base64Data = imageData.split(',')[1];
        console.log('发送人脸检测请求，数据长度:', base64Data.length);

        const response = await axios.post<FaceDetectionResponse>('/api/vision/face/detect', {
            image_base64: base64Data  // 只发送base64部分，不包含Data URL前缀
        });

        // 确保返回数据符合类型定义
        const data = response.data;
        return {
            success: data.success ?? false,
            face_count: data.face_count ?? 0,
            faces: data.faces?.map(face => ({
                score: face.score ?? 0,
                location: {
                    x: face.location?.x ?? 0,
                    y: face.location?.y ?? 0,
                    width: face.location?.width ?? 0,
                    height: face.location?.height ?? 0
                },
                properties: {
                    expression: face.properties?.expression ?? 'unknown',
                    gender: face.properties?.gender ?? 'unknown',
                    glass: face.properties?.glass ?? 'none',
                    hair: face.properties?.hair ?? 'unknown',
                    beard: face.properties?.beard ?? 'none',
                    mask: face.properties?.mask ?? 'none'
                }
            })) ?? [],
            error: data.error
        };
    } catch (error: any) {
        console.error('人脸检测失败:', error);
        const errorMessage = error.response?.data?.error || error.message || '人脸检测失败，请重试';
        return {
            success: false,
            face_count: 0,
            faces: [],
            error: errorMessage
        };
    }
}; 