#!/usr/bin/env yarn dev
import { createQueue } from 'kue';

// Create a queue for push notification jobs
const queue = createQueue({ name: 'push_notification_code' });

// Define the job data
const jobData = {
  phoneNumber: '07045679939',
  message: 'Account registered',
};

// Create a new job in the queue
const job = queue.create('push_notification_code', jobData);

// Add event listeners for the job
job
  .on('enqueue', () => {
    console.log(`Notification job created: ${job.id}`);
  })
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed attempt', (errorMessage) => {
    console.log(`Notification job failed: ${errorMessage}`);
  });

// Save the job to the queue
job.save((err) => {
  if (err) {
    console.error('Failed to save job:', err);
  }
});
