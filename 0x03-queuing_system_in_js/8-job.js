#!/usr/bin/env yarn dev
import { Queue, Job } from 'kue';

/**
 * Creates push notification jobs from the array of job info objects.
 * @param {Array<Object>} jobs - List of job data objects, each containing the necessary information for a notification.
 * @param {Queue} queue - The Kue queue instance to process the jobs.
 * @throws Will throw an error if `jobs` is not an array.
 */
export const createPushNotificationsJobs = (jobs, queue) => {
  // Validate that `jobs` is an array
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  // Iterate through each job info object and create a job
  jobs.forEach((jobInfo) => {
    const job = queue.create('push_notification_code_3', jobInfo);

    // Add event listeners to handle job lifecycle events
    job
      .on('enqueue', () => {
        console.log(`Notification job created: ${job.id}`);
      })
      .on('complete', () => {
        console.log(`Notification job ${job.id} completed`);
      })
      .on('failed', (err) => {
        console.error(`Notification job ${job.id} failed: ${err.message || err.toString()}`);
      })
      .on('progress', (progress) => {
        console.log(`Notification job ${job.id} is ${progress}% complete`);
      });

    // Save the job to the queue
    job.save((err) => {
      if (err) {
        console.error(`Failed to save job ${job.id}: ${err.message || err.toString()}`);
      }
    });
  });
};

export default createPushNotificationsJobs;
