const net = require('net');
const WebSocket = require('ws');

const tcpServer = net.createServer(socket => {
  socket.on('data', data => {
    try {
      const parsed = JSON.parse(data.toString());
      const wrapped = JSON.stringify({ alarm: parsed });
      clients.forEach(ws => ws.send(wrapped));
    } catch (err) {
      console.error('Failed to parse TCP data:', err);
    }
  });
});

tcpServer.listen(6000, () => console.log('TCP listening on 6000'));

const wss = new WebSocket.Server({ port: 8000 });

let clients = [];

wss.on('connection', ws => {
  console.log('WebSocket client connected');
  clients.push(ws);

  ws.on('close', () => {
    clients = clients.filter(c => c !== ws);
  });
});