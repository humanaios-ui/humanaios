/**
 * Artillery Scenario Processor
 * Helper functions for load test scenarios
 */

module.exports = {
  /**
   * Setup: Called once before the scenario starts
   */
  beforeScenario: (context, ee, next) => {
    context.vars.timestamp = new Date().toISOString();
    context.vars.iteration = context.vars.$loopCount || 0;
    next();
  },

  /**
   * Per-request hook: Log assessment submissions
   */
  beforeRequest: (requestParams, context, ee, next) => {
    if (requestParams.name === "post" && requestParams.url.includes("/assessments")) {
      context.vars.submission_timestamp = Date.now();
    }
    next();
  },

  /**
   * After each request: Track metrics
   */
  afterResponse: (requestParams, response, context, ee, next) => {
    if (requestParams.name === "post" && requestParams.url.includes("/assessments")) {
      const latency = Date.now() - (context.vars.submission_timestamp || Date.now());
      console.log(`[SUBMISSION] job_id=${context.vars.job_id} latency=${latency}ms`);
    }

    if (requestParams.url.includes("/result")) {
      console.log(`[RESULT] assessment_id=${context.vars.assessment_id} li=${context.vars.learning_index || 'N/A'}`);
    }

    next();
  },

  /**
   * Cleanup: Called once after scenario completes
   */
  afterScenario: (context, ee, next) => {
    console.log(`[SCENARIO_COMPLETE] Completed at ${new Date().toISOString()}`);
    next();
  },

  /**
   * Custom function: Simulate think time
   */
  think: (context, ee, next) => {
    const seconds = context.vars.think_time || 1;
    setTimeout(() => next(), seconds * 1000);
  },

  /**
   * Custom function: Validate response
   */
  validateJobStatus: (context, ee, next) => {
    const status = context.vars.job_status;
    if (!["queued", "running", "completed", "failed"].includes(status)) {
      throw new Error(`Invalid job status: ${status}`);
    }
    next();
  },
};
