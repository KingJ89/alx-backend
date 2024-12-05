import redis from 'redis';

// Create and configure the Redis client
const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});

// Define school data to be added
const schoolData = {
  Portland: 50,
  Seattle: 80,
  "New York": 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2,
};

// Add data to the hash set
for (const [city, value] of Object.entries(schoolData)) {
  client.hset("HolbertonSchools", city, value, redis.print);
}

// Retrieve and display all data from the hash set
client.hgetall("HolbertonSchools", (err, reply) => {
  if (err) {
    console.error(`Error fetching data: ${err.message}`);
    return;
  }
  console.log(reply);
});
