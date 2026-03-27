const express = require('express')
const axios = require('axios')
const path = require('path')
const app = express()

app.use(express.json())
app.use(express.static('public'))  // carpeta donde va el HTML

let dashboardData = null  // guarda los últimos datos recibidos

app.post('/analizar', async (req, res) => {
  const { labels, values, prompt } = req.body
  console.log('Datos recibidos, consultando Qwen...')

  try {
    const qwenResp = await axios.post(
      'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
      {
        model: 'qwen-plus',
        messages: [{ role: 'user', content: prompt }]
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.QWEN_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    )

    const insight = qwenResp.data.choices[0].message.content

    dashboardData = { labels, values, insight }
    console.log('Insight generado, dashboard listo.')
    res.json({ ok: true })

  } catch (err) {
    console.error('Error con Qwen:', err.message)
    res.status(500).json({ error: err.message })
  }
})

app.get('/datos', (req, res) => {
  if (!dashboardData) return res.status(404).json({ error: 'Aún no hay datos' })
  res.json(dashboardData)
})

app.listen(8080, () => console.log('Servidor corriendo en :8080'))