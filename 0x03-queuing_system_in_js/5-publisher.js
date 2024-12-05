import redis from 'redis';

// Create and configure the Redis client
const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});

// Subscribe to the channel
const channelName = 'holberton school channel';
client.subscribe(channelName);

// Handle messages from the channel
client.on('message', (channel, message) => {
  console.log(`Message received on channel ${channel}: ${message}`);
  
  if (message === 'KILL_SERVER') {
    console.log('KILL_SERVER command received. Unsubscribing and shutting down the client.');
    client.unsubscribe();
    client.quit();
  }
});
