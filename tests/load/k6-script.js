import http from 'k6/http';
import { check, sleep } from 'k6';
import { uuidv4 } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';

export const options = {
    stages: [
        { duration: '10s', target: 10 }, // Ramp up to 10 users
        { duration: '20s', target: 50 }, // Ramp up to 50 users
        { duration: '30s', target: 50 }, // Stay at 50 users
        { duration: '10s', target: 0 },  // Ramp down
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
        http_req_failed: ['rate<0.01'],   // http errors should be less than 1%
    },
};

const BASE_URL = 'http://host.docker.internal:8080'; // Access host from container
const API_KEY = 'local-dev-api-key';

export default function () {
    const headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
    };

    // 1. Record a Fact
    const sourceId = `load-test-${uuidv4()}`;
    const payload = JSON.stringify({
        content: `Load Test Content ${uuidv4()}`,
        source_type: 'user_input',
        source_id: sourceId,
        recorded_by: 'k6-load-tester',
    });

    const recordRes = http.post(`${BASE_URL}/v1/facts`, payload, { headers });

    check(recordRes, {
        'record status is 201': (r) => r.status === 201,
        'has signature': (r) => r.json('signature') !== undefined,
    });

    if (recordRes.status === 201) {
        const factId = recordRes.json('fact_id');

        // 2. Get the Fact
        const getRes = http.get(`${BASE_URL}/v1/facts/${factId}`, { headers });
        check(getRes, {
            'get status is 200': (r) => r.status === 200,
        });
    }

    sleep(1);
}
