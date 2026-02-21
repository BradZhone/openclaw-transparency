module.exports = {
  apps: [
    {
      name: 'transparency-api',
      cwd: '/home/brad/.openclaw/skills/transparency',
      script: 'python3',
      args: '-m uvicorn api_server:app --host 0.0.0.0 --port 8000',
      interpreter: 'none',
      restart_delay: 5000,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M'
    },
    {
      name: 'transparency-web',
      cwd: '/home/brad/.openclaw/skills/transparency',
      script: 'python3',
      args: '-m http.server 8080',
      interpreter: 'none',
      restart_delay: 5000,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M'
    }
  ]
};
