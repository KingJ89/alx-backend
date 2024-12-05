#!/usr/bin/yarn dev
import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

const app = express();
const client = createClient({ name: 'reserve_seat' });
const queue = createQueue();
const INITIAL_SEATS_COUNT = 50;
let reservationEnabled = false;
const PORT = 1245;

/**
 * Modifies the number of available seats.
 * @param {number} number - The new number of seats.
 */
const reserveSeat = async (number) => {
  await promisify(client.SET).bind(client)('available_seats', number);
};

/**
 * Retrieves the number of available seats.
 * @returns {Promise<number>}
 */
const getCurrentAvailableSeats = async () => {
  const seats = await promisify(client.GET).bind(client)('available_seats');
  return Number.parseInt(seats || 0);
};

app.get('/available_seats', async (_, res) => {
  try {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats });
  } catch (error) {
    res.status(500).json({ status: 'Error retrieving available seats', error: error.message });
  }
});

app.get('/reserve_seat', async (_req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservations are blocked' });
  }

  try {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats <= 0) {
      return res.json({ status: 'No available seats to reserve' });
    }

    const job = queue.create('reserve_seat');
    
    job.on('failed', (err) => {
      console.error('Seat reservation job', job.id, 'failed:', err.message || err.toString());
    });
    job.on('complete', () => {
      console.log('Seat reservation job', job.id, 'completed');
    });
    job.save();

    res.json({ status: 'Reservation in process' });
  } catch (error) {
    res.status(500).json({ status: 'Reservation failed', error: error.message });
  }
});

app.get('/process', (_req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (_job, done) => {
    try {
      const availableSeats = await getCurrentAvailableSeats();
      reservationEnabled = availableSeats <= 1 ? false : reservationEnabled;

      if (availableSeats >= 1) {
        await reserveSeat(availableSeats - 1);
        done();
      } else {
        done(new Error('Not enough seats available'));
      }
    } catch (error) {
      done(error);
    }
  });
});

const resetAvailableSeats = async (initialSeatsCount) => {
  try {
    await promisify(client.SET).bind(client)('available_seats', Number.parseInt(initialSeatsCount));
  } catch (error) {
    console.error('Error resetting available seats:', error.message);
  }
};

app.listen(PORT, async () => {
  try {
    await resetAvailableSeats(process.env.INITIAL_SEATS_COUNT || INITIAL_SEATS_COUNT);
    reservationEnabled = true;
    console.log(`API available on localhost port ${PORT}`);
  } catch (error) {
    console.error('Error initializing the server:', error.message);
  }
});

export default app;
