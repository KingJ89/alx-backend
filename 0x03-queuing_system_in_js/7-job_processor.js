#!/usr/bin/env yarn dev
import { createQueue } from 'kue';

const BLACKLISTED_NUMBERS = ['4153518780', '4153518781'];
const queue = createQueue();

/**
 * Sends a push notification to a user.
 * @param {string} phoneNumber - The recipient's phone number.
 * @param {string} message - The message to send.
 * @param {Object} job - The job instance.
 * @param {Function} done - Callback to signal job completion or failure.
 */
const sendNotification = (phoneNumber, message, job, done) => {
  const total = 2;
  let pending = total;

  const sendInterval = setInterval(() => {
    const progress = total - pending;

    // Update job progress
    if (progress <= total / 2) {
      job.progress(progress, total);
    }

    // Check for blacklisted numbers
    if (BLACKLISTED_NUMBERS.includes(phoneNumber)) {
      clearInterval(sendInterval);
      done(new Error(`Phone number ${phoneNumber} is blacklisted`));
      return;
    }

    // Log notification send attempt
    if (progress === 0) {
      console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    }

    // Decrement pending and finish the job if all steps are complete
    pending -= 1;
    if (pending === 0) {
      clearInterval(sendInterval);
      done();
    }
  }, 1000);
};

// Process jobs in the 'push_notification_code_2' queue, with concurrency set to 2
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});
