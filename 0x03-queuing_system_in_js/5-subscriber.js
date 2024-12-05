import redis from 'redis';

const client = redis.createClient();

// Event listeners for Redis connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});

// Subscribe to the Redis channel
const channelName = 'holberton school channel';
client.subscribe(channelName);

// Handle messages received on the channel
client.on('message', (channel, message) => {
  console.log(message);
  if (message === 'KILL_SERVER') {
    client.unsubscribe();
    client.quit();
  }
});

/**
 * Publishes a message to the Redis channel after a specified delay.
 * @param {string} message - The message to publish.
 * @param {number} delay - Delay in milliseconds before publishing the message.
 */
function publishMessage(message, delay) {
  setTimeout(() => {
    console.log(`About to send: ${message}`);
    client.publish(channelName, message);
  }, delay);
}

// Schedule messages to be published
publishMessage('Holberton Student #1 starts course', 100);
publishMessage('Holberton Student #2 starts course', 200);
publishMessage('KILL_SERVER', 300);
publishMessage('Holberton Student #3 starts course', 400);

