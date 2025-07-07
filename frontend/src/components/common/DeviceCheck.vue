<template>
  <div class="device-check-dialog" v-if="modelValue">
    <div class="dialog-content">
      <h3>设备检测</h3>
      <div class="device-status">
        <div class="device-item">
          <i :class="cameraStatus ? 'fas fa-check-circle success' : 'fas fa-times-circle error'"></i>
          摄像头: {{ cameraStatus ? '已就绪' : '未就绪' }}
        </div>
        <div class="device-item">
          <i :class="microphoneStatus ? 'fas fa-check-circle success' : 'fas fa-times-circle error'"></i>
          麦克风: {{ microphoneStatus ? '已就绪' : '未就绪' }}
        </div>
        <div class="device-item">
          <i :class="networkStatus ? 'fas fa-check-circle success' : 'fas fa-times-circle error'"></i>
          网络连接: {{ networkStatus ? '已连接' : '未连接' }}
        </div>
      </div>
      <div class="dialog-buttons">
        <button @click="retryCheck" class="retry-btn">重试</button>
        <button @click="closeDialog" class="confirm-btn" :disabled="!allDevicesReady">确定</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';

export default defineComponent({
  name: 'DeviceCheck',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  emits: ['update:modelValue', 'device-status'],
  setup(props, { emit }) {
    const cameraStatus = ref(false);
    const microphoneStatus = ref(false);
    const networkStatus = ref(true);

    const allDevicesReady = computed(() => {
      return cameraStatus.value && microphoneStatus.value && networkStatus.value;
    });

    function checkDevices() {
      return new Promise((resolve) => {
        networkStatus.value = navigator.onLine;
        
        navigator.mediaDevices.enumerateDevices()
          .then(devices => {
            const hasCamera = devices.some(device => device.kind === 'videoinput');
            const hasMicrophone = devices.some(device => device.kind === 'audioinput');

            if (hasCamera && hasMicrophone) {
              return navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            }
            return Promise.reject('No devices found');
          })
          .then(stream => {
            cameraStatus.value = true;
            microphoneStatus.value = true;
            stream.getTracks().forEach(track => track.stop());
            emit('device-status', true);
            resolve(true);
          })
          .catch(error => {
            console.error('设备检测失败:', error);
            emit('device-status', false);
            resolve(false);
          });
      });
    }

    function retryCheck() {
      checkDevices();
    }

    function closeDialog() {
      if (allDevicesReady.value) {
        emit('update:modelValue', false);
      }
    }

    window.addEventListener('online', () => networkStatus.value = true);
    window.addEventListener('offline', () => networkStatus.value = false);

    onMounted(() => {
      checkDevices();
    });

    return {
      cameraStatus,
      microphoneStatus,
      networkStatus,
      allDevicesReady,
      retryCheck,
      closeDialog
    };
  }
});
</script>

<style scoped>
.device-check-dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-content {
  background: var(--bg-color, #fff);
  border-radius: 8px;
  padding: 20px;
  width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.device-status {
  margin: 20px 0;
}

.device-item {
  display: flex;
  align-items: center;
  margin: 10px 0;
  font-size: 16px;
}

.device-item i {
  margin-right: 10px;
  font-size: 20px;
}

.success {
  color: #4CAF50;
}

.error {
  color: #f44336;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.retry-btn, .confirm-btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-size: 14px;
}

.retry-btn {
  background: #f5f5f5;
  color: #333;
}

.confirm-btn {
  background: #4CAF50;
  color: white;
}

.confirm-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style> 