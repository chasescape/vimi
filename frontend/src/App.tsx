import React, { useEffect, useRef, useState } from 'react'
import { Button, Input, message, Spin } from 'antd'
import AvatarPlatform, {
  PlayerEvents,
  SDKEvents,
} from './testSdk/3.1.2.1002/avatar-sdk-web_3.1.2.1002/index.js'

const SDK_CONFIG = {
  serverUrl: 'wss://avatar.cn-huadong-1.xf-yun.com/v1/interact',
  appId: 'e5850021',
  apiKey: 'dda0f69489a3db1e0d495f40a5fd40eb',
  apiSecret: 'OTNlMGI0OWUxM2JlMWRhM2EzNDVhZjAw',
  sceneId: '202632480413585408',
}

const GLOBAL_PARAMS = {
  avatar_dispatch: { interactive_mode: 0, content_analysis: 0 },
  stream: {
    protocol: 'xrtc',
    alpha: 0,
    bitrate: 1000000,
    fps: 25,
  },
  avatar: {
    avatar_id: '110021006',
    width: 1920,
    height: 1080,
    mask_region: [0, 0, 1080, 1920],
    scale: 1,
    move_h: 0,
    move_v: 0,
    audio_format: 1,
  },
  tts: {
    vcn: 'x4_lingxiaoqi_oral',
    speed: 50,
    pitch: 50,
    volume: 100,
  },
  subtitle: {
    subtitle: 1,
    font_color: '#ffffff',
  },
  background: {
    enabled: false,
    type: 'url',
    data: '',
  },
}

function App() {
  const interactiveRef = useRef<any>(null)  // 初始化为 null
  const [loading, setLoading] = useState(false)
  const [subtitle, setSubtitle] = useState('')
  const [text, setText] = useState('')

  // 初始化 SDK 并绑定事件，一次完成
  const initAndBindSDK = () => {
    if (interactiveRef.current) {
      message.warning('SDK 已初始化')
      return
    }
    try {
      interactiveRef.current = new (AvatarPlatform as any)({
        useInlinePlayer: true,
        binaryData: false,
      })

      // 绑定SDK事件
      interactiveRef.current.removeAllListeners()
      interactiveRef.current
        .on(SDKEvents.connected, (res: any) => {
          console.log('SDK connected', res)
        })
        .on(SDKEvents.stream_start, () => {
          console.log('SDK stream_start')
        })
        .on(SDKEvents.disconnected, (e: any) => {
          setLoading(false)
          message.error('连接断开')
          console.error(e)
        })
        .on(SDKEvents.subtitle_info, (data: any) => {
          setSubtitle(data?.text || '')
        })
        .on(SDKEvents.error, (err: any) => {
          console.error('SDK error', err)
        })

      // 绑定播放器事件
      const player = interactiveRef.current.player
      if (player) {
        player.removeAllListeners()
        player
          .on(PlayerEvents.error, (e: any) => {
            console.error('Player error', e)
          })
          .on(PlayerEvents.play, () => {
            console.log('Player play')
          })
          .on(PlayerEvents.playing, () => {
            console.log('Player playing')
          })
      }

      setApiInfo()
      setGlobalParams()
      message.success('SDK 初始化成功')
    } catch (e: any) {
      message.error('初始化失败: ' + e.message)
    }
  }

  const setApiInfo = () => {
    if (!interactiveRef.current) {
      message.warning('请先初始化SDK')
      return
    }
    interactiveRef.current.setApiInfo({
      serverUrl: SDK_CONFIG.serverUrl,
      appId: SDK_CONFIG.appId,
      apiKey: SDK_CONFIG.apiKey,
      apiSecret: SDK_CONFIG.apiSecret,
      sceneId: SDK_CONFIG.sceneId,
    })
  }

  const setGlobalParams = () => {
    if (!interactiveRef.current) {
      message.warning('请先初始化SDK')
      return
    }
    interactiveRef.current.setGlobalParams(GLOBAL_PARAMS)
  }

  // 启动虚拟人和开始录音
  const startInterview = async () => {
    if (!interactiveRef.current) {
      initAndBindSDK()
    }
    setLoading(true)
    try {
      await interactiveRef.current.start({
        wrapper: document.querySelector('.wrapper1') as HTMLElement, // 类型断言
      })
      message.success('虚拟人启动成功，开始全双工录音')
      startRecord()
    } catch (e: any) {
      message.error('启动失败: ' + e.message)
    }
    setLoading(false)
  }

  // 开始录音
  const startRecord = () => {
    if (!interactiveRef.current) {
      message.warning('请先启动SDK')
      return
    }
    if (interactiveRef.current.recorder) {
      interactiveRef.current.recorder.stopRecord()
      interactiveRef.current.destroyRecorder()
    }
    interactiveRef.current.createRecorder({
      sampleRate: 16000,
    })
    interactiveRef.current.recorder.startRecord(
      0,
      () => {
        console.log('录音自动停止')
      },
      {
        nlp: true,
      }
    )
  }

  // 停止录音
  const stopRecord = () => {
    if (!interactiveRef.current || !interactiveRef.current.recorder) {
      message.warning('录音尚未开始')
      return
    }
    interactiveRef.current.recorder.stopRecord()
    message.info('录音停止')
  }

  // 发送文本交互
  const sendText = () => {
    if (!interactiveRef.current) {
      message.warning('请先启动SDK')
      return
    }
    if (!text.trim()) {
      message.warning('请输入文本')
      return
    }
    interactiveRef.current
      .writeText(text, {
        nlp: true,
        avatar_dispatch: {
          interactive_mode: 0,
          content_analysis: 0,
        },
        tts: {
          vcn: 'x4_lingxiaoqi_oral',
          speed: 50,
          pitch: 50,
          volume: 100,
        },
      })
      .then((reqId: string) => {
        message.success(`文本发送成功，requestId: ${reqId}`)
      })
      .catch((err: any) => {
        message.error('文本发送失败')
        console.error(err)
      })
  }

  // 发送打断命令
  const interruptSpeak = () => {
    if (!interactiveRef.current) {
      message.warning('请先启动SDK')
      return
    }
    interactiveRef.current.interrupt()
    message.info('已发送打断命令')
  }

  // 停止SDK连接
  const stopSDK = () => {
    if (!interactiveRef.current) {
      message.warning('SDK尚未初始化')
      return
    }
    interactiveRef.current.stop()
    interactiveRef.current.destroy()
    interactiveRef.current = null
    message.success('SDK已停止并销毁')
  }

  // 组件卸载时清理
  useEffect(() => {
    return () => {
      if (interactiveRef.current) {
        interactiveRef.current.stop()
        interactiveRef.current.destroy()
        interactiveRef.current = null
      }
    }
  }, [])

  return (
    <Spin spinning={loading} tip="加载中...">
      <div style={{ padding: 20 }}>
        <div
          className="wrapper1"
          style={{
            width: 480,
            height: 720,
            border: '1px solid #ccc',
            marginBottom: 10,
          }}
        ></div>

        <p>虚拟人字幕：{subtitle}</p>

        <Input.TextArea
          rows={4}
          placeholder="请输入与虚拟人交互的文本"
          value={text}
          onChange={(e) => setText(e.target.value)}
          style={{ marginBottom: 10 }}
        />

        <div>
          <Button type="primary" onClick={startInterview} style={{ marginRight: 8 }}>
            开始面试
          </Button>
          <Button type="primary" onClick={sendText} style={{ marginRight: 8 }}>
            发送文本交互
          </Button>
          <Button onClick={interruptSpeak} style={{ marginRight: 8 }}>
            打断播报
          </Button>
          <Button onClick={stopRecord} style={{ marginRight: 8 }}>
            停止录音
          </Button>
          <Button onClick={stopSDK} danger>
            停止SDK连接
          </Button>
        </div>
      </div>
    </Spin>
  )
}

export default App
