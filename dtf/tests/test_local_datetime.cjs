const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const source = fs.readFileSync(
    path.join(__dirname, '..', 'static', 'dtf', 'local_datetime.js'),
    'utf8',
);
const mockModule = { exports: {} };
vm.runInNewContext(source, { module: mockModule });
const formatter = mockModule.exports;

test('formats a Date using the host locale and timezone', () => {
    const date = new Date('2026-11-24T09:09:05Z');
    const formatted = formatter.formatLocalDatetime(date);

    assert.equal(typeof formatted, 'string');
    assert.notEqual(formatted, '');
});

test('adds a localized timezone tooltip to a date element', () => {
    const date = new Date('2026-11-24T09:09:05Z');
    const element = { title: '' };

    formatter.setLocalDatetimeTooltip(element, date);

    assert.notEqual(element.title, '');
});

test('uses a long date format for tooltips', () => {
    const date = new Date('2026-11-24T09:09:05Z');
    const formatted = formatter.formatTooltipDatetime(date);

    assert.equal(typeof formatted, 'string');
    assert.notEqual(formatted, '');
});

test('formats local datetime elements and leaves malformed values unchanged', () => {
    const valid = {
        dataset: { localDatetime: '2026-11-24T09:09:05Z' },
        textContent: 'server fallback',
    };
    const invalid = {
        dataset: { localDatetime: 'not-a-date' },
        textContent: 'server fallback',
        title: 'server fallback title',
    };
    const root = {
        querySelectorAll: () => [valid, invalid],
    };

    formatter.formatLocalDatetimes(root);

    assert.notEqual(valid.textContent, 'server fallback');
    assert.notEqual(valid.title, undefined);
    assert.match(valid.title, /\([^)]+\)$/);
    assert.equal(invalid.textContent, 'server fallback');
    assert.equal(invalid.title, 'server fallback title');
});
