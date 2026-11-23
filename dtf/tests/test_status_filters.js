const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const source = fs.readFileSync(
    path.join(__dirname, '..', 'static', 'dtf', 'status_filter.js'),
    'utf8',
);
const { disableAbsentStatusFilters } = vm.runInNewContext(
    `${source}\n({ disableAbsentStatusFilters })`,
);

function rowWithStatus(status) {
    return {
        getElementsByClassName(className) {
            return className === 'status-filter'
                ? [{ textContent: ` ${status} ` }]
                : [];
        },
    };
}

test('disables filters with no matching rows and preserves their saved state', () => {
    const checkboxes = [
        { value: 'successful', checked: true },
        { value: 'failed', checked: false },
        { value: 'unknown', checked: true },
    ];

    disableAbsentStatusFilters(
        [rowWithStatus('successful'), rowWithStatus('failed')],
        checkboxes,
    );

    assert.equal(checkboxes[0].disabled, false);
    assert.equal(checkboxes[1].disabled, false);
    assert.equal(checkboxes[2].disabled, true);
    assert.equal(checkboxes[2].checked, true);
    assert.equal(checkboxes[1].checked, false);
});

test('disables every status filter when there are no result rows', () => {
    const checkboxes = [
        { value: 'successful' },
        { value: 'failed' },
    ];

    disableAbsentStatusFilters([], checkboxes);

    assert.deepEqual(
        checkboxes.map(checkbox => checkbox.disabled),
        [true, true],
    );
});
