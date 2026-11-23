const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const durationSource = fs.readFileSync(
    path.join(__dirname, '..', 'static', 'dtf', 'duration.js'),
    'utf8',
);
const duration = vm.runInNewContext(
    `${durationSource}\n({ parseISO8601Duration, totalSeconds, printISO8601Duration })`,
);

test('formats durations using the server-side human-readable representation', () => {
    const cases = [
        ['PT1M1.23S', '0:01:01.230000'],
        ['PT0.4567S', '0:00:00.456700'],
        ['P400DT3H5.5M', '400 days, 3:05:30'],
        ['-P1DT1H', '-2 days, 23:00:00'],
        ['-PT1.23S', '-1 day, 23:59:58.770000'],
    ];

    for (const [isoDuration, expected] of cases) {
        const parsed = duration.parseISO8601Duration(isoDuration);
        assert.equal(duration.printISO8601Duration(parsed), expected);
    }
});

test('keeps duration conversion numeric for chart plotting', () => {
    const parsed = duration.parseISO8601Duration('PT1M1.23S');

    assert.equal(duration.totalSeconds(parsed), 61.23);
});

test('reports malformed durations without throwing', () => {
    const parsed = duration.parseISO8601Duration('not-a-duration');

    assert.equal(parsed, null);
    assert.equal(duration.totalSeconds(parsed), null);
    assert.equal(duration.printISO8601Duration(parsed), 'N/A');
});
