#!/usr/bin/env yarn dev
import { createQueue } from 'kue';

// Create a queue instance
const queue = createQueue();

/**
 * Function to send a notification.
 * @param {string} phoneNumber - The recipient's phone number.
 * @param {string} message - The notification message.
 */
const sendNotification = (phoneNumber, message) => {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
};

// Process jobs in the 'push_notification_code' queue
queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;

  // Send the notification
  sendNotification(phoneNumber, message);

  // Signal that the job is complete
  done();
});
