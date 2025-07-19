const handleRegister = async () => {
  try {
    console.log('注册数据:', registerForm.value)
    const response = await request.post('/api/auth/register', {
      username: registerForm.value.username,
      email: registerForm.value.email,
      password: registerForm.value.password,
      role: registerForm.value.role
    })
    
    if (response.data.success) {
      ElMessage.success('注册成功！')
      router.push('/auth/login')
    } else {
      ElMessage.error(response.data.message || '注册失败')
    }
  } catch (error) {
    console.error('注册错误:', error)
    if (error.response) {
      console.error('错误响应:', error.response.data)
      ElMessage.error(error.response.data.message || '注册失败')
    } else {
      ElMessage.error('网络错误，请稍后重试')
    }
  }
} 