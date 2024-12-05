#!/usr/bin/env yarn test
import sinon from 'sinon';
import { expect } from 'chai';
import { createQueue } from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  const BIG_BROTHER = sinon.spy(console);
  const QUEUE = createQueue({ name: 'push_notification_code_test' });

  before(() => {
    QUEUE.testMode.enter(true);
  });

  after(() => {
    QUEUE.testMode.clear();
    QUEUE.testMode.exit();
  });

  afterEach(() => {
    BIG_BROTHER.log.resetHistory();
  });

  it('throws an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, QUEUE)).to.throw('Jobs is not an array');
  });

  it('adds jobs to the queue with the correct type and logs job creation', (done) => {
    const jobInfos = [
      {
        phoneNumber: '44556677889',
        message: 'Use the code 1982 to verify your account',
      },
      {
        phoneNumber: '98877665544',
        message: 'Use the code 1738 to verify your account',
      },
    ];

    // Create jobs
    createPushNotificationsJobs(jobInfos, QUEUE);

    // Ensure jobs are added to the queue
    expect(QUEUE.testMode.jobs.length).to.equal(2);
    expect(QUEUE.testMode.jobs[0].data).to.deep.equal(jobInfos[0]);
    expect(QUEUE.testMode.jobs[0].type).to.equal('push_notification_code_3');

    // Process job and check log output
    QUEUE.process('push_notification_code_3', () => {
      expect(
        BIG_BROTHER.log.calledWith('Notification job created:', QUEUE.testMode.jobs[0].id)
      ).to.be.true;
      done();
    });
  });

  it('registers the progress event handler for a job', (done) => {
    // Register the progress listener
    QUEUE.testMode.jobs[0].addListener('progress', (progress) => {
      expect(
        BIG_BROTHER.log.calledWith('Notification job', QUEUE.testMode.jobs[0].id, `${progress}% complete`)
      ).to.be.true;
      done();
    });

    // Emit progress event
    QUEUE.testMode.jobs[0].emit('progress', 25);
  });

  it('registers the failed event handler for a job', (done) => {
    // Register the failed listener
    QUEUE.testMode.jobs[0].addListener('failed', (err) => {
      expect(
        BIG_BROTHER.log.calledWith('Notification job', QUEUE.testMode.jobs[0].id, 'failed:', err.message)
      ).to.be.true;
      done();
    });

    // Emit failed event
    QUEUE.testMode.jobs[0].emit('failed', new Error('Failed to send'));
  });

  it('registers the complete event handler for a job', (done) => {
    // Register the complete listener
    QUEUE.testMode.jobs[0].addListener('complete', () => {
      expect(
        BIG_BROTHER.log.calledWith('Notification job', QUEUE.testMode.jobs[0].id, 'completed')
      ).to.be.true;
      done();
    });

    // Emit complete event
    QUEUE.testMode.jobs[0].emit('complete');
  });
});
