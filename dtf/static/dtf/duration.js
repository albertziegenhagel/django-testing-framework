
const iso8601DurationRegex = /^(?<sign>[-+]?)P(?:(?<days>\d+(\.\d+)?)D)?(?:T(?:(?<hours>\d+(\.\d+)?)H)?(?:(?<minutes>\d+(\.\d+)?)M)?(?:(?<seconds>\d+(\.\d+)?)S)?)?$/u

function parseISO8601Duration(iso8601DurationStr) {
    var matches = iso8601DurationRegex.exec(iso8601DurationStr);

    if(matches === null) {
        return null;
    }

    return {
        sign: matches.groups.sign === undefined ? '+' : matches.groups.sign,
        days: matches.groups.days === undefined ? 0 : parseFloat(matches.groups.days),
        hours: matches.groups.hours === undefined ? 0 : parseFloat(matches.groups.hours),
        minutes: matches.groups.minutes === undefined ? 0 : parseFloat(matches.groups.minutes),
        seconds: matches.groups.seconds === undefined ? 0 : parseFloat(matches.groups.seconds)
    };
}

function totalSeconds(duration) {
    if(duration === null) {
        return null;
    }

    return (duration.sign === '-' ? -1 : 1) *
        (duration.days*24*60*60 +
        duration.hours*60*60 +
        duration.minutes*60 + 
        duration.seconds);
}

function printISO8601Duration(duration) {
    if(duration === null) {
        return "N/A";
    }

    const totalMicroseconds = Math.round(totalSeconds(duration) * 1000000);
    const microsecondsPerDay = 86400 * 1000000;
    const days = Math.floor(totalMicroseconds / microsecondsPerDay);
    const remainingMicroseconds = totalMicroseconds - days * microsecondsPerDay;
    const hh = Math.floor(remainingMicroseconds / (3600 * 1000000));
    const mm = Math.floor((remainingMicroseconds % (3600 * 1000000)) / (60 * 1000000));
    const seconds = (remainingMicroseconds % (60 * 1000000)) / 1000000;
    const integerSeconds = Math.floor(seconds);
    const microseconds = Math.round((seconds - integerSeconds) * 1000000);
    const fractional = microseconds > 0
        ? `.${String(microseconds).padStart(6, '0')}`
        : "";
    const result = `${hh}:${String(mm).padStart(2, '0')}:${String(integerSeconds).padStart(2, '0')}${fractional}`;

    if(days !== 0) {
        const plural = Math.abs(days) === 1 ? "" : "s";
        return `${days} day${plural}, ${result}`;
    }

    return result;
}
